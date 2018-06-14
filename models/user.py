from .model import Model


class User(Model):
    """
    User 是一个保存用户数据的 model
    现在只有两个属性 username 和 password
    """
    def __init__(self, form):
        self.id = form.get('id', None)
        self.name = form.get('name', '游客')
        # self.username = form.get('username', '')
        self.password = form.get('password', '')