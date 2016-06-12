class Morph:
    def __init__(self, surface):
        self._surface = surface

    def surface(self):
        return self._surface

    def key(self):
        return ':' + self._surface

class UnknownMorph(Morph):
    def __init__(self, kind, surface):
        super(Morph, self).__init__(surface)
        assert kind == 'hiragana' || kind == 'katakana' || kind == 'other'
        self._kind = kind

    def key(self):
        return '_' + self._surface
