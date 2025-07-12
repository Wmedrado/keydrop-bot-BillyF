class _Auth:
    def sign_in_with_email_and_password(self, *a, **k):
        return {}
    def create_user_with_email_and_password(self, *a, **k):
        return {}

class Firebase:
    def auth(self):
        return _Auth()

def initialize_app(config):
    return Firebase()
