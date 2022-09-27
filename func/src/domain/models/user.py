class UserData:
    email: str
    nick_name: str
    unique_id: str

    def __init__(self, email: str, nick_name: str, unique_id: str, **kwargs):
        self.email = email
        self.nick_name = nick_name
        self.unique_id = unique_id
