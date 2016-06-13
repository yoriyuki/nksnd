import utils

class Morph:
    def __init__(self, surface):
        self._surface = surface

    def surface(self):
        return self._surface

    def key(self):
        return ':' + self._surface

class UnknownMorph(Morph):
    def __init__(self, surface):
        super(Morph, self).__init__(surface)
        if utils.is_hiragana(surface):
            self._kind = 'hiragana'
        else if utils.is_katakana(surdace):
            self._kind = 'katakana'
        else:
            self._kind = 'other'
        if len(surface) <= 6:
            self._len = len(surface)
        else:
            self._len = '*'

    def key(self):
        return '_' + self_len + self._kind
