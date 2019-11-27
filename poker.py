#!/usr/bin/python
# -*- coding: utf-8 -*-
import random

class Card(object):
    display = {
        2:'2',
        3:'3',
        4:'4',
        5:'5',
        6:'6',
        7:'7',
        8:'8',
        9:'9',
        10:'10',
        11:'J',
        12:'Q',
        13:'K',
        14:'A'
    }
    suits = {
        'clubs': '♣',
        'diamonds': '♦',
        'hearts': '♥',
        'spades': '♠'
    }

    def __init__(self, val, suit):
        self.number_value = val
        self.display_value = self.display[val]
        self.suit_val = self.suits.items()[suit][0]
        self.suit_symbol = self.suits.items()[suit][1]

    def __str__(self):
        # return render_card()
        return '{}{}'.format(self.display_value, self.suit_symbol)

    def render_card(self):
        val = self.display_value
        if len(val)<2:
            val ='{} '.format(val)
        return '''┌─────────┐
| {}      |
|         |
|    {}    |
|         |
|       {}|
└─────────┘'''.format(val, self.suit_symbol, val)

    def render_blank(self):
        return ('┌         ┐'
        '\n           '
        '\n           '
        '\n           '
        '\n           '
        '\n           '
        '\n└         ┘')


class Deck(object):
    def __init__(self):
        super(Deck, self).__init__()
        self.deck = []

    def shuffle(self):
        for i in range(2,14):
            for j in range(0,4):
                c = Card(i,j)
                self.deck.append(c)

    def draw(self, num_cards):
        cards = []
        for c in range(num_cards):
            card_index = random.randrange(0, len(self.deck), 1)
            cards.append(self.deck.pop(card_index))
        return cards

class PayTable(object):
    scores = [
        {'ROYAL FLUSH': 4000},
        {'STRAIGHT FLUSH': 250},
        {'FOUR OF A KIND': 125},
        {'FULL HOUSE': 45},
        {'FLUSH': 30},
        {'STRAIGHT': 20},
        {'THREE OF A KIND': 15},
        {'TWO PAIR': 10},
        {'PAIR': 5},
    ]

    def get_pay_table(self):
        return self.scores

    def get_payout(self, hand):
        for i in self.scores:
            k,v = i.items()[0]
            if hand == k:
                return v
        return 0

class VideoPoker(object):

    def __init__(self):
        self.deck = Deck()
        self.hand = []
        self.round = 2 # always start in gameover mode
        self.result = ''
        self.balance = 100

    def reset_round(self):
        self.deck.shuffle()
        self.hand = self.deck.draw(5)
        self.round = 1
        self.result = ''
        self.balance -= 5 # pay the bet for a new hand

    def draw(self, selection=set()):
        self.round += 1
        if self.round > 2:
            self.reset_round()
        # replace all other cards in the hand besides the selected ones
        else:
            for i in range(0,5):
                if i not in selection:
                    self.hand[i] = self.deck.draw(1)[0]
            self.score()

    def score(self):
        self.check_hand()
        self.balance += PayTable().get_payout(self.result)

    def check_hand(self):
        counts = {'values':{}, 'suits':{}}
        scores = []
        for i in self.hand:
            # count up values
            if i.number_value not in counts['values']:
                counts['values'][i.number_value] = 0
            counts['values'][i.number_value] += 1
            # count up suits
            if i.suit_val not in counts['suits']:
                counts['suits'][i.suit_val] = 0
            counts['suits'][i.suit_val] += 1


        # check for straights
        # make the list of values into a unique, sorted set
        # a set with less than 5 items means there is at least a pair in there
        uniq_vals = sorted(list(set([i.number_value for i in self.hand])))
        if len(uniq_vals) == 5:
            is_straight = True
            # if previous value is greater than 1 away in a sorted list, not a straight
            previous_value = uniq_vals[0]
            for i in uniq_vals:
                if i - previous_value > 1:
                    is_straight = False
                previous_value = i

            if is_straight:
                scores.append('STRAIGHT')

        # check for pair, 3 of a kind, 4 of a kind
        else:
            for k,v in counts['values'].items():
                if v == 4:
                    scores.append('QUADS')
                elif v == 3:
                    scores.append('TRIPS')
                elif v == 2:
                    scores.append('PAIR')

        # also check for flush
        for k,v in counts['suits'].items():
            if v == 5:
                scores.append('FLUSH')

        # assume gameover, otherwise check hands in descending order
        tmp = 'GAMEOVER'
        if 'FLUSH' in scores and 'STRAIGHT' in scores:
            tmp = 'STRAIGHT FLUSH'
            # if the lowest card is 10 in this straight flush, it's a royal flush
            if uniq_vals[0] == 10:
                tmp = 'ROYAL FLUSH'
        elif 'QUADS' in scores:
            tmp = 'FOUR OF A KIND'
        elif 'FLUSH' in scores:
            tmp = 'FLUSH'
        elif 'STRAIGHT' in scores:
            tmp = 'STRAIGHT'
        elif 'TRIPS' in scores and 'PAIR' in scores:
            tmp = 'FULL HOUSE'
        elif 'TRIPS' in scores:
            tmp = 'THREE OF A KIND'
        elif 'PAIR' in scores:
            tmp = 'PAIR'
            if scores.count('PAIR') > 1:
                tmp = 'TWO PAIR'

        self.result = tmp

    def render_frame(self, positions):
        str_cards = []
        for i in range(0,5):
            if i in positions:
                # str_cards.append(self.hand[i].render_card_v2())
                str_cards.append(self.hand[i].render_card())
            else:
                str_cards.append(self.hand[i].render_blank())

        # tmp = 'Round: {}\n'.format(self.round)
        tmp = ''
        for i in range(0,len(str_cards[0].splitlines())):
            for card in str_cards:
                tmp += '  ' + card.splitlines()[i]
            tmp+='\n'
        return tmp


    def render_new(self, selected):
        all_selected = set({0,1,2,3,4})
        populate = all_selected - selected
        printable = selected.copy()
        frames = []
        # first only show selected ones
        frames.append(self.render_frame(printable))
        # fill in the blanks
        for i in populate:
            printable.add(i)
            frames.append(self.render_frame(printable))
        return frames
