class MxItem:
    def __init__(self, parent, path, name):
        self._parent = parent
        self._path = path
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def path(self):
        return self._path

    @property
    def parent(self):
        return self._parent

    def __eq__(self, other):
        if not isinstance(other, MxItem):
            return False
        if self.name != other.name:
            return False
        if self.path != other.path:
            return False
        if self.parent != other.parent:
            return False
        return True


