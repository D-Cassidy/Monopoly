import numpy as np
from constants import PROPERTY_INFO
from constants import SQUARE_NAMES

BOARD_SIZE = 40
NUM_PLAYERS = 4
STARTING_MONEY = 1500

class Board(object):

    def __init__(self):
        self.MAX_PLAYERS = 8

    def setup_game(self, num_players):
        if (len(SQUARE_NAMES) != BOARD_SIZE): return
        if (NUM_PLAYERS > self.MAX_PLAYERS or NUM_PLAYERS < 0): return

        # Squares
        self.squares = []
        for i in range(BOARD_SIZE):
            if (SQUARE_NAMES[i] in PROPERTY_INFO.keys()):
                self.squares.append(Property(SQUARE_NAMES[i]))
            else:
                self.squares.append(Square(SQUARE_NAMES[i]))

        assert len(self.squares) == BOARD_SIZE

        # Players
        self.players = []
        for i in range(NUM_PLAYERS):
            name = "P" + str(i+1)
            self.players.append(Player(i, name, STARTING_MONEY))

        # Community Chest
        self.community_chance = []

        # Chance
        self.chance = []

    def roll(self):
        d1, d2 = 0, 0
        d1 = np.random.randint(1, 6)
        d2 = np.random.randint(1, 6)

        return d1 + d2


class Square(object):

    def __init__(self, name):
        self.name = name

    def type(self):
        return "square"


class Property(Square):

    def __init__(self, name):
        self.name = name

        self.price = PROPERTY_INFO[name][0]
        self.rent = PROPERTY_INFO[name][1]
        self.price_per_house = PROPERTY_INFO[name][2]

        self.owner = -1 # -1 for no owner
        self.mortgaged = False
        self.num_houses = 0

    def type(self):
        return "property"

    def get_rent(self, prop, player, roll=0):
        rent = -1
        utilities = ['Electric Company', 'Water Works']
        rr = ['Reading Railroad', 'Pennsylvania Railroad', 'B. & O. Railroad', 'Short Line']

        if (property.name in utilities):
            count = -1
            for p in utilities:
                if (p in player.properties): count+=1
            rent = prop.rent[count] * roll

        elif (property.name in rr):
            count = -1
            for p in rr:
                if (p in player.properties): count+=1
            rent = prop.rent[count]

        else:
            rent = prop.rent[prop.num_houses]

        return rent


class Player(object):

    def __init__(self, number, name, balance):
        self.number = number
        self.name = name
        self.balance = balance

        self.properties = []
        self.jail_cards = 0

        self.position = 0 # Starts on GO square

    def change_balance(self, amount):
        self.balance += amount

board = Board()
board.setup_game(NUM_PLAYERS)
