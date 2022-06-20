stub_user_mongo = {'nick_name': 'Vinicius', 'email': 'vro@lionx.com.br'}


class StubAttachmentUploadInstance:
    def __init__(self, token=None):
        self.token = token or None

    def __repr__(self):
        return f'StubAttachmentUploadInstance(token="{self.token}")'


class StubUser:
    def __init__(self, id=None, external_id=None, name=None, email=None):
        self.email = email or None
        self.external_id = external_id or None
        self.id = id or None
        self.name = name or None

    def __repr__(self):
        return f'StubUser(id="{self.id}", external_id="{self.external_id}")'


class StubGetUsers:
    def __init__(self, values=None):
        self.values = values or []

    def append_user(self, stub_user: StubUser):
        self.values.append(stub_user)
        return self

    def __repr__(self):
        return f'StubGetUsers(values="{self.values}")'