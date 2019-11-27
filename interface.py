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
            tmp += '     [hold]  '
        else:
            tmp += '     [    ]  '
    s.addstr(8,0, tmp)
    s.refresh()
    return tmp

def render_paytable(s, vp):
    table = PayTable().get_pay_table()
    row = 0
    s.clear()
    for i in table:
        k,v = i.items()[0]
        padding = ' '*get_right_justified_offset(s, str(k)+str(v))
        wide_string = '{}{}{}'.format(k,padding,v)
        s.addstr(row, 0, wide_string)
        if k == vp.result:
            s.addstr(row, 0, wide_string, curses.color_pair(1))
        row += 1
    s.refresh()

def render_cards(s, vp, existing_cards, first=False):
    # get frames
    frames = vp.render_new(existing_cards)
    if first:
        frames = [frames[0]]
    last_frame = None
    # draw each frame
    for i in frames:
        time.sleep(0.25)
        s.clear()
        # s.addstr(0, 0, i, curses.color_pair(1))
        s.addstr(0, 0, i)
        s.addstr(11,0, 'CREDIT {}'.format(vp.balance))

        if vp.round == 2:
            s.addstr(11,get_center_offset(s,vp.result), vp.result)

        tmp = 'BET'
        if vp.round == 1:
            tmp = 'DRAW'
        tmp = '{} [ENTER]'.format(tmp)
        s.addstr(11, get_right_justified_offset(s, tmp), tmp)
        render_selection(s, existing_cards)
        s.refresh()


def draw_menu(stdscr):
    k = 0
    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    # Initialization
    height, width = stdscr.getmaxyx()
    stdscr.refresh()

    width = 67
    paytable_win = curses.newwin(0,width,0,0)
    card_win = curses.newwin(14,width,10,0)
    card_win.clear()



    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # init poker stuff
    selection = set()
    vp = VideoPoker()
    # set a useless hand and render the blanks
    vp.hand = [ Card(14,0), Card(14,0), Card(14,0), Card(14,0), Card(14,0) ]
    render_paytable(paytable_win, vp)
    render_cards(card_win, vp, selection, first=True)

    while (k not in [ord('q'), ord('Q')]):
        # Initialization
        # stdscr.clear()
        height, width = stdscr.getmaxyx()

        # render_cards(card_win, vp, selection, first=True)

        if k == 10: # enter key
            # reset selection on first round, show result on second
            if vp.round == 2:
                selection = set()

            vp.draw(selection)
            render_paytable(paytable_win, vp)
            render_cards(card_win, vp, selection)

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
