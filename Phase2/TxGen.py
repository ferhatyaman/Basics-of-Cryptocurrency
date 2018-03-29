import string
import DSA
import random
import uuid
import hashlib

    
def hash_me(transaction):
    transaction = transaction.encode()
    h = hashlib.sha3_256(transaction).hexdigest()
    return h


def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
def GenSingleTx(p, q, g, alpha, beta):
    transaction = ""
    transaction += "*** Bitcoin transaction ***\n"

    line = "Serial number: "
    x = uuid.uuid4().int
    line += str(x) + "\n"
    transaction += line
    
    line = "Payer: " + id_generator() + "\n"
    transaction += line

    line = "Payee: " + id_generator() + "\n"
    transaction += line

    line = "Amount: "
    y = random.randint(1,1000)
    line += str(y) + " Satoshi\n"
    transaction += line
    
    line = "p: " + str(p) + "\n"
    transaction += line
    
    line = "q: " + str(q) + "\n"
    transaction += line
    
    line = "g: " + str(g) + "\n"
    transaction += line
    
    line = "Public Key (beta): " + str(beta) + "\n"
    transaction += line
    
    m = transaction
    
    (r, s) = DSA.SignGen(m, p, q, g, alpha, beta)
    
    line = "Signature (r): " + str(r) + "\n"
    transaction += line
    
    line = "Signature (s): " + str(s) + "\n"
    transaction += line
    
    return transaction

def testSingleTx():
    if os.path.exists('DSA_pkey.txt') == True and os.path.exists('DSA_skey.txt') == True:
        skeyFile = open('DSA_skey.txt', 'r')
        q = int(skeyFile.readline())
        p = int(skeyFile.readline())
        g = int(skeyFile.readline())
        alpha = int(skeyFile.readline())
        skeyFile.close()
        print ("Public key is read from DSA_skey.txt")

        pkeyFile = open('DSA_pkey.txt', 'r')
        lines = pkeyFile.readlines()
        beta = int(lines[3])
        pkeyFile.close()
        print ("Public key is read from DSA_pkey.txt")
        
    else:
        print ('DSA_skey.txt or DSA_pkey.txt does not exist')
        sys.exit()

    # pick a random message (string)
    TxFile = open("SingleTransaction.txt", "w")
    lines = TxFile.readlines()
    m = lines[0:9]
    print ("message: ", m)

    r = int(lines[9][15:])
    s = int(lines[10][15:])
    print ("Signature:")
    print ("r: ", r)
    print ("s: ", s)

    if DSA.SignVer(m, r, s, p, q, g, beta)==1:
        print ("Signature verifies:))")
    else:
        print ("Signature does not verify:((")
        sys.exit()
