class Base:
    name = None

    def __init__(self, name=None, *args, **kwargs):
        self.name = name or ''

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.name}>'
