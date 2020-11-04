import random
import sys
from collections import defaultdict

card_order_dict = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J" ,"Q", "K", "A"]

def get_deck():
  deck = ['2-h','3-h','4-h','5-h','6-h','7-h','8-h','9-h','10-h','J-h','Q-h','K-h','A-h','2-d','3-d','4-d','5-d','6-d','7-d','8-d','9-d','10-d','J-d','Q-d','K-d','A-d','2-c','3-c','4-c','5-c','6-c','7-c','8-c','9-c','10-c','J-c','Q-c','K-c','A-c','2-s','3-s','4-s','5-s','6-s','7-s','8-s','9-s','10-s','J-s','Q-s','K-s','A-s']
  return deck

def loop_deck_removal(cards):
  deck = get_deck()

  for x in cards:
    deck.remove(x)

  return deck

def serve_amount_from_deck(deck: list, amount: int = 5):
    tirage = random.sample(deck, amount)

    for x in tirage:
      deck.remove(x)
    
    return tirage

def deuxieme_tirage(chosen_cards: list, deck: list):
    if len(chosen_cards) == 5:
        return chosen_cards

    new_cards_amount = 5 - len(chosen_cards)
    chosen_cards.extend(serve_amount_from_deck(deck, new_cards_amount))

    return chosen_cards

def deconstruct_draw(draw):
  rank_array = [h.split("-")[0] for h in draw]
  color_array = [h.split("-")[1] for h in draw]

  return rank_array, color_array


def check_flush(draw):
    rank_array, color_array = deconstruct_draw(draw)

    if len(set(color_array)) == 1:
      return True

    return False

def check_straight(draw):
  rank_array, color_array = deconstruct_draw(draw)

  if sorted(rank_array) == ['2', '3', '4', '5', 'A']:
    return True

  for i in range(9):
    if sorted(rank_array) == sorted(card_order_dict[i:5+i]):
      return True
  
  return False

def check_royal_flush(draw):
  rank_array, color_array = deconstruct_draw(draw)

  if check_flush(draw) == True and sorted(rank_array) == ['10', 'A', 'J', 'K', 'Q']:
    return True
  
  return False

def check_straight_flush(draw):
  rank_array, color_array = deconstruct_draw(draw)

  if check_flush(draw) == True and check_straight(draw) == True:
    return True

  return False

def check_four_of_a_kind(draw):
  rank_array, color_array = deconstruct_draw(draw)
  value_counts = defaultdict(lambda:0)

  for i in rank_array:
    value_counts[i]+=1

  if sorted(value_counts.values()) == [1,4]:
    return True
  return False

def check_full_house(draw):
  rank_array, color_array = deconstruct_draw(draw)
  value_counts = defaultdict(lambda:0)

  for v in rank_array:
        value_counts[v]+=1

  if sorted(value_counts.values()) == [2,3]:
    return True
  return False

def check_three_of_a_kind(draw):
  rank_array, color_array = deconstruct_draw(draw)
  value_counts = defaultdict(lambda:0)

  for i in rank_array:
    value_counts[i]+=1

  if set(value_counts.values()) == set([3, 1]):
    return True
  return False

def check_two_pairs(draw):
  rank_array, color_array = deconstruct_draw(draw)
  value_counts = defaultdict(lambda:0)

  for v in rank_array:
        value_counts[v]+=1

  if sorted(value_counts.values()) == [1,2,2]:
    return True
  return False

def check_one_pair(draw):
  rank_array, color_array = deconstruct_draw(draw)
  value_counts = defaultdict(lambda:0)

  for v in rank_array:
        value_counts[v]+=1

  if sorted(value_counts.values()) == [1,1,1,2]:
    return True
  return False

def check_best_hand(draw):
  if check_royal_flush(draw):
    return 250, "Quinte Flush Royale"
  elif check_straight_flush(draw):
    return 50, "Quinte Flush"
  elif check_four_of_a_kind(draw):
    return 25, "Carré"
  elif check_full_house(draw):
    return 9, "Full House"
  elif check_flush(draw):
    return 6, "Flush"
  elif check_straight(draw):
    return 4, "Quinte"
  elif check_three_of_a_kind(draw):
    return 3, "Brelan"
  elif check_two_pairs(draw):
    return 2, "Double Paire"
  elif check_one_pair(draw):
    return 1, "Paire"

  return 0, "Rien"

# def bank_roll(bank):
#     print(f"Le montant de votre banque se situe à: {bank}€\n")
#     if bank <= 0:
#         print("Vous n'avez plus de sous, byebye\n")
#         sys.exit()

#     bet = int(input("Veuillez entrer votre mise\n"))
#     while True:
#         if bet > bank:
#             bet = int(input("La somme renseigné est supérieur à votre banque, veuillez entrer une mise convenable\n"))
#         else:
#             break