import sys, os, locale, curses
import poker
locale.setlocale(locale.LC_ALL, '')

def render_selection(selection):
    tmp = ''
    for i in range(0,5):
        if i in selection:
            tmp += '     [hold]  '
        else:
            tmp += '     [    ]  '
    return tmp

def draw_menu(stdscr):
    k = 0
    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    vp = poker.VideoPoker()
    card_rendering = vp.render()
    selection = set()

    while (k != ord('q')):
        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        if k == 10: # enter key
            vp.draw(selection)
            card_rendering = vp.render()
            # reset selection on first round, show result on second
            if vp.round == 1:
                selection = set()
        elif k in [49,50,51,52,53]:
            # only make changes during round 1
            if vp.round == 1:
                i = k-49
                if i not in selection:
                    selection.add(i)
                else:
                    selection.remove(i)


        # Rendering cards and the cards to hold
        stdscr.addstr(0, 0, card_rendering)
        stdscr.addstr(8,0, render_selection(selection))
        stdscr.addstr(11,26, vp.result)
        stdscr.addstr(12,0, '')
        # stdscr.addstr(10,1, str(list(selection)))
        # stdscr.addstr(11,1, 'last key = {}'.format(k))

        # Refresh the screen
        stdscr.refresh()
        # Wait for next input
        k = stdscr.getch()

def main():
    curses.wrapper(draw_menu)

if __name__ == "__main__":
    main()
