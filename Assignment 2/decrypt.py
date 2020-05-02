import sys
from struct import pack, unpack


# The F doesn't not change from encryption to decryption
def F(w):
    return ((w * 31337) ^ (w * 1337 >> 16)) % 2 ** 32


def decrypt(block):
    # The 2 steps of encryption to reverse
    # a, b, c, d = b ^ F(a | F(c ^ F(d)) ^ F(a | c) ^ d), c ^ F(a ^ F(d) ^ (a | d)), d ^ F(a | F(a) ^ a), a ^ 31337 ( 1 )
    # a, b, c, d = c ^ F(d | F(b ^ F(a)) ^ F(d | b) ^ a), b ^ F(d ^ F(a) ^ (d | a)), a ^ F(d | F(d) ^ d), d ^ 1337 ( 2 )
    # Decryption goes from bottom to top

    a, b, c, d = unpack("<4I", block)
    for i in xrange(32):
        # Reversing the 2nd step of encryption
        aOld = a
        d = d ^ 1337  # dOld = d ^ 1337
        a = c ^ (F(d | F(d) ^ d))  # cOld = a ^ F(d | F(d) ^ d)
        b = b ^ (F(d ^ F(a) ^ (d | a)))  # bOld = b ^ F(d ^ F(a) ^ (d | a))
        c = aOld ^ (F(d | F(b ^ F(a)) ^ F(d | b) ^ a))  # aOld = c ^ F(d | F(b ^ F(a)) ^ F(d | b) ^ a)

        # Reversing the 1st step of encryption
        aOld = a
        a = d ^ 31337  # dOld = a ^ 31337
        d = c ^ (F(a | F(a) ^ a))  # cOld = d ^ F(a | F(a) ^ a)
        c = b ^ (F(a ^ F(d) ^ (a | d)))  # bOld = c ^ F(a ^ F(d) ^ (a | d))
        b = aOld ^ (F(a | F(c ^ F(d)) ^ F(a | c) ^ d))  # aOld = b ^ F(a | F(c ^ F(d)) ^ F(a | c) ^ d)
    return pack("<4I", a, b, c, d)


ct = open("flag.enc").read()
pt = "".join(decrypt(ct[i:i + 16]) for i in xrange(0, len(ct), 16))
open("flag" + ".dec", "w").write(pt)
