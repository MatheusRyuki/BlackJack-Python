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
        x = input("\nVocê quer comprar mais ou parar? Coloque C ou P: \n")

        if x[0].lower() == "c":
            hit(deck, hand)
        elif x[0].lower() == "p":
            print("O jogador para, turno da Casa")
            playing = False
        else:
            print("Você não colocou uma letra válida!")
            continue
        break


def show_some(player, dealer):
    print("\nMão da casa:")
    print(" <Carta Escondida>")
    print("", dealer.cards[1])
    print("\nMão do jogador:", *player.cards, sep="\n ")


def show_all(player, dealer):
    print("\nMão da casa:", *dealer.cards, sep="\n ")
    print("Mão da casa =", dealer.value)
    print("\nMão do jogador", *player.cards, sep="\n ")
    print("Mão do jogador =", player.value)


def player_busts(player, dealer, chips):
    print("\nO jogador explodiu a mão!")
    chips.lose_bet()


def player_wins(player, dealer, chips):
    print("\nO jogador ganhou!")
    chips.win_bet()


def dealer_busts(player, dealer, chips):
    print("\nO jogador ganhou! A casa explodiu a mão")
    chips.win_bet()


def dealer_wins(player, dealer, chips):
    print("\nA casa ganhou!")
    chips.lose_bet()


def push(player, dealer):
    print("O jogador e a Casa empataram!")


def start_game(chips):
    print("Bem-vindo ao 21!")

    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    player_chips = Chips(chips)

    take_bet(player_chips)

    show_some(player_hand, dealer_hand)
    playing = True
    while playing == True:
        hit_or_stand(deck, player_hand)
        show_some(player_hand, dealer_hand)

        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            playing = False

        if player_hand.value <= 21:
            hit_or_stand(deck, player_hand)
            while dealer_hand.value < 17:
                hit(deck, dealer_hand)

            show_all(player_hand, dealer_hand)

            if dealer_hand.value > 21:
                dealer_busts(player_hand, dealer_hand, player_chips)
            elif dealer_hand.value > player_hand.value or player_hand.value > 21:
                dealer_wins(player_hand, dealer_hand, player_chips)
            elif dealer_hand.value < player_hand.value:
                player_wins(player_hand, dealer_hand, player_chips)
            else:
                push(player_hand, dealer_hand)

        print("\n Quantidade de fichas atuais: {}\n".format(player_chips.total))

        if player_chips.total == 0:
            print("Você não tem mais fichas para jogar! Você quebrou!")
            break

        else:
            new_game = input("\nGostaria de jogar outra mão? s/n\n")

            if new_game[0].lower() == "s":
                start_game(player_chips.total)
            else:
                print("Obrigado por jogar!")
                break


start_game(100)
