from collections import Counter
import heapq
from functools import reduce
from random import randint


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

class Huffman:

    def __init__(self):
        self.__heap = []
        self.__rootNode = None
        self.__codes = {}

    def __getFreq(self, txt):  # gets probability of each character into Counter object
        try:
            prob = Counter()
            siz = len(txt)
            for i in txt:
                prob[i] += 1 / siz
            return prob
        except OSError as e:
            print("Could not open/read file")
        except Exception as e:
            print("Unknown error: ", e)


    def __makeHeap(self, freq):
        try:
            for k in freq:
                node = Node(k, freq[k])
                heapq.heappush(self.__heap, node)
        except Exception as e:
            print("Unknown error in makeHeap: ", e)

    def __makeTree(self):
        try:
            while len(self.__heap) > 1:
                node1 = heapq.heappop(self.__heap)
                node2 = heapq.heappop(self.__heap)

                merged = Node(None, node1.freq + node2.freq)
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
                return ans

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
                result[2**i - 1] = pbits[i] #assigning perity bits

            ans = ''.join(map(str, result))# converting to string
            return ans
        except Exception as e:
            print("Unknown error on generating hamming code: ", e)

    def __writeResult(self, txt):
        try:
            ans = ''
            for i in txt:
                ans += self.__codes[i]

            with open('encoded_text.txt', 'w') as fil:
                fil.write(ans)
            print("Huffman encoded: ", ans)
            m = len(ans)

            res = ''
            for i in range(0, len(ans),4):
                res += self.__GenerateHamming(ans[i:(i+4)])

            print("Hamming encoded: ", res)
            with open('hamming.txt', 'w') as fil:
                fil.write(res)

        except Exception as e:
            print("Error on writeResult", e)

    def encode(self, fileName):
        try:
            with open(fileName, 'r') as file:
                txt = file.read()
                print("Text: ", txt)
                freq = self.__getFreq(txt)

            self.__makeHeap(freq)
            self.__makeTree()
            root = heapq.heappop(self.__heap)
            self.__rootNode = root
            self.__makeCodes(root, '')
            self.__writeResult(txt)
        except Exception as e:
            print("Unknown error: ", e)

    def __makeError(self): #makinging an error for hamming encoding
        with open('hamming.txt', 'r') as file:
            txt = file.read()
            txt = txt.strip()
        res = ''
        for i in range(0, len(txt), 7):
            x = list(txt[i:(i + 7)])
            l = randint(0, len(x))
            if l != len(x):
                x[l] = str(1 - int(x[l]))
            res += ''.join(map(str, x))
        print("Hamming encoded with errors: ", res)
        with open('WithErrors.txt', 'w') as file:
            file.write(res)

    def decode(self):
        try:
            self.__makeError()
            self.__HammingErrorCorrection()
            self.__HammingToHuffman()

            with open('hamming_decoded.txt', 'r') as file:
                txt = file.read()

            res = ''
            root = self.__rootNode
            cur = root
            for code in txt:
                if code == '0':
                    if cur.char is not None:
                        res += cur.char
                        cur = root

                    cur = cur.left
                else:
                    if cur.char is not None:
                        res += cur.char
                        cur = root
                    cur = cur.right
            res += cur.char
            print('Decoded text:', res)
            with open('decoded_text.txt', 'w') as file:
                file.write(res)

        except Exception as e:
            print('Error in decoding', e)

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

    def __HammingErrorCorrection(self):
        try:
            # Error correcting of hamming
            with open('WithErrors.txt', 'r') as file:
                txt = file.read()
                txt = txt.strip()

            res = ''
            for i in range(0, len(txt), 7):
                x = list(txt[i:(i + 7)])
                cur = self.__HammingBlockCorrection(i, x)
                res += cur

            print("Corrected hamming encoded text", res)

            with open('corrected_hamming.txt', 'w') as file:
                file.write(res)
        except Exception as e:
            print("HammingErrorCorrection unknown error: ", e)

    def __HammingToHuffman(self):
        try:
            with open('corrected_hamming.txt', 'r') as file:
                txt = file.read()
                txt = txt.strip()

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
            print("Gained Huffman code:", res )

            with open('hamming_decoded.txt', 'w') as file:
                file.write(res)
        except Exception as e:
            print("Error at hamming to huffman", e)

