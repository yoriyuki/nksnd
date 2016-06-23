import utils

class Morph:
    def __init__(self, surface):
        self._surface = surface
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

    def surface(self):
        return self._surface

    def key(self):
        return ':' + self._surface

    def unknown_key(self):
        return '_' + self_len + self._kind
