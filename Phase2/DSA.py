# -- coding: utf-8 --
import hashlib
import random
from  pyprimes import isprime



def subGroupGenerator(p, q):
  e = (p-1) // q 
  g = 1
  while g == 1:
  	h = random.randint(0, p-1)
  	g = pow(h,e,p)
  return g

    
def egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
    gcd = b
    return gcd, x, y

def modinv(a, m):
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        return None  # modular inverse does not exist
    else:
        return x % m

#Post-condition: returns public parameters q,p,g
def DL_Param_Generator(small_bound, large_bound):
    L = 2048
    N = 256
    seedlen = N 
    q = 4
    U = 2
    domain_parameter_seed = 0
    while not isprime(q):
        # domain_parameter_seed = number.getPrime(seedlen)
        domain_parameter_seed =int(random.getrandbits(seedlen))
        U = hash(domain_parameter_seed % pow(2, N-1))
        q = pow(2, N-1) + U + 1 - (U%2)

    # print("q:", q)

    offset = 1 
    V = list()
    for counter in range(0, 4*L-1):
        outlen = (U.bit_length())
        n = L // outlen -1
        b = L - 1 - (n*outlen)
        for j in range(0, n):
            V.append(hash((domain_parameter_seed+offset+j)%pow(2, seedlen)))
        W = 0 
        for i in range(0,n-1):
            W += V[i] * pow(2, (i) * outlen)
        W += (V[-1] % pow(2,b)) * pow(2, n * outlen)
        X = W + pow(2, L-1)
        c = X % (2*q)
        p = X - (c-1)
        if isprime(p):
            g = subGroupGenerator(p,q)
            return q,p,g
        offset += n + 1
    return (0,0,0)



#Pre-condition: it takes q, p, g as parameter
#Prodecure: A user picks a random secret key 0 < α < q and computes the public key β = gα mod p.
#Post-condition: returns key tuple as (alpha, beta)
def KeyGen(p, q, g):
    alpha = random.randint(1,q)
    beta = pow(g,alpha,p)
    return alpha, beta

# Pre-condition: takes message, secret key(alfa), q, p and genrator(g)
# Post-condition: returns signature tuple as (r,s)
def SignGen(message, p, q, g, alpha, beta):
    message = message.encode()
    h = int(hashlib.sha3_256(message).hexdigest(), 16)
    h = h % q
    k = random.randint(1, q-1)
    r = pow(g, k, p) % q
    s = (alpha * r + k * h) % q
    return (r, s)

#Pre-condition: takes message, signature tuple(r,s), q, p, g and public key(beta)
#Post-condtion: if condition holds it returns verification true, otherwise false
def SignVer(message, r, s, p, q, g, beta):
    message = message.encode()
    h = int(hashlib.sha3_256(message).hexdigest(), 16)
    h = h % q
    v = modinv(h, q)
    z_one = (s*v) % q
    z_two = ((q - r) * v) % q
    u = (pow(g, z_one, p) * pow(beta, z_two, p)) % p

    if r == (u % q):
        return 1
    else:
        return 0


