# add threads to be faster
import threading
import socket
import sys
import time
from math import floor


# globalizing vars
portStart = 0
portEnd = 0
HOST = 0
thread_count = 0

if (len(sys.argv) > 5):
	print("Too many arguments")
	print("scanner [hostname] [thread count] [starting port] [ending port]")
	exit()

# made loop to help with error handling
while True:
	# checking for hostname
	try:
		if (len(sys.argv) >= 2):
			HOST = socket.gethostbyname(sys.argv[1])
		else:
			HOST = input("Who would you like to scan? ")
			HOST = socket.gethostbyname(HOST)
	except socket.gaierror as err:
		print("Address Invalid:", err)
		continue


	# checking for thread count
	try:
		if (len(sys.argv) >= 3 and int(sys.argv[2]) > 0):
			thread_count = int(sys.argv[2])
		else:
			thread_count = int(input("How many threads do you want to use? "))
	except ValueError as err:
		print("Invalid count:", err)
		continue


	# checking for port range
	try:
		if ((len(sys.argv) == 4)):
			sys.argv.pop()
			raise ValueError
		elif (len(sys.argv) == 5):
			portStart = sys.argv[4]
			portEnd = sys.argv[5]
		else:
			portStart = int(input("At what port would you like to start? "))
			portEnd = int(input("At what port would you like to stop? "))
	except ValueError as err:
		print("Invalid port numbers:", err)
		continue

	break 	#breaks out of loop when no errors


def partitioned_scan(start, end):
	print(f'{threading.current_thread().name}: {start}, {end}')
	for i in range(start, end+1):
		# making socket obj to connect to server
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			connection = s.connect_ex((HOST,i))

			if connection == 0:
				print(f'Port {i}:\tOpen')

			if (floor(((time.time() - start) % 30)) == 0):
				print(f'Still scanning. On port {i}')

		print( f'{threading.current_thread().name} scanned port {i}.')



portLength = int(portEnd - portStart + 1)
thread_partition_size = int(portLength / thread_count)


if __name__ == "__main__":
	# marking start
	start = time.time()
	print("Starting scan...\n")


	if (thread_count > 1):
		thread_list = []
		# for loop to create, start, and join thread
		# store in array
		for thread in range(thread_count):
			print(thread)
			thread_list.append(threading.Thread(target=partitioned_scan, args=( (thread_partition_size*thread)+1, (thread_partition_size * (thread+1)) )))
		
		for thread in thread_list:
			thread.start()

		for thread in thread_list:
			thread.join()
	else:
		partitioned_scan(portStart, portEnd)


	print("\nScan complete...")
	print(f'Time taken: {time.time() - start}')
