class UserView:
    def __init__(self, content):
        self._content = content

    def __str__(self):
        return self._content
