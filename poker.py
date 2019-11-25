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

    def render_blank(self):
        return ('┌         ┐'
        '\n           '
        '\n           '
        '\n           '
        '\n           '
        '\n           '
        '\n└         ┘')


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
        # self.deck = []
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
        for i in range(0,5):
            if i not in selection:
                self.hand[i] = self.deck.draw(1)[0]

    def score(self):
        self.result = 'GAMEOVER'

    def render(self, num):
        str_cards = []
        for i in range(0, num):
            str_cards.append(self.hand[i].render_card())

        tmp = 'Round: {}\n'.format(self.round)
        for i in range(0,len(str_cards[0].splitlines())):
            for card in str_cards:
                tmp += '  ' + card.splitlines()[i]
            tmp+='\n'
        return tmp

    def render_frame(self, positions):
        str_cards = []
        for i in range(0,5):
            if i in positions:
                str_cards.append(self.hand[i].render_card())
            else:
                str_cards.append(self.hand[i].render_blank())

        tmp = 'Round: {}\n'.format(self.round)
        # tmp = ''
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



if __name__ == '__main__':
    vp = VideoPoker()
    selection = set()
    # selection = set({0,4})
    # selection = set({0,2,3,4})
    # print(vp.hand[0].render_blank())
    # print(vp.render_frame(selection))
    print(selection)
    for frame in vp.render_new(selection):

        print(selection)
        print(frame)
