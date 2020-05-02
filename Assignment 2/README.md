# Assignment #2

The Assignment is to solve this problem [GenFei](https://cybertalents.com/challenges/cryptography/genfei) on [CyberTalents](https://cybertalents.com/).<br>
The task is to decrypt the file flag.enc given the encryption algorithm contained in encrypt.py. The solution is contained in decrypt.py. <br>
Below is the submission proof in my profile [MuKassab](https://cybertalents.com/members/MuKassab/profile)
![Submission Proof](imgs/submission.PNG)

## Thought Process
First of all we note that we don't need to change anything in the F(w) function as it should be the same in both enc/dec. <br>
Now we can analyze the encryption code below

```
# Hashes(#) are appended to text until it's length is divisible by 16.

def encrypt(block):
    # Each 16 letters can converted to 4 unsigned integers and then stored in a, b, c, d.
    a, b, c, d = unpack("<4I", block)
    
    # The network is applied 32 rounds
    for rno in xrange(32):
        a, b, c, d = b ^ F(a | F(c ^ F(d)) ^ F(a | c) ^ d), c ^ F(a ^ F(d) ^ (a | d)), d ^ F(a | F(a) ^ a), a ^ 31337 # (st. 1)
        a, b, c, d = c ^ F(d | F(b ^ F(a)) ^ F(d | b) ^ a), b ^ F(d ^ F(a) ^ (d | a)), a ^ F(d | F(d) ^ d), d ^ 1337 # (st. 2)
    # After the encryption is done the result is again packed into 16 charachters (most likely in unreadable human form)
    return pack("<4I", a, b, c, d)
```

Now that we have a general idea of how the encryption works we can analyze both encryption lines and we will start with the 2nd one as decryption is applied from bottom to top. <br>

```
a, b, c, d = c ^ F(d | F(b ^ F(a)) ^ F(d | b) ^ a), b ^ F(d ^ F(a) ^ (d | a)), a ^ F(d | F(d) ^ d), d ^ 1337 # (st. 2)
# let's convert this to a more readable form
# a = c ^ F(d | F(b ^ F(a)) ^ F(d | b) ^ a)
# b = b ^ F(d ^ F(a) ^ (d | a))
# c = a ^ F(d | F(d) ^ d)
# d =  d ^ 1337  ---> We can easily restore "d" value from this by applying the XOR op. again.
# c only depends on d and we have that value c 
# then from c = a ^ F(d | F(d) ^ d) we get a = c ^ F(d | F(d) ^ d) (now we have d, a)
# using the same method from a = c ^ F(d | F(b ^ F(a)) ^ F(d | b) ^ a) we get
# b = b ^ F(d ^ F(a) ^ (d | a)) (now we have d, a, b)
# lastly from a = c ^ F(d | F(b ^ F(a)) ^ F(d | b) ^ a) we get c = a ^ F(d | F(b ^ F(a)) ^ F(d | b) ^ a)
```

Again we can apply the same thinking to reverse the 1st line in the code and you can find the equations in the decrypt.py file.
