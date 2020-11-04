from collections import defaultdict

card_order_dict = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J" ,"Q", "K", "A"]

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