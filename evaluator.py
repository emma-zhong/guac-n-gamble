import random #random module to shuffle the deck for monte-carlo
from collections import Counter #counter to count occurrences of ranks and suits

#evaluates the strength of a poker hand
#parameter: cards, a list
#returns a tuple (hand_strength, sorted_ranks)
def evaluate_hand(cards):
    
    #changes letters into values, changes cards into a list of list 
    #['AH', '10D', '5S', '3C', '2D']->[[14, 'H'], [10, 'D'], [5, 'S'], [3, 'C'], [2, 'D']]
    def parse_cards(cards):
        ranks = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 
                 '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        return [[ranks[card[:-1]], card[-1]] for card in cards]

    #counts how many times each rank appears in the list of cards
    #returns a counter (kind of like a dictionary)
    def count_ranks(cards):
        return Counter(rank for rank, _ in cards)

    #check if hand contains a flush
    def is_flush(cards):
        #count occurrences of each suit
        suit_counts = Counter(suit for _, suit in cards)
        #find if there is a flush (suit with 5 or more cards)
        flush_suit = next((suit for suit, count in suit_counts.items() if count >= 5), None)
        if flush_suit:
            #extract only cards of that suit, sort by rank (highest first)
            return sorted([rank for rank, suit in cards if suit == flush_suit], reverse=True)
        return False

    #check if hand contains a straight
    def is_straight(cards):
        #get unique ranks, sorted in descending order
        sorted_ranks = sorted(set(rank for rank, _ in cards), reverse=True)
        #check if any five consecutive ranks exist
        for i in range(len(sorted_ranks) - 4):
            if sorted_ranks[i] - sorted_ranks[i + 4] == 4:  # Difference of 4 means they are consecutive
                return sorted_ranks[i:i+5]
        #special case: A-5 straight (Ace counts as 1 here)
        if set([14, 5, 4, 3, 2]).issubset(sorted_ranks):
            return [5, 4, 3, 2, 1]
        return False
    
    #determines the strength of a hand
    def get_hand_strength(cards):
        #count occurrence of each rank
        counter = count_ranks(cards)
        #make it into a list
        counts = list(counter.values())
        #sort rank from greatest to least
        sorted_ranks = sorted(counter.keys(), key=lambda rank: (counter[rank], rank), reverse=True)

        #check for different hand rankings
        if is_flush(cards) and is_straight(cards):
            if sorted_ranks[:5] == [14, 13, 12, 11, 10]:  # Royal Flush
                return 110, sorted_ranks
            return 100, sorted_ranks  # Straight Flush
        if 4 in counts:
            return 80, sorted_ranks  # Four of a Kind
        if 3 in counts and 2 in counts:
            return 70, sorted_ranks  # Full House
        if is_flush(cards):
            return 60, sorted_ranks  # Flush
        if is_straight(cards):
            return 50, sorted_ranks  # Straight
        if 3 in counts:
            return 40, sorted_ranks  # Three of a Kind
        if counts.count(2) == 2:
            return 30, sorted_ranks  # Two Pair
        if 2 in counts:
            return 20, sorted_ranks  # One Pair
        return 1, sorted_ranks  # High Card

    #parse cards and then get hand strength
    return get_hand_strength(parse_cards(cards))

#compares two hand scores
def compare_scores(my_score, opponent_score):
    if my_score[0] > opponent_score[0]:
        return True
    elif my_score[0] < opponent_score[0]:
        return False
    else:
        #if primary hand score is the same, move onto comparing kickers
        return my_score[1] > opponent_score[1]

def simulate_win_probability(my_hand, community_cards, num_opponents, num_simulations=1000):
    #creates a deck of cards
    suits = ['h', 'd', 'c', 's']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    deck = [rank + suit for rank in ranks for suit in suits]

    #removes known cards
    known_cards = set(my_hand + community_cards)
    deck = [card for card in deck if card not in known_cards]

    wins = 0

    for _ in range(num_simulations):
        #shuffle deck
        random.shuffle(deck)
        
        # Deal opponent hands first
        opponent_hands = [deck[2 * i: 2 * (i + 1)] for i in range(num_opponents)]
        
        # Deal the remaining community cards
        remaining_community = deck[2 * num_opponents: 5 - len(community_cards) + 2 * num_opponents]
        new_community = community_cards + remaining_community
        
        #evaluate my hand + opponent hand
        my_score = evaluate_hand(my_hand + new_community)
        opponent_scores = [evaluate_hand(hand + new_community) for hand in opponent_hands]

        if all(compare_scores(my_score, op_score) for op_score in opponent_scores):
            wins += 1

    return (wins / num_simulations) * 100

my_hand = ['AH', '5H']
community_cards = ['3D','3H', '3S', '3C', '2D']
num_opponents = 2
print(evaluate_hand(my_hand + community_cards))
result = simulate_win_probability(my_hand, community_cards, num_opponents)
print(result)
