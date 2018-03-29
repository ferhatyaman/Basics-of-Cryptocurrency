
# TxBlockFile: The name of the file that contains a block of transactions (e.g., “TransactionBlock0.txt”
# in the attachment)
# • ChainFile: The name of the file that contains proof of works for the transactions in all
# past blocks. If not exits, it is created for the first block (e.g., “LongestChain.txt” in the
# attachment)
# • PoWLen: the number of zero digits in the proof of work (typically set to six)
# • TxLen: the number lines in a transaction (it is 10 in our case)
from random import *
import uuid
import hashlib
import string
import random,os,sys

blockCount = 3 # number of link in the block chain (you can change)
TxCount = 8    # number of transactions in a block (you can change, but set it to a power of two)
PoWLen = 6     # the number of 0s in PoW (you can change)
TxLen = 10     # no of lines in a transaction (do not change)
LinkLen = 4    # no of lines in a link of the chain (do not change)

def check_PoW(h):
    if h[0:6] == "000000":
        return True
    else:
        return False

def hash_me(new_entry):
    block = new_entry
    block = block.encode()
    h = hashlib.sha3_256(block).hexdigest()
    return h
    
def genNonce():
    return uuid.uuid4().int
    
def merkleTree(TxBlockFileName):
    if os.path.exists(TxBlockFileName) == False:
        print ("Error: ", TxBlockFileName, "does not exist")
        sys.exit()
    
    TxBlockFile = open(TxBlockFileName, "r")
    lines = TxBlockFile.readlines()
    hashTree = []
    for i in range(0,TxCount):
        transaction = "".join(lines[i*TxLen:(i+1)*TxLen])
        transaction = transaction.encode()
        hashTree.append(hashlib.sha3_256(transaction).hexdigest())

    t = TxCount
    j = 0
    while(t>1):
        for i in range(j,j+t,2):
            m = hashTree[i]+hashTree[i+1]
            m = m.encode()
            hashTree.append(hashlib.sha3_256(m).hexdigest())
        j += t
        t = t>>1
    h = hashTree[2*TxCount-2]
    return h

def PoW(TxBlockFileName, ChainFileName, PoWLen, TxLen):
    BlockChainFileName = "LongestChain.txt"
    new_entry = ""
    fileExists = os.path.exists(BlockChainFileName)
    if fileExists == False:
        new_entry += "Day Zero Link in the Chain\n"
        print('File generated    ', BlockChainFileName)
    else:
        BlockChainFile = open(BlockChainFileName, "r")
        lines = BlockChainFile.readlines()
        previous_hash = lines[-1]
        new_entry += str(previous_hash)
        BlockChainFile.close()
        
    new_entry+= str(merkleTree(TxBlockFileName))+"\n"
    nonce = str(genNonce()) + "\n"
    h = hash_me(new_entry + nonce)
    while not check_PoW(h):
        nonce = str(genNonce()) + "\n"
        h = hash_me(new_entry + nonce)
    new_entry += nonce
    new_entry += str(h) + "\n"
    print('PoW generated')
    if not fileExists:
        BlockChainFile = open(BlockChainFileName, "w")
    else:
        BlockChainFile = open(BlockChainFileName, "a")
    BlockChainFile.write(new_entry)
    print(new_entry)
    BlockChainFile.close()