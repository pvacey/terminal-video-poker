#!/usr/bin/env python3
from poker import *
import pytest

# create a video poker object
# manually override the hands and score them, checking the expected values
vp = VideoPoker()

'''
test scoring hands
'''
def test_nothing():
    vp.hand = [
        Card(2,0),
        Card(3,2),
        Card(4,1),
        Card(7,3),
        Card(6,3)
    ]
    vp.score()
    assert vp.result == "GAMEOVER"

def test_nothing_2():
    vp.hand = [
        Card(2,0),
        Card(5,1),
        Card(14,2),
        Card(7,2),
        Card(13,0)
    ]
    vp.score()
    assert vp.result == "GAMEOVER"

def test_pair():
    vp.hand = [
        Card(2,0),
        Card(2,2),
        Card(4,1),
        Card(5,3),
        Card(6,3)
    ]
    vp.score()
    assert vp.result == "PAIR"

def test_pair_2():
    vp.hand = [
        Card(5,0),
        Card(2,2),
        Card(6,1),
        Card(13,3),
        Card(6,3)
    ]
    vp.score()
    assert vp.result == "PAIR"

def test_jacks():
    vp.hand = [
        Card(11,0),
        Card(2,2),
        Card(13,1),
        Card(13,3),
        Card(6,3)
    ]
    vp.score()
    assert vp.result == "JACKS OR BETTER"

def test_jacks_2():
    vp.hand = [
        Card(11,0),
        Card(2,2),
        Card(14,1),
        Card(14,3),
        Card(6,3)
    ]
    vp.score()
    assert vp.result == "JACKS OR BETTER"


def test_two_pair():
    vp.hand = [
        Card(5,0),
        Card(5,2),
        Card(13,1),
        Card(13,3),
        Card(6,3)
    ]
    vp.score()
    assert vp.result == "TWO PAIR"

def test_two_pair_2():
    vp.hand = [
        Card(14,0),
        Card(2,2),
        Card(14,1),
        Card(13,3),
        Card(2,3)
    ]
    vp.score()
    assert vp.result == "TWO PAIR"

def test_three_of_a_kind():
    vp.hand = [
        Card(14,0),
        Card(5,2),
        Card(14,1),
        Card(14,3),
        Card(2,3)
    ]
    vp.score()
    assert vp.result == "THREE OF A KIND"

def test_three_of_a_kind_2():
    vp.hand = [
        Card(11,0),
        Card(11,2),
        Card(10,1),
        Card(4,3),
        Card(11,3)
    ]
    vp.score()
    assert vp.result == "THREE OF A KIND"

def test_full_house():
    vp.hand = [
        Card(14,0),
        Card(2,2),
        Card(14,1),
        Card(14,3),
        Card(2,3)
    ]
    vp.score()
    assert vp.result == "FULL HOUSE"

def test_full_house_2():
    vp.hand = [
        Card(14,1),
        Card(4,2),
        Card(14,2),
        Card(4,3),
        Card(14,0)
    ]
    vp.score()
    assert vp.result == "FULL HOUSE"

def test_straight():
    vp.hand = [
        Card(14,1),
        Card(11,2),
        Card(13,0),
        Card(12,3),
        Card(10,0)
    ]
    vp.score()
    assert vp.result == "STRAIGHT"

def test_straight_2():
    vp.hand = [
        Card(3,0),
        Card(4,0),
        Card(5,1),
        Card(6,0),
        Card(7,0)
    ]
    vp.score()
    assert vp.result == "STRAIGHT"

def test_flush():
    vp.hand = [
        Card(3,0),
        Card(5,0),
        Card(13,0),
        Card(11,0),
        Card(12,0)
    ]
    vp.score()
    assert vp.result == "FLUSH"

def test_flush_2():
    vp.hand = [
        Card(14,1),
        Card(2,1),
        Card(13,1),
        Card(3,1),
        Card(12,1)
    ]
    vp.score()
    assert vp.result == "FLUSH"

def test_four_of_a_kind():
    vp.hand = [
        Card(11,0),
        Card(11,2),
        Card(11,1),
        Card(4,3),
        Card(11,3)
    ]
    vp.score()
    assert vp.result == "FOUR OF A KIND"

def test_four_of_a_kind_2():
    vp.hand = [
        Card(2,0),
        Card(11,2),
        Card(2,1),
        Card(2,3),
        Card(2,2)
    ]
    vp.score()
    assert vp.result == "FOUR OF A KIND"

def test_straight_flush():
    vp.hand = [
        Card(3,0),
        Card(4,0),
        Card(5,0),
        Card(6,0),
        Card(7,0)
    ]
    vp.score()
    assert vp.result == "STRAIGHT FLUSH"

def test_straight_flush_2():
    # just slightly lower than royal flush
    vp.hand = [
        Card(10,3),
        Card(13,3),
        Card(9,3),
        Card(11,3),
        Card(12,3)
    ]
    vp.score()
    assert vp.result == "STRAIGHT FLUSH"

def test_royal_flush():
    vp.hand = [
        Card(10,3),
        Card(13,3),
        Card(14,3),
        Card(11,3),
        Card(12,3)
    ]
    vp.score()
    assert vp.result == "ROYAL FLUSH"

def test_royal_flush_2():
    vp.hand = [
        Card(10,1),
        Card(12,1),
        Card(14,1),
        Card(13,1),
        Card(11,1)
    ]
    vp.score()
    assert vp.result == "ROYAL FLUSH"

'''
test payouts and betting
'''
def test_get_pay_table():
    pay_table = PayTable().get_pay_table()
    assert pay_table == [{'ROYAL FLUSH': 4000}, {'STRAIGHT FLUSH': 250}, {'FOUR OF A KIND': 125}, {'FULL HOUSE': 45}, {'FLUSH': 30}, {'STRAIGHT': 20}, {'THREE OF A KIND': 15}, {'TWO PAIR': 10}, {'JACKS OR BETTER': 5}, {'PAIR': 0}]

def test_get_payout():
    assert PayTable().get_payout('STRAIGHT') == 20

def test_get_payout_2():
    assert PayTable().get_payout('GAMEOVER') == 0

def test_get_payout_3():
    assert PayTable().get_payout('FLUSH') == 30

def test_get_payout_4():
    assert PayTable().get_payout('STRAIGHT FLUSH') == 250

def test_payout_applied():
    # scoring a flush adds 30 to balance
    vp.balance = 200
    vp.hand = [
        Card(3,1),
        Card(11,1),
        Card(2,1),
        Card(2,1),
        Card(2,1)
    ]
    vp.score()
    print(vp.balance)
    assert vp.balance == 230

def test_payout_applied_2():
    # scoring a pair adds 5 to balance
    vp.balance = 105
    vp.hand = [
        Card(3,0),
        Card(11,1),
        Card(12,3),
        Card(12,2),
        Card(2,1)
    ]
    vp.score()
    print(vp.balance)
    assert vp.balance == 110

def test_bet_deducted():
    vp.balance = 150
    vp.round = 2
    vp.draw()
    assert vp.balance == 145

def test_end_to_end():
    # start fresh, draw a hand, win a flush (forced), earn payout - bet
    vp.__init__()
    assert vp.balance == 100
    vp.draw()
    assert vp.balance == 95
    # set a flush manually
    vp.hand = [
        Card(3,1),
        Card(11,1),
        Card(5,1),
        Card(2,1),
        Card(2,1)
    ]
    # hold everything
    vp.draw(set({0,1,2,3,4}))
    assert vp.result == 'FLUSH' and vp.balance == 125

def test_end_to_end_2():
    # start fresh, draw a hand, win a pair (forced), break even
    vp.__init__()
    vp.draw()
    # set a pair manually
    vp.hand = [
        Card(3,1),
        Card(11,1),
        Card(5,2),
        Card(12,2),
        Card(12,1)
    ]
    # hold everything
    vp.draw(set({0,1,2,3,4}))
    assert vp.result == 'JACKS OR BETTER' and vp.balance == 100

'''
misc
'''
def test_paytable_pop():
    # make sure that we are using a copy of the paytable and not modifying it
    table = PayTable().get_pay_table()
    table_length = len(table)
    table.pop()
    # now get the table again, the pop should be have changed the original list
    table = PayTable().get_pay_table()
    assert table_length == len(table)

# def test_cannot_have_1():
#     vp.__init__()
#     vp.deck.shuffle()
#     for c in vp.deck.deck:
#         print(c)
#     assert False
