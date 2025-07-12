import importlib

def test_module_import():
    import password_reset
    assert hasattr(password_reset, 'request_reset')
    assert hasattr(password_reset, 'verify_token')
    assert hasattr(password_reset, 'reset_password')
