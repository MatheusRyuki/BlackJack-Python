import random

suits = ("Corações", "Diamantes", "Espadas", "Paus")
ranks = (
    "Dois",
    "Três",
    "Quatro",
    "Cinco",
    "Seis",
    "Sete",
    "Oito",
    "Nove",
    "Dez",
    "Valete",
    "Rainha",
    "Rei",
    "Ás",
)
values = {
    "Dois": 2,
    "Três": 3,
    "Quatro": 4,
    "Cinco": 5,
    "Seis": 6,
    "Sete": 7,
    "Oito": 8,
    "Nove": 9,
    "Dez": 10,
    "Valete": 10,
    "Rainha": 10,
    "Rei": 10,
    "Ás": 11,
}
playing: True


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + " de " + self.suit


class Deck:
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        deck_comp = ""
        for card in self.deck:
            deck_comp += "\n" + card.__str__()
        return "O deck tem " + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card


class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == "Ás":
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips:
    def __init__(self, total=100):
        self.total = total
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


def take_bet(chips):
    while True:
        try:
            chips.bet = int(input("Quantas fichas você deseja apostar? "))
        except:
            print("Por favor, coloque um número válido")
        else:
            if chips.bet > chips.total:
                print(
                    "Você não tem fichas o suficiente! Você tem: {}".format(chips.total)
                )
            else:
                break


def hit(deck, hand):
    single_card = deck.deal()
    hand.add_card(single_card)
    hand.adjust_for_ace()


def hit_or_stand(deck, hand):
    global playing

    while True:
        x = input("Você quer comprar mais ou parar? Coloque C ou P")

        if x[0].lower() == "C":
            hit(deck, hand)
        elif x[0].lower() == "P":
            print("O jogador para, turno da Casa")
            playing = False

        else:
            print("Você não colocou uma letra válida!")
            continue
        break


def player_busts(player, dealer, chips):
    print("O jogador explodiu a mão!")
    chips.lose_bet()


def player_wins(player, dealer, chips):
    print("O jogador ganhou!")
    chips.win_bet()


def dealer_busts(player, dealer, chips):
    print("O jogador ganhou! A casa explodiu a mão")
    chips.win_bet()


def dealer_wins(player, dealer, chips):
    print("A casa ganhou!")
    chips.lose_bet()


def push(player, dealer):
    print("O jogador e a Casa empataram!")
