import random

class Deck:
    def __init__(self):
        self.cards = []
        self.removed_cards = []
        for suits in range(4):
            for card in range(1, 14):
                if card == 1:
                    self.cards.append('A')
                elif card >= 10:
                    self.cards.append(10)
                else:
                    self.cards.append(card)
        random.shuffle(self.cards)

    def pickCard(self, player):
        card = self.cards[-1]
        del self.cards[-1]
        self.removed_cards.append(card)
        player.cards.append(card)
        return card

class Player:

    def __init__(self, name, money):
        self.cards = []
        self.name = name
        self.money = money

    def total_val(self):
        summ = 0
        summ2 = 0
        for x in self.cards:
            if x == 'A':
                summ += 11
            else:
                summ += x

        for x in self.cards:
            if x == 'A':
                summ2 += 1
            else:
                summ2 += x
        if summ <= 21 and summ > summ2:
            return summ
        return summ2

def loser_script():
    print("You've lost too much of your money at the table to bet!")
    print("\nWould you like to play again? Type Yes if so, otherwise, press anything.")

    word = input()
    if word == 'Yes':
        main()
    else:
        print("Goodbye!")
        quit()


def starting_money():
    while True:
        money = input()
        if not money.isdigit():
            print("That is not a valid integer value for how much you want to play with.")
            print("\nHow much money do you want to play with? Bet's start at 100")
        elif int(money) < 100:
            print("That is less than the minimum betting amount.")
        else:
            print()
            break
    return money


def betting_script(player):
    while True:
        print("How much would you like to bet?")
        amount = input()
        if not amount.isdigit():
            print("That is not a valid integer value for how much you want to bet.")
        elif int(amount) < 100:
            print("You must bet at least 100.")
        elif player.money - int(amount) < 0:
            print("You don't have that much money!")
        else:
            amount = int(amount)
            break
    return amount


def hitting_script(amount, deck, player):
    if player.money - amount * 2 >= 0:
        print("If you want to double down, press h and then hit return, otherwise press return:")
        key = input()
        if key == 'h':
            amount *= 2
            deck.pickCard(player)
            print("Your card is " + str(player.cards[-1]))
            # if player.total_val() > 21:
            #     print("You lost this hand!")
    while player.total_val() < 21:
        print("If you want to hit, press h and then hit return, otherwise press return:")
        key = input()
        if key == 'h':
            deck.pickCard(player)
            print("Your card is " + str(player.cards[-1]))
        else:
            break
        # if player.total_val() > 21:
        #     print("You lost this hand!")
    return amount


def dealer_script(dealer, deck):
    while dealer.total_val() < 17:
        deck.pickCard(dealer)
        print("The dealer hit and received a " + str(dealer.cards[-1]) + ".")
    print("\nThe dealers cards are ", end="")
    if len(dealer.cards) == 2:
        print(str(dealer.cards[0]) + " and " + str(dealer.cards[1]) + ".")
    else:
        for x in dealer.cards[0:len(dealer.cards) - 1:1]:
            print(str(x) + ", ", end="")
        print("and " + str(dealer.cards[-1]) + ".")
    print()


def determine_winner(amount, dealer, player):
    if dealer.total_val() > 21:
        print("You win!")
        player.money += amount
    elif (player.cards[0] == 'A' or player.cards[1] == 'A') and player.total_val() == 21 and dealer.total_val() != 21:
        print("You win! You earn 1.5x your bet")
        player.money += int(amount * 1.5)
    elif dealer.total_val() == player.total_val():
        print("You stay.")
    elif dealer.total_val() < player.total_val():
        print("You win!")
        player.money += amount
    else:
        print("You bust.")
        player.money -= amount


def reset_cards(player, dealer):
    player.cards = []
    dealer.cards = []


def main():
    print("Welcome to Blackjack!")
    print("Press ctrl-c to escape at anytime.\n")
    print("What's your name?")
    name = input()
    print("Hi " + name + ", let's get started!\n")
    print("How much money do you want to play with? Bet's start at 100.")

    money = starting_money()
    money = int(money)
    player = Player(name, money)
    dealer = Player("Dealer", 10000000)
    deck = Deck()

    while True:
        if player.money < 100:
            loser_script()
        if len(deck.cards) < 35:
            print("The deck is being reshuffled.")
            deck = Deck()
        print("You have $" + str(player.money) + " remaining.")

        amount = betting_script(player)

        deck.pickCard(dealer)
        deck.pickCard(dealer)
        print("\nThe dealers shown card is of value " + str(dealer.cards[-1]) + ".")
        deck.pickCard(player)
        deck.pickCard(player)
        print("Your cards are of value " + str(player.cards[0]) + ", " + str(player.cards[1]))
        if (player.cards[0] == 'A' or player.cards[1] == 'A') and player.total_val() == 21:
            print("You got a BlackJack!")
        else:
            amount = hitting_script(amount, deck, player)
        if player.total_val() <= 21:
            dealer_script(dealer, deck)
            determine_winner(amount, dealer, player)
        else:
            print("You bust.")
            player.money -= amount

        reset_cards(player, dealer)
        print()




main()