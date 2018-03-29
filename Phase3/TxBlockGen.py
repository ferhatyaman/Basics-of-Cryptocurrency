import uuid, DSA,random

def GenTxBlock(p, q, g, count):
    whole_transaction = ""

    for i in range(count): 
        transaction = ""
        transaction += "*** Bitcoin transaction ***\n"

        line = "Serial number: "
        x = uuid.uuid4().int
        line += str(x) + "\n"
        transaction += line
        
        line = "p: " + str(p) + "\n"
        transaction += line
        
        line = "q: " + str(q) + "\n"
        transaction += line
        
        line = "g: " + str(g) + "\n"
        transaction += line

        alpha, beta = DSA.KeyGen(p,q,g)
        
        line = "Payer Public Key (beta): " + str(beta) + "\n"
        transaction += line

        alpha2, beta2 = DSA.KeyGen(p,q,g)
        line = "Payee Public Key (beta): " + str(beta2) + "\n"
        transaction += line
        
        line = "Amount: "
        y = random.randint(1,1000)
        line += str(y) + " Satoshi\n"
        transaction += line
        
        m = transaction
        
        (r, s) = DSA.SignGen(m, p, q, g, alpha, beta)
        
        line = "Signature (r): " + str(r) + "\n"
        transaction += line
        
        line = "Signature (s): " + str(s) + "\n"
        transaction += line

        whole_transaction += transaction

    return whole_transaction