import random
import os
import sys

from helper.triage import check_best_hand

deck = ['2-h','3-h','4-h','5-h','6-h','7-h','8-h','9-h','10-h','J-h','Q-h','K-h','A-h','2-d','3-d','4-d','5-d','6-d','7-d','8-d','9-d','10-d','J-d','Q-d','K-d','A-d','2-c','3-c','4-c','5-c','6-c','7-c','8-c','9-c','10-c','J-c','Q-c','K-c','A-c','2-s','3-s','4-s','5-s','6-s','7-s','8-s','9-s','10-s','J-s','Q-s','K-s','A-s']

def reset_deck():
  global deck
  deck = ['2-h','3-h','4-h','5-h','6-h','7-h','8-h','9-h','10-h','J-h','Q-h','K-h','A-h','2-d','3-d','4-d','5-d','6-d','7-d','8-d','9-d','10-d','J-d','Q-d','K-d','A-d','2-c','3-c','4-c','5-c','6-c','7-c','8-c','9-c','10-c','J-c','Q-c','K-c','A-c','2-s','3-s','4-s','5-s','6-s','7-s','8-s','9-s','10-s','J-s','Q-s','K-s','A-s']

def serve_amount_from_deck(deck: list, amount: int = 5):
    tirage = random.sample(deck, amount)

    for x in tirage:
        deck.remove(x)
    
    return tirage
    
def card_choice(card_draw: list):
    new_card_draw = []

    for x in card_draw:
        input_message = f"Voulez vous gardez votre carte : [{x}] y/n\n"
        keeps_card = input(input_message)

        while True:
            if keeps_card.lower() == "y":
                new_card_draw.append(x)
                break
            elif keeps_card.lower() == "n":
                break
            else:
                print("Erreur: veuillez renseignez y ou n")
                keeps_card = input(input_message)

        pass

    return new_card_draw

def second_draw(chosen_cards: list, deck: list):
    if len(chosen_cards) == 5:
        return chosen_cards

    new_cards_amount = 5 - len(chosen_cards)
    chosen_cards.extend(serve_amount_from_deck(deck, new_cards_amount))

    return chosen_cards

def bank_roll(bank):
    print(f"Le montant de votre banque se situe à: {bank}€\n")
    if bank <= 0:
        print("Vous n'avez plus de sous, byebye\n")
        sys.exit()

    bet = int(input("Veuillez entrer votre mise\n"))
    while True:
        if bet > bank:
            bet = int(input("La somme renseigné est supérieur à votre banque, veuillez entrer une mise convenable\n"))
        else:
            return bet
            break
    
def main():
    bank = 50
    while True:
        bet = bank_roll(bank)
        bank -= bet
        draw = serve_amount_from_deck(deck, 5)
        print(f"Premier tirage: {draw}\n")
        chosen_cards = card_choice(draw)
        second_draw_res = second_draw(chosen_cards, deck)
        print(f"Deuxième tirage: {second_draw_res}\n")

        mult_mise, hand_result = check_best_hand(second_draw_res)

        bank += (bet * mult_mise)

        print(f"Vous avez eu une : {hand_result}\n")
        reset_deck()

main()
