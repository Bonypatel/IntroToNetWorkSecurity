import hashlib
import random
import time
from openpyxl import Workbook

def create_puzzle(byte):
	bitstring = "0b"
	for num in range(0, byte * 8):
		bitstring += str(random.randint(0, 1))
	return bitstring

def main():
	times = []
	numTrials = raw_input("Enter number of trials: ")
	startByte = raw_input("Enter byte to test: ")
	print("")

	book = Workbook()
	sheet = book.active
	sheet['A1'] = 'Byte'
	sheet['B1'] = 'Time'

	bitstring = create_puzzle(int(startByte))
	#print("P = %s\n" % bitstring)
	bits = 1 << (int(startByte) * 8)
	for trial in range(1, (int(numTrials) + 1)):
		start = time.time() * 1000
		while(True):
			message = ""
			for num in range(0, 1000):
				message += str(random.randint(0, 1))
			guess = hashlib.sha256(message).hexdigest()
			guess = "0x" + guess
			if(bin(int(guess, 16) & (bits-1)) == bitstring):
				break;
		end = time.time() * 1000
		sheet['A' + str(trial + 1)] = str(startByte)
		sheet['B' + str(trial + 1)] = str(end - start)

		sheetName = "bytes_" + str(startByte) + "_trials_" + str(numTrials) + ".xlsx"
		book.save(str(sheetName))
		times.append(end - start)

		#print("M = %s\n" % message)

	avg = sum(times)/int(numTrials)
	print("avg time for %s bytes: %d ms" % (startByte, avg))
	del times[:]

if __name__ == "__main__":
	main()