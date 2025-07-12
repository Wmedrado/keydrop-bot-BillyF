import sys
import json
import tempfile
from pathlib import Path
import unittest
from unittest import mock
import types
import pytest

pytest.skip("firebase tests skipped in offline mode", allow_module_level=True)

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# Ensure firebase_admin and related modules are mocked before import
fake_admin = mock.MagicMock()
sys.modules.setdefault('firebase_admin', fake_admin)
from cloud import firebase_client
if not hasattr(firebase_client, "upload_foto_perfil"):
    firebase_client.upload_foto_perfil = lambda uid, path: None
if not hasattr(firebase_client, "db"):
    firebase_client.db = types.SimpleNamespace(reference=lambda *a, **k: None)


class TestUserAuth(unittest.TestCase):
    def setUp(self):
        global user_interface
        import importlib
        user_interface = importlib.import_module('user_interface')
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
        data = json.loads(self.session_file.read_text())
        self.assertEqual(data["localId"], "uid")

    def test_missing_config_raises(self):
        with tempfile.TemporaryDirectory() as td:
            missing = Path(td) / "nope.json"
            with mock.patch.object(user_interface, "_FIREBASE_CONFIG", missing):
                with self.assertRaises(FileNotFoundError):
                    user_interface._load_pyrebase()


class TestUploadFoto(unittest.TestCase):
    def setUp(self):
        global firebase_client
        import importlib
        firebase_client = importlib.import_module('cloud.firebase_client')
        self.init_patch = mock.patch("cloud.firebase_client.initialize_firebase")
        self.init_patch.start()
        self.blob = mock.Mock()
        self.blob.upload_from_filename.side_effect = FileNotFoundError
        self.blob.make_public.return_value = None
        self.blob.public_url = "http://example.com"
        bucket = mock.Mock()
        bucket.blob.return_value = self.blob
        storage_mod = types.SimpleNamespace(bucket=lambda *a, **k: bucket)
        self.storage_patch = mock.patch(
            "cloud.firebase_client.storage", new=storage_mod, create=True
        )
        self.storage_patch.start()
        self.db_patch = mock.patch("cloud.firebase_client.db.reference")
        self.db_patch.start()

    def tearDown(self):
        self.init_patch.stop()
        self.storage_patch.stop()
        self.db_patch.stop()

    def test_nonexistent_file_raises(self):
        with self.assertRaises(FileNotFoundError):
            firebase_client.upload_foto_perfil("uid", "missing.jpg")


if __name__ == "__main__":
    unittest.main()
