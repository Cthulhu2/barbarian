import enum
from optparse import Values

OPTS = Values()


class Partie(enum.Enum):
    demo = enum.auto()
    solo = enum.auto()
    vs = enum.auto()


class Game:  # Mutable options
    Country = 'Europe'  # USA, Europe
    Decor = 'foret'  # foret, plaine, trone, arene
    Partie = Partie.solo
    IA = 0
    ScoreA = 0
    ScoreB = 0
