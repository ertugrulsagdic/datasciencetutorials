import inquirer
import numpy as np


class Card:
    def __init__(self, suite, rank):
        self.suite = suite
        self.rank = rank

    def name(self):
        return self.rank + " of " + self.suite


class Deck:
    suites = np.array(['Hearts', 'Diamonds', 'Clubs', 'Spades'])
    ranks = np.array(['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'])

    def __init__(self):
        self.cards = np.array([])
        for suite in self.suites:
            for rank in self.ranks:
                self.cards = np.append(self.cards, Card(suite, rank))

    def take_card(self):
        card = self.cards[-1]
        self.cards = np.delete(self.cards, -1)
        return card

    def remove_card(self, card):
        i,  = np.where(self.cards==card)
        self.cards = np.delete(self.cards, i[0])

    def add_card(self, card):
        self.cards = np.append(self.cards, card)

    def shuffle(self):
        if len(self.cards) < 52:
            print('Can not suffle after cards dealed.')
        else:
            np.random.shuffle(self.cards)

    def show_deck(self):
        print('Deck has ' + str(self.cards.size) + ' cards:')
        for card in self.cards:
            print(card.name())


class Player:
    def __init__(self, name):
        self.name = name
        self.cards = np.array([])

    def remove_card(self, card):
        i,  = np.where(self.cards==card)
        self.cards = np.delete(self.cards, i[0])

    def add_card(self, card):
        self.cards = np.append(self.cards, card)

    def show_cards(self):
        if (len(self.cards) == 0):
            print(self.name + ' has no cards.')
        else:
            print(self.name + ' has ' + str(self.cards.size) + ' cards:')
            for card in self.cards:
                print(card.name())


class Game:
    player_names = np.array(['Player 1', 'Player 2', 'Player 3', 'Player 4'])

    def __init__(self):
        self.deck = Deck()
        self.players = np.array([])
        for name in self.player_names:
            self.players = np.append(self.players, Player(name))

    def deal(self):
        self.deck.shuffle()
        for player in self.players:
            for _ in range(0, 8):
                card = self.deck.take_card()
                player.add_card(card)

    def exchange_cards(self, player_name):
        player = self.get_player_with_name(player_name)
        
        cards_to_add = []
        print('Cards exhanged: ')
        for _ in range(4):
            random_card_index = np.random.randint(len(player.cards) - 1)
            card = player.cards[random_card_index]
            player.remove_card(card)
            print(card.name())
            cards_to_add = np.append(cards_to_add, card)

        for _ in range(4):
            player.add_card(self.deck.take_card())

        for c1 in cards_to_add:
            self.deck.add_card(c1)

    def get_player_with_name(self, player_name):
        i,  = np.where(self.player_names==player_name)
        return self.players[i[0]]

    def show_player_info(self):
        for player in self.players:
            player.show_cards()


if __name__ == "__main__":

    game = Game()

    game.deal()

    game.show_player_info()
    print('---------------------------')

    game.deck.show_deck()
    print()

    while True:
        questions = [
            inquirer.List(
                'player_name',
                message='Select the player',
                choices= game.player_names.tolist(),
            ),
        ]
        player_name = inquirer.prompt(questions)['player_name']

        game.exchange_cards(player_name)
        print('---------------------------')

        game.get_player_with_name(player_name).show_cards()
        print('---------------------------')

        game.deck.show_deck()
        print()

        confirm = {
            inquirer.Confirm(
                'exit',
                message="Do you want to exit?" ,
                default=True
            ),
        }
        
        if inquirer.prompt(confirm)['exit']:
            exit()
