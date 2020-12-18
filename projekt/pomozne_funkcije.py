from enum import Enum
from functools import wraps

class Meni(Enum):
    """
    Razred za izbire v menijih.
    """
    def __init__(self, ime, funkcija):
        """
        Konstruktor izbire.
        """
        self.ime = ime
        self.funkcija = funkcija

    def __str__(self):
        """
        Znakovna predstavitev izbire.
        """
        return self.ime


class Seznam(Enum):
    """
    Razred za sezname.
    """
    def __str__(self):
        """
        Znakovna predstavitev vnosa.
        """
        return self.value


class JaNe(Seznam):
    """
    Razred za izbiro ja/ne.
    """
    JA = "Ja"
    NE = "Ne"


def prekinitev(fun):
    """
    Dekorator za obravnavo prekinitev s Ctrl+C.
    """
    @wraps(fun)
    def funkcija(*largs, **kwargs):
        try:
            fun(*largs, **kwargs)
        except KeyboardInterrupt:
            print("\nPrekinitev!")
    return funkcija
