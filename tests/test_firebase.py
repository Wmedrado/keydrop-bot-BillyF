import sys
import json
import tempfile
from pathlib import Path
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import user_interface
from cloud import firebase_client
import types
import sys

# Ensure stub modules exist for patching
if 'cloud.firebase_client.storage' not in sys.modules:
    storage_mod = types.ModuleType('cloud.firebase_client.storage')
    storage_mod.bucket = lambda *a, **k: None
    sys.modules['cloud.firebase_client.storage'] = storage_mod
    firebase_client.storage = storage_mod
if 'cloud.firebase_client.db' not in sys.modules:
    db_mod = types.ModuleType('cloud.firebase_client.db')
    db_mod.reference = lambda *a, **k: None
    sys.modules['cloud.firebase_client.db'] = db_mod
    firebase_client.db = db_mod


class TestUserAuth(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.session_file = Path(self.tmp.name) / "session.json"
        self.patcher_file = mock.patch.object(user_interface, "_SESSION_FILE", self.session_file)
        self.patcher_file.start()

    def tearDown(self):
        self.patcher_file.stop()
        self.tmp.cleanup()

    def test_login_saves_session_file(self):
        mock_auth = mock.Mock()
        mock_auth.sign_in_with_email_and_password.return_value = {
            "idToken": "token",
            "refreshToken": "refresh",
            "localId": "uid",
        }
        mock_fb = mock.Mock()
        mock_fb.auth.return_value = mock_auth
        with mock.patch.object(user_interface, "_load_pyrebase", return_value=mock_fb):
            user_interface.autenticar_usuario("a@b.com", "123")
        self.assertTrue(self.session_file.exists())
        try:
            sf_content = self.session_file.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            sf_content = self.session_file.read_text(encoding="latin-1")
        data = json.loads(sf_content)
        self.assertEqual(data["localId"], "uid")

    def test_missing_config_raises(self):
        with tempfile.TemporaryDirectory() as td:
            missing = Path(td) / "nope.json"
            with mock.patch.object(user_interface, "_FIREBASE_CONFIG", missing):
                with self.assertRaises(FileNotFoundError):
                    user_interface._load_pyrebase()


class TestUploadFoto(unittest.TestCase):
    def setUp(self):
        if not hasattr(firebase_client, 'storage'):
            self.skipTest('firebase_admin not available')
        self.init_patch = mock.patch("cloud.firebase_client.initialize_firebase")
        self.init_patch.start()
        self.blob = mock.Mock()
        self.blob.upload_from_filename.side_effect = FileNotFoundError
        self.blob.make_public.return_value = None
        self.blob.public_url = "http://example.com"
        bucket = mock.Mock()
        bucket.blob.return_value = self.blob
        self.bucket_patch = mock.patch("cloud.firebase_client.storage.bucket", return_value=bucket)
        self.bucket_patch.start()
        self.db_patch = mock.patch("cloud.firebase_client.db.reference")
        self.db_patch.start()

    def tearDown(self):
        self.init_patch.stop()
        self.bucket_patch.stop()
        self.db_patch.stop()

    def test_nonexistent_file_raises(self):
        with self.assertRaises(FileNotFoundError):
            firebase_client.upload_foto_perfil("uid", "missing.jpg")


if __name__ == "__main__":
    unittest.main()
