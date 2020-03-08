import sys


class ShiftCipher:
    # ord() is used to convert char to ascii
    # chr() is used to convert ascii to char

    def encrypt(self, inp, out, key):
        key %= 26
        for line in inp:
            outLine = ""
            for char in line:
                if char == "\n":
                    continue
                if char == ' ' or char.isalpha() is False:
                    outLine += char
                    continue
                isUpper = False
                if char.isupper():
                    isUpper = True
                char = char.lower()
                newChar = (ord(char) - ord('a') + key) % 26
                newChar = chr(newChar + ord('a'))
                if isUpper:
                    newChar = newChar.upper()
                outLine += newChar
            outLine += "\n"
            out.write(outLine)

    def decrypt(self, inp, out, key):
        key %= 26
        for line in inp:
            outLine = ""
            for char in line:
                if char == "\n":
                    continue
                if char == ' ' or char.isalpha() is False:
                    outLine += char
                    continue
                isUpper = False
                if char.isupper():
                    isUpper = True
                char = char.lower()
                newChar = (ord(char) - ord('a') - key + 26) % 26
                newChar = chr(newChar + ord('a'))
                if isUpper:
                    newChar = newChar.upper()
                outLine += newChar
            outLine += "\n"
            out.write(outLine)


class AffineCipher:

    def encrypt(self, inp, out, a, b):
        if self.isCoprimes(a, 26) is False:
            print("a, m(26) must be coprimes!")
            return
        for line in inp:
            outLine = ""
            for char in line:
                if char == "\n":
                    continue
                if char == ' ' or char.isalpha() is False:
                    outLine += char
                    continue
                isUpper = False
                if char.isupper():
                    isUpper = True
                char = char.lower()
                newChar = (ord(char) - ord('a'))
                newChar = (newChar * a + b) % 26
                newChar = chr(newChar + ord('a'))
                if isUpper:
                    newChar = newChar.upper()
                outLine += newChar
            outLine += "\n"
            out.write(outLine)

    def decrypt(self, inp, out, a, b):
        mInverse = self.getMultiplicativeInverse(a)
        if mInverse == -1:
            print("a has no multiplicative inverse!")
            return
        for line in inp:
            print(line)
            outLine = ""
            for char in line:
                if char == "\n":
                    continue
                if char == ' ' or char.isalpha() is False:
                    outLine += char
                    continue
                isUpper = False
                if char.isupper():
                    isUpper = True
                char = char.lower()
                newChar = (ord(char) - ord('a'))
                newChar = (mInverse * (newChar - b)) % 26
                newChar = chr(newChar + ord('a'))
                if isUpper:
                    newChar = newChar.upper()
                outLine += newChar
            outLine += "\n"
            out.write(outLine)

    def getMultiplicativeInverse(self, a):
        for i in range(1, 26):
            result = (i * a) % 26
            if result == 1:
                return i
        return -1

    def isCoprimes(self, a, m):
        for i in range(2, m + 1):
            if a % i == 0 and m % i == 0:
                return False
        return True


class VigenereCipher:

    def encrypt(self, inp, out, key):
        key = key.lower()
        keyLn = len(key)
        charCount = 0
        for line in inp:
            outLine = ""
            for char in line:
                keyChar = key[charCount % keyLn]
                charCount += 1
                if char == "\n":
                    continue
                if char == ' ' or char.isalpha() is False:
                    outLine += char
                    continue
                isUpper = False
                if char.isupper():
                    isUpper = True
                char = char.lower()
                newChar = (ord(char) - ord('a'))
                keyChar = (ord(keyChar) - ord('a'))
                newChar = (newChar + keyChar) % 26
                newChar = chr(newChar + ord('a'))
                if isUpper:
                    newChar = newChar.upper()
                outLine += newChar
            outLine += "\n"
            out.write(outLine)

    def decrypt(self, inp, out, key):
        key = key.lower()
        keyLn = len(key)
        charCount = 0
        for line in inp:
            outLine = ""
            for char in line:
                keyChar = key[charCount % keyLn]
                charCount += 1
                if char == "\n":
                    continue
                if char == ' ' or char.isalpha() is False:
                    outLine += char
                    continue
                isUpper = False
                if char.isupper():
                    isUpper = True
                char = char.lower()
                keyChar = (ord(keyChar) - ord('a'))
                newChar = (ord(char) - ord('a') - keyChar + 26) % 26
                newChar = chr(newChar + ord('a'))
                if isUpper:
                    newChar = newChar.upper()
                outLine += newChar
            outLine += "\n"
            out.write(outLine)


def main():
    inFile = None
    outFile = None
    argCount = len(sys.argv)
    args = list(sys.argv)
    pars = list()
    # The following code validates the passed arguments
    # print(argCount)
    # print(args)
    if argCount < 6:  # Python File, Cypher, Enc/Dec, Inp, Out, Parameter(s)
        print("Please provide all the required the parameters!")
        return
    elif args[1] not in ["shift", "affine", "vigenere"]:
        print("Cypher name is not valid!")
        return
    elif args[2] not in ['encrypt', 'decrypt']:
        print("Please specify operation type enc/ dec")
        return
    try:  # Check if input file exists
        inFile = open(args[3])
    except FileNotFoundError:
        print("Input file doesn't not exits")
        return
    try:
        outFile = open(args[4])
        con = "-"
        while con != "y" and con != "n":
            con = input("output file already exists. override ? (y/ n) ")
        if con == "n":
            print("Closing!")
            return
        else:
            outFile.close()
            outFile = outFile = open(args[4], "w")
    except FileNotFoundError:
        outFile = open(args[4], "w")
        print("New File Created")
    if args[1] == "shift":
        shiftCipher = ShiftCipher()
        if argCount > 6:
            print("Only one extra parameter (key) is required")
            return
        try:
            args[5] = int(args[5])
        except ValueError:
            print("Check the key is a single integer!")
            return
        if args[2] == 'encrypt':
            shiftCipher.encrypt(inFile, outFile, args[5])
        else:
            shiftCipher.decrypt(inFile, outFile, args[5])
    elif args[1] == 'affine':
        affineCipher = AffineCipher()
        if argCount == 6:
            print("Affine Cipher requires two parameters a, b!")
            return
        try:
            args[5] = int(args[5])
            args[6] = int(args[6])
        except ValueError:
            print("a, b must be integers!")
            return
        if args[2] == 'encrypt':
            affineCipher.encrypt(inFile, outFile, args[5], args[6])
        else:
            affineCipher.decrypt(inFile, outFile, args[5], args[6])
    else:
        vigenereCipher = VigenereCipher()
        if argCount > 6:
            print("Vigenere Cipher only requires one parameter (Key)")
            return
        if args[5].isalpha() is False:
            print("The key must be all english characters only")
            return
        if args[2] == 'encrypt':
            vigenereCipher.encrypt(inFile, outFile, args[5])
        else:
            vigenereCipher.decrypt(inFile, outFile, args[5])


if __name__ == '__main__':
    main()
