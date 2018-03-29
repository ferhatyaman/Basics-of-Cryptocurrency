#Created by Gulsum Can and Ferhat Yaman
#We use python3 to run the code.
from random import *
import uuid
import hashlib
import string
import random

def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def check_PoW(h):
    if h[0:6] == "000000":
        return True
    else:
        return False

def hash_me(lines):
	TxLen = 8
	transaction = "".join(lines[i*TxLen:i*TxLen+TxLen-1])
	transaction = transaction.encode()
	h = hashlib.sha3_256(transaction).hexdigest()
	return h


TxLen = 8		
prev_hash = ""
lines = list()
for i in range(0,1):
	lines.append("*** Bitcoin transaction ***\n")
	
	line = "Serial number: "
	x = uuid.uuid4().int
	line += str(x) + "\n"
	lines.append(line)
	
	if i % 2 == 0:
		lines.append("Payer: Ferhat Yaman\n")
	else:
		lines.append("Payer: Gulsum Can\n")

	line = "Payee: " + id_generator() + "\n"
	lines.append(line)

	line = "Amount: "

	y = randint(1,1000)

	line += str(y) + " Satoshi\n"

	lines.append(line)

	if i == 0:
		lines.append("Previous hash in the chain: First transaction\n")
	else:
		line = "Previous hash in the chain: " + str(prev_hash) + "\n"
		lines.append(line)
		

	line = "Nonce: "
	nonce = uuid.uuid4().int
	line += str(nonce) + "\n"
	lines.append(line)
	
	h = hash_me(lines)
	while not check_PoW(h):
		line = "Nonce: "
		nonce = uuid.uuid4().int
		line += str(nonce) + "\n"
		lines[-1] = line
		h = hash_me(lines)
		prev_hash = h
	
	line = "Proof of Work: " + str(h) + "\n"
	lines.append(line)
	print(lines[i*8:])
	
thefile = open('test.txt', 'w')
for item in lines:
	thefile.write(item)
		
	#assign prev_hash

print (lines)
