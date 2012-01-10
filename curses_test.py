'''
import gevent
from gevent import httplib
from time import time

def getshit(url):
	gevent.sleep(1)
	print "connecting %s" % url
	s = time()
	conn = gevent.spawn(httplib.HTTPConnection,url)
	conn.join()
	print "connecting to %s took %d" % (url,time()-s)
	print "getting %s" % url
	s = time()
	response = gevent.spawn(conn.value.request,'GET','/')
	response.join()
	print "response %s took %d" % (url,time()-s)



urls = ['google.com','google.com','google.com','google.com','google.com','google.com','google.com','google.com','google.com','google.com','google.com']

cons = [gevent.spawn(getshit,url) for url in urls]
gevent.joinall(cons)
'''

import curses,time
import curses

#define this here so its global...
stdscr = 'foobar'

def curses_print_table(table,posy=0,posx=0,column_padding=1):
	column_widths = {}
	for row_num in range(len(table)):
		if type(table[row_num]) == list:
			for element_num in range(len(table[row_num])):
				if column_widths.setdefault(element_num,0) < len(str(table[row_num][element_num])):
					column_widths[element_num] = len(str(table[row_num][element_num]))

	stdscr.clear()
	for row_num in range(len(table)):
		stdscr.move(posy+row_num,posx)
		for element_num in range(len(column_widths)):
			if element_num < len(table[row_num]):
				element = str(table[row_num][element_num])
			else:
				element = ""
			stdscr.addstr(" | %s" % element.ljust(column_widths[element_num]+column_padding))
		stdscr.addstr("|\n")
	stdscr.refresh()

def main():
	table = [[123,'zero,one','zero,two'],['one,zero','one,one','one,two'],['asdf','asdf']]
	i = 1
	while True:
		table[0][0] = i
		i *= 10
		curses_print_table(table,20,10)
		time.sleep(.1)

if __name__ == "__main__":
	#setup curses and run callback
	try:
		stdscr = curses.initscr()
		curses.noecho()
		curses.cbreak()
		curses.curs_set(0)
		stdscr.keypad(1)
		main()
		#quit nicely
		stdscr.keypad(0)
		curses.echo()
		curses.nocbreak()
		curses.endwin()
	#catch exceptions and die nice(er)
	except:
		stdscr.keypad(0)
		curses.echo()
		curses.nocbreak()
		curses.endwin()
		raise