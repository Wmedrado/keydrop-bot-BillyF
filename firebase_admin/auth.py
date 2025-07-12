class _User:
    def __init__(self, uid='uid'):
        self.uid = uid


def get_user_by_email(email):
    return _User()


def update_user(uid, password):
    return _User(uid)
