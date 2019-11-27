#!/usr/bin/env python3
import sys
import os
import locale
import curses
import time

from poker import *
locale.setlocale(locale.LC_ALL, '')

def get_right_justified_offset(screen, string):
    height, width = screen.getmaxyx()
    return (width - len(string) - 1)

def get_center_offset(screen, string):
    height, width = screen.getmaxyx()
    half_length_of_message = int(len(string) / 2)
    middle_column = int(width / 2)
    return middle_column - half_length_of_message

def render_selection(s, selection):
    tmp = ''
    for i in range(0,5):
        if i in selection:
            tmp += '       [x]     '
        else:
            tmp += '       [ ]     '
    s.addstr(10,1, tmp)
    s.refresh()
    return tmp

def render_paytable(s, vp):
    table = PayTable().get_pay_table()
    row = 1
    s.clear()
    # drop pairs
    table.pop()
    for i in table:
        k,v = list(i.items())[0]
        padding = ' '*(get_right_justified_offset(s, str(k)+str(v))-3)
        wide_string = ' {}{}{} '.format(k,padding,v)
        s.addstr(row, 1, wide_string)
        if k == vp.result and vp.round == 2:
            s.addstr(row, 1, wide_string, curses.color_pair(3))
        row += 1
    s.box(0,0)
    s.refresh()

def render_status_line(s, vp):
    row = 12
    s.addstr(row,1, ' CREDIT {} '.format(vp.balance))
    s.addstr(row,get_center_offset(s,vp.result), vp.result)
    if vp.round == 2:
        if vp.result == '' or vp.result == 'PAIR':
            s.addstr(row,get_center_offset(s,'GAME OVER'), 'GAME OVER')
        else:
            s.addstr(row,get_center_offset(s,vp.result), vp.result)

    tmp = 'BET 5'
    if vp.round == 1:
        tmp = 'DRAW'
    tmp = '{} [ENTER] '.format(tmp)
    s.addstr(row, get_right_justified_offset(s, tmp), tmp)
    s.refresh()

def render_cardwin(s, vp, existing_cards, first=False):
    all_selected = set({0,1,2,3,4})
    populate = all_selected - existing_cards
    printable = existing_cards.copy()

    # only start each render sequence showing the selected cards
    render_cards(s, vp, printable)
    render_selection(s, existing_cards)
    render_status_line(s, vp)
    s.box(0,0)
    if not first:
        time.sleep(0.3)
        # fill in the blanks
        for i in populate:
            s.clear()
            printable.add(i)
            # render_selection(s, existing_cards)
            render_cards(s, vp, printable)
            render_selection(s, existing_cards)
            render_status_line(s, vp)
            s.box(0,0)
            s.refresh()
            time.sleep(0.15)


def render_cards(s, vp, existing_cards, first=False):
    width = 11
    height = 7
    padding = 4
    x_margin = 2
    y_margin = 1

    left = padding
    right = padding + width
    up = 2
    down = height + up
    index = 0

    s.clear()
    s.box(0,0)
    for c in vp.hand:
        for y in range(up, down):
            for x in range(left, right):
                # if index not in existing_cards:
                if index in existing_cards:
                    color = curses.color_pair(1)
                    # print filler space
                    s.addstr(y, x, ' ', color)

                    char_width = len(c.display_value)

                    # red for some cards
                    if c.suit_val in ['hearts', 'diamonds']:
                        color = curses.color_pair(2)
                    # top left
                    if x == (left+x_margin) and y == (up+y_margin):
                        s.addstr(y, x, c.display_value, color)
                    if (char_width > 1) and x == (left+x_margin+1) and y == (up+y_margin):
                        s.addstr(y, x, c.display_value[1], color)
                    # center
                    middle_x = left + int((right-left)/2)
                    middle_y = up + int((down-up)/2)
                    if x == middle_x and y == middle_y:
                        s.addstr(y, x, c.suit_symbol, color)
                    # bottom right
                    first_val = c.display_value[0]
                    second_val = None
                    if char_width > 1:
                        second_val = c.display_value[1]
                    if x == (right-x_margin-1) and y == (down-y_margin-1):
                        s.addstr(y, x, first_val, color)
                        if second_val:
                            s.addstr(y, x, second_val, color)
                    if second_val and x == (right-x_margin-2) and y == (down-y_margin-1):
                        s.addstr(y, x, first_val, color)
                else:
                    s.addstr(y, x, 'X', curses.color_pair(4))

        left += width + padding
        right += width + padding
        index += 1
    s.refresh()

def draw_menu(stdscr):

    # Initialization
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    stdscr.refresh()
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_RED)

    width = 79
    paytable_win = curses.newwin(11,width,0,0)
    card_win = curses.newwin(14,width,11,0)
    card_win.clear()

    # init poker stuff
    k = 0
    selection = set()
    vp = VideoPoker()
    # set a useless hand and render the blanks
    vp.hand = [ Card(14,0), Card(14,0), Card(14,0), Card(14,0), Card(14,0) ]
    render_paytable(paytable_win, vp)
    render_cardwin(card_win, vp, selection, first=True)

    while (k not in [ord('q'), ord('Q')]):

        if k == 10: # enter key
            # reset selection on first round, show result on second
            if vp.round == 2:
                selection = set()

            vp.draw(selection)
            render_cardwin(card_win, vp, selection)
            render_paytable(paytable_win, vp)

        elif k in [49,50,51,52,53]: # 1,2,3,4,5 keys
            # only allow "hold" changes during round 1
            if vp.round == 1:
                i = k-49
                if i not in selection:
                    selection.add(i)
                else:
                    selection.remove(i)
                render_selection(card_win, selection)

        # Wait for next input
        k = stdscr.getch()

def main():
    curses.wrapper(draw_menu)

if __name__ == "__main__":
    main()
'''
TODO
- render `10` instead of `T`
- scrolling credits vs 1 frame update
- maybe not possible
    - flash center of status bar on payout? might mean no waiting for key input
    - beep on payout???
'''
