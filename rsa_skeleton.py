import random

#Names: Kailey Totland and Skye Jorgensen
#HW3
#Pledge: I pledge my honor that I have abided by the Stevens Honor System.

# test constants
test_p = 23
test_q = 47
test_e =  35
test_d = 347
message = "Hello world!"

def calc_n(p, q):
    # do not modify!
    return p * q

def calc_phi(p, q):
    # do not modify!
    return (p - 1) * (q - 1)

def modexp(b, e, m):
    # returns b^e % m efficiently
    # use the binary modular exponentiation algorithm explained in the lab slides
    # Complete this part during the lab
    
    if m == 1:
        return 0
    
    result = 1
    b = b % m
    
    while e > 0:
        if e % 2 == 1:
            result = (result * b) % m
        e = e >> 1  # Use right shift for division by 2
        b = (b * b) % m
    
    return result



def RSA_enc(plaintext, key):
    # key should be a tuple (n, e)
    # the ord() function will be useful here
    # we recommend extracting the components of the key from the tuple for efficiency purposes
    # return a list of integers
    n, e = key
    plain_ascii = []
    for i in range(len(plaintext)):
        charact = plaintext[i]
        plain_ascii.append(ord(charact))
    
    cipher = []
    for i in range(len(plain_ascii)):
        charact = plain_ascii[i]
        cipher.append(modexp(charact, e, n))

    return cipher


def RSA_dec(ciphertext, key):
    # key should be a tuple (n, e)
    # the chr() function will be useful here
    # we recommend extracting the components of the key from the tuple for efficiency purposes
    # return a string
    n, e = key
    decrypt_ascii = []
    for i in range(len(ciphertext)):
        charact = ciphertext[i]
        decrypt_ascii.append(modexp(charact, e, n))
    
    plain = []
    for i in range(len(decrypt_ascii)):
        charact = decrypt_ascii[i]
        plain.append(chr(charact))
    
    final = ''.join(plain)
    return final


def test():
    # do not modify!
    n       = calc_n(test_p, test_q)
    private = [n, test_d]
    public  = [n, test_e]
    
    print("Public key:",public)
    print("Private key:",private)
    
    ciphertext = RSA_enc(message,public)
    plaintext  = RSA_dec(ciphertext,private)

    print("Original message:",message)
    print("Encrypted message:",ciphertext)
    print("Decrypted message:",plaintext)

# === Below this comment is the portions of this assignment that contribute to HW 2 ===

def egcd(b, n):
    # runs the extended Euclidean algorithm on b and n
    # returns a triple (g, x, y) s.t. bx + ny = g = gcd(b, n)
    # review the extended Euclidean algorithm on Wikipedia
    # Complete for HW 2 extra credit
    s = 0
    old_s = 1
    r = n
    old_r = b

    while r != 0:
        quot = old_r // r
        (old_r, r) = (r, old_r - quot * r)
        (old_s, s) = (s, old_s - quot * s)

    if b != 0:
        bezout_t = (old_r - old_s * b) // n
    else:
        bezout_t = 0

    return old_r, old_s, bezout_t


def mulinv(e, n):
    # returns the multiplicative inverse of e in n
    # make use of the egcd above
    # Complete for HW 2 extra credit
    g, x, y = egcd(e, n)
    if g != 1:
        print("doesn’t exist")
        return
    else:
        return (x % n + n) % n

def checkprime(n, size):
    # do not modify!
    # determine if a number is prime
    if n % 2 == 0 or n % 3 == 0: return False
    i = 0

    # fermat primality test, complexity ~(log n)^4
    while i < size:
        if modexp(random.randint(1, n - 1), n - 1, n) != 1: return False
        i += 1

    # division primality test
    i = 5
    while i * i <= n:
        if n % i == 0: return False
        i += 2
        if n % i == 0: return False
        i += 4
    return True

def primegen(size):
    # do not modify!
    # generates a <size> digit prime
    if(size == 1): return random.choice([2, 3, 5, 7])
    lower = 10 ** (size - 1)
    upper = 10 ** size - 1
    p = random.randint(lower, upper)
    p -= (p % 6)
    p += 1
    if p < lower: p += 6
    elif p > upper: p -= 6
    q = p - 2
    while p < upper or q > lower:
        if p < upper:
            if checkprime(p, size): return p
            p += 4
        if q > lower:
            if checkprime(q, size): return q
            q -= 4
        if p < upper:
            if checkprime(p, size): return p
            p += 2
        if q > lower:
            if checkprime(q, size): return q
            q -= 2
        

def keygen(size):
    # generate a random public/private key pair
    # size is the digits in the rsa modulus, approximately. must be even, >2
    # return a tuple of tuples, [[n, e], [n, d]]
    assert(size % 2 == 0 and size > 2) # keep this line!

    p = primegen(size // 2)
    q = primegen(size // 2)

    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randint(2, phi - 1)
    while egcd(e, phi)[0]!= 1:
        e = random.randint(2, phi - 1)

    d = mulinv(e, phi)

    public_key = [n, e]

    private_key = [n, d]

    return [public_key, private_key]

def customkeytest(text, size):
    keypair = keygen(size)
    
    print("Public key:",keypair[0])
    print("Private key:",keypair[1])
    
    ciphertext = RSA_enc(text,keypair[0])
    plaintext  = RSA_dec(ciphertext,keypair[1])

    print("Original message:",text)
    print("Encrypted message:",ciphertext)
    print("Decrypted message:",plaintext)
