import ci.check_frontend_backend_sync as sync

def test_frontend_backend_sync():
    front = sync.get_frontend_endpoints()
    back = sync.get_backend_endpoints()
    assert front <= back
    assert sync.main() == 0
