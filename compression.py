from collections import Counter
import heapq
from functools import reduce
import random
import math


class Huffman:

    def __init__(self):
        self.__heap = []
        self.__rootNode = None
        self.__codes = {}

    class Node:

        def __init__(self, char, freq):
            self.char = char
            self.freq = freq
            self.left = None
            self.right = None

        def __lt__(self, other):
            return self.freq < other.freq

        def __eq__(self, other):
            if not other:
                return False
            if not isinstance(other, Node):
                return False
            return self.freq == other.freq

        def __str__(self):
            return self.char

    def __getFreq(self, txt):
        prob = Counter()
        siz = len(txt)
        for i in txt:
            prob[i] += 1 / siz
        return prob

    def __makeHeap(self, freq):
        try:
            for k in freq:
                node = self.Node(k, freq[k])
                heapq.heappush(self.__heap, node)
        except Exception as e:
            print("Unknown error in makeHeap: ", e)

    def __makeTree(self):
        try:
            while len(self.__heap) > 1:
                node1 = heapq.heappop(self.__heap)
                node2 = heapq.heappop(self.__heap)

                merged = self.Node(None, node1.freq + node2.freq)
                merged.left = node1
                merged.right = node2
                heapq.heappush(self.__heap, merged)
        except Exception as e:
            print("Unknown error in makeTree: ", e)

    def __makeCodes(self, node, cd):
        try:
            if node.char is not None:
                self.__codes[node.char] = cd
            else:
                self.__makeCodes(node.left, cd + '0')
                self.__makeCodes(node.right, cd + '1')
        except Exception as e:
            print("Unknown error on makeCodes", e)

    def encode(self, readFilePath, writeFilePath):
        try:
            with open(readFilePath, 'r') as file:
                txt = file.read()

            freq = self.__getFreq(txt)
            self.__makeHeap(freq)
            self.__makeTree()
            root = heapq.heappop(self.__heap)
            self.__rootNode = root
            
            if root.char is None:
                self.__makeCodes(root, '')
            else:
                self.__codes[root.char] = '0'

            ans = ''
            for i in txt:
                ans += self.__codes[i]

            
            with open(writeFilePath, 'w') as fil:
                fil.write(ans)

        except Exception as e:
            print("Unknown error: ", e)

    def decode(self, readFilePath, writeFilePath):
        try:
            with open(readFilePath, 'r') as file:
                txt = file.read()

            res = ''
            root = self.__rootNode
            cur = root
            for code in txt:
                if code == '0':
                    if cur.char is not None:
                        res += cur.char
                        cur = root

                    if cur.left:
                        cur = cur.left
                else:
                    if cur.char is not None:
                        res += cur.char
                        cur = root
                    
                    if cur.right:
                        cur = cur.right
            res += cur.char
            with open(writeFilePath, 'w') as file:
                file.write(res)

        except Exception as e:
            print('Error in huffman decoding', e)
class Hamming:


    def makeError(self, readFilePath, writeFilePath): #makinging an error for hamming encoding
        with open(readFilePath, 'r') as file:
            txt = file.read()

        res = ''
        for i in range(0, len(txt), 7):
            x = list(txt[i:(i + 7)])
            l = random.randint(0, len(x))
            if l != len(x):
                x[l] = str(1 - int(x[l]))
            res += ''.join(map(str, x))
        with open(writeFilePath, 'w') as file:
            file.write(res)


    def __generateMatrix(self, m , r, revers=False):
        matrix = []
        cur = 0
        for i in range(m + r):
            cur = cur + 1
            binar = bin(cur)[2:]
            while len(binar) != r:
                binar = '0' + binar
            if revers:
                matrix.append(list(reversed(binar)))
            else:
                matrix.append(list(binar))
        return matrix

    def __generateParityBits(self, data, matrix): #generating redunant bits using matrix
        c = 0
        pbits = []
        while 2 ** c < len(data):
            ans = 0
            for i in range(len(data)):
                ans += int(data[i]) * int(matrix[i][c])
            pbits.append(ans % 2)
            c += 1
        return pbits

    def __GenerateHamming(self, bits):
        try:
            data = list(bits)
            m = len(data)
            c, j, r = 0, 0, 0
            result = []
            while m + r + 1 > pow(2, r): # Calculating number of redunant bits
                r += 1

            if r == 0:
                ans = ''.join(map(str, data))
            else:
                for i in range(r + m): #Adding redunant bits
                    p = (2 ** c)
                    if (p == (i + 1)):
                        result.append(0)
                        c = c + 1
                    else:
                        result.append(int(data[j]))
                        j = j + 1

                matrix = self.__generateMatrix(m, r, True) #making matrix
                pbits = self.__generateParityBits(result, matrix) #finding values of parity bits
                for i in range(r):
                    result[2**i - 1] = pbits[i] #assigning parity bits

                ans = ''.join(map(str, result))# converting to string
            return ans
        except Exception as e:
            print("Unknown error on generating hamming code: ", e)

    def encode(self, readFilePath, writeFilePath):
        try:
            with open(readFilePath, 'r') as fil:
                txt = fil.read()


            res = ''
            for i in range(0, len(txt), 4):
                res += self.__GenerateHamming(txt[i:(i + 4)])

            with open(writeFilePath, 'w') as fil:
                fil.write(res)

            return res
        except Exception as e:
            print('hamming encode: ', e)

    def __HammingBlockCorrection(self, startIndex, data):
        try:
            m = len(data)
            r = 0
            while 2**r < m: # getting value of r(redunant bits)
                r += 1
            # getting matrix
            matrix = self.__generateMatrix(m-r, r)

            pbits = self.__generateParityBits(data, matrix)

            syndrome = reduce(lambda x,y: str(x)+str(y), pbits)# position of error as binary code
            error = int(syndrome,2) # converting binary to decimal

            if error != 0:
                data[error-1] = str(1 - int(data[error-1]))

            ans = ''.join(map(str, data))
            return ans
        except Exception as e:
            print("Unknown error at hamming decode", e)

    def ErrorCorrection(self, readFilePath, writeFilePath):
        try:
            with open(readFilePath, 'r') as file:
                txt = file.read()
                txt = txt.strip()

            res = ''
            for i in range(0, len(txt), 7):
                x = list(txt[i:(i + 7)])
                cur = self.__HammingBlockCorrection(i, x)
                res += cur


            with open(writeFilePath, 'w') as file:
                file.write(res)
        except Exception as e:
            print("HammingErrorCorrection unknown error: ", e)


    def decode(self, readFilePath, writeFilePath ):
        try:
            with open(readFilePath, 'r') as file:
                txt = file.read()

            final = []
            x = []
            for i in range(0, len(txt), 7):
                x = list(txt[i:(i + 7)])
                c = 0
                for j in range(len(x)):
                    if j + 1!= pow(2,c) :
                        final += str(x[j])
                    else:
                        c += 1

            res = ''.join(map(str, final))

            
            with open(writeFilePath, 'w') as file:
                file.write(res)
        except Exception as e:
            print("Error at huffman decode", e)
class Encryption:

    def __init__(self):
        self.public, self.private = self.__generateKeys()

    def __generateKeys(self):
        primes = [i for i in range(17, 500) if self.__is_prime(i)]
        p = random.choice(primes)
        q = p
        while (q == p):
            q = random.choice(primes)

        n,r = (p * q, (p - 1) * (q - 1))
        e = random.choice([i for i in range(1, 1000) if math.gcd(i, r) == 1])
        d = self.__mult_inv(e, r)
        return ((e, n), (d, n))

    def __is_prime(self, num):
        if num == 2:
            return True
        if num < 2 or num % 2 == 0:
            return False
        for n in range(3, int(num ** 0.5) + 2, 2):
            if num % n == 0:
                return False
        return True

    def __eugcd(self, e, r):
        for i in range(1, r):
            while (e != 0):
                a, b = r // e, r % e
                r = e
                r = b

    def __eea(self, a, b):
        if a % b == 0:
            return (b, 0, 1)

        g, s, t = self.__eea(b, a % b)
        s = s - ((a // b) * t)
        return (g, t, s)

    def __mult_inv(self, e, r):
        g, s, _ = self.__eea(e, r)

        if g == 1:
            return s % r

    def Encrypt(self, readFilePath, writeFilePath):
        try:
            with open(readFilePath, 'r') as filt:
                plaintext = filt.read()

            e,n = self.public
            ans = [(ord(char) ** e) % n for char in plaintext]
            res = ''
            for i in ans:
                res += chr(i)

            with open(writeFilePath, 'w') as file:
                file.write(res)

        except Exception as e:
            print(e)

    def Decrypt(self, readFilePath, writeFilePath):
        try:
            with open(readFilePath, 'r') as filt:
                ciphertext = filt.read()

            d,n = self.private

            ans = [(ord(char) ** d) % n for char in ciphertext]
            res = ''
            for i in ans:
                res += chr(i)

            with open(writeFilePath, 'w') as file:
                file.write(res)
        except Exception as e:
            print(e)
