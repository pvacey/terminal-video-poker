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
    return (width - len(string))

def get_center_offset(screen, string):
    height, width = screen.getmaxyx()
    half_length_of_message = int(len(string) / 2)
    middle_column = int(width / 2)
    return middle_column - half_length_of_message

def render_selection(s, selection):
    tmp = ''
    for i in range(0,5):
        if i in selection:
            tmp += '        [x]    '
        else:
            tmp += '        [ ]    '
    s.addstr(8,0, tmp)
    s.refresh()
    return tmp

def render_paytable(s, vp):
    table = PayTable().get_pay_table()
    row = 0
    s.clear()
    # drop pairs
    table.pop()
    for i in table:
        k,v = list(i.items())[0]
        padding = ' '*get_right_justified_offset(s, str(k)+str(v))
        wide_string = '{}{}{}'.format(k,padding,v)
        s.addstr(row, 0, wide_string)
        if k == vp.result:
            s.addstr(row, 0, wide_string, curses.color_pair(3))
        row += 1
    s.refresh()

def render_status_line(s, vp):
    s.addstr(11,0, 'CREDIT {}'.format(vp.balance))
    if vp.round == 2:
        s.addstr(11,get_center_offset(s,vp.result), vp.result)
    tmp = 'BET 5'
    if vp.round == 1:
        tmp = 'DRAW'
    tmp = '{} [ENTER]'.format(tmp)
    s.addstr(11, get_right_justified_offset(s, tmp), tmp)
    s.refresh()

def render_cardwin(s, vp, existing_cards, first=False):
    all_selected = set({0,1,2,3,4})
    populate = all_selected - existing_cards
    printable = existing_cards.copy()

    # only start each render sequence showing the selected cards
    render_cards(s, vp, printable)
    render_selection(s, existing_cards)
    render_status_line(s, vp)
    if not first:
        time.sleep(0.5)
        # fill in the blanks
        for i in populate:
            s.clear()
            printable.add(i)
            # render_selection(s, existing_cards)
            render_cards(s, vp, printable)
            render_selection(s, existing_cards)
            render_status_line(s, vp)
            s.refresh()
            time.sleep(0.25)

def render_cards(s, vp, existing_cards, first=False):
    width = 11
    height = 7
    padding = 4
    x_margin = 2
    y_margin = 1

    left = padding
    right = padding + width
    up = 0
    down = height
    index = 0



    s.clear()
    # s.addstr(13, 0, str(existing_cards))
    for c in vp.hand:
        for y in range(up, down):
            for x in range(left, right):
                # if index not in existing_cards:
                if index in existing_cards:
                    color = curses.color_pair(1)
                    # print filler space
                    s.addstr(y, x, ' ', color)

                    # red for some cards
                    if c.suit_val in ['hearts', 'diamonds']:
                        color = curses.color_pair(2)
                    # top left
                    if x == (left+x_margin) and y == (up+y_margin):
                        s.addstr(y, x, c.display_value, color)
                    # center
                    middle_x = left + int((right-left)/2)
                    if x == middle_x and y ==int(down/2):
                        s.addstr(y, x, c.suit_symbol, color)
                    # bottom right
                    if x == (right-x_margin-1) and y == (down-y_margin-1):
                        s.addstr(y, x, c.display_value, color)
                else:
                    s.addstr(y, x, 'X', curses.color_pair(4))
                    # if (x == left or x == right-1)  or (y == up or y == down-1):
                    #     s.addstr(y, x, ' ', curses.color_pair(1))

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
    paytable_win = curses.newwin(10,width,0,0)
    card_win = curses.newwin(14,width,10,0)
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
