import os
import pty
from threading import Thread

class PyTerm:
	def __init__(self):
		pass


	def _startOutputPollingThread(self, output_handler):

		def pollingOutput(cout, output_handler):
			while not cout.closed:
				line = cout.readline()
				output_handler(line)

		self._outputPollingThread = Thread(target=pollingOutput, args=(self._cout, output_handler))
		self._outputPollingThread.start()

	'''
		@param	shell	str		the location of the shell you like e.g. '/bin/bash'
		@param	output_handler	func	a callback when ptm output ready
	'''
	def prepare(self, shell, output_handler):
		(self._pid, fd) = pty.fork()
		if self._pid:
			# parent
			self._cin = os.fdopen(fd, "w")
			self._cout = os.fdopen(fd, "r")
			self._startOutputPollingThread(output_handler)
		else:
			# child
			os.execv(shell, (shell,))


	'''
		it will write as a keyboard like fd to ptm fd
	'''
	def exe(self, cmd):
		self._cin.write(cmd+"\n")


'''
	Example
'''

def output_handler(line):
	print "[OUTPUT] " + line

term = PyTerm()
term.prepare("/bin/bash", output_handler)
term.exe("pwd")

term.exe("exit")





