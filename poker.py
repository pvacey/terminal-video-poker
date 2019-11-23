#!/usr/bin/python
# -*- coding: utf-8 -*-
import random

class Card(object):
    def __init__(self, val, suit_val, suit_symbol):
        self.val = val
        self.suit_val = suit_val
        self.suit_symbol = suit_symbol

    def __str__(self):
        # return render_card()
        return '{}{}'.format(self.val, self.suit_symbol)

    def render_card(self):
        val = self.val
        if len(val)<2:
            val ='{} '.format(val)
        return '''┌─────────┐
| {}      |
|         |
|    {}    |
|         |
|       {}|
└─────────┘'''.format(val, self.suit_symbol, val)

class Deck(object):
    suit = [
        {'name':'diamonds', 'symbol': '♦'},
        {'name':'hearts', 'symbol': '♥'},
        {'name':'clubs', 'symbol': '♣'},
        {'name':'spades', 'symbol': '♠'}
    ]
    val = ['2','3','4','5','6','7','8','9','10', 'J', 'Q', 'K', 'A']

    def __init__(self):
        super(Deck, self).__init__()
        self.deck = []

    def shuffle(self):
        self.deck = []
        for s in self.suit:
            for v in self.val:
                self.deck.append(Card(v,s['name'],s['symbol']))

    def draw(self, num_cards):
        cards = []
        for c in range(num_cards):
            card_index = random.randrange(0, len(self.deck), 1)
            cards.append(self.deck.pop(card_index))
        return cards

class VideoPoker(object):
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.hand = self.deck.draw(5)
        self.round = 1
        self.result = ''

    def draw(self, selection):
        self.round += 1
        if self.round == 2:
            self.score()
        if self.round > 2:
            self.__init__()

        # replace all other cards in the hand besides the selected ones
        new_cards = self.deck.draw(5-len(selection))
        for i in range(0,5):
            if i not in selection:
                self.hand[i] = new_cards.pop()

    def score(self):
        self.result = 'GAMEOVER'

    def render(self, num=5):
        str_cards = []
        for c in self.hand:
            str_cards.append(c.render_card())

        tmp = 'Round: {}\n'.format(self.round)
        for i in range(0,len(str_cards[0].splitlines()),1):
            for card in str_cards:
                tmp += '  ' + card.splitlines()[i]
            tmp+='\n'
        return tmp

# deck = Deck()
# deck.shuffle()
#
# hand = deck.draw(5)
# print_hand(hand)
