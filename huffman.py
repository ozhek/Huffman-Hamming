from collections import Counter
import heapq


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

    def __writeResult(self, txt):
        try:
            ans = ''
            for i in txt:
                ans += self.__codes[i]

            print(ans)
            with open('encoded_text.txt', 'w') as fil:
                fil.write(ans)

        except Exception as e:
            print("Error on writeResult", e)

    def encode(self, fileName):
        try:
            with open(fileName, 'r') as file:
                txt = file.read()
                freq = self.__getFreq(txt)

            self.__makeHeap(freq)
            self.__makeTree()
            root = heapq.heappop(self.__heap)
            self.__rootNode = root
            self.__makeCodes(root, '')
            self.__writeResult(txt)

        except Exception as e:
            print("Unknown error: ", e)

    def decode(self):
        try:
            with open('encoded_text.txt', 'r') as file:
                res = ''
                txt = file.read()
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
            print(res)
            with open('decoded_text.txt', 'w') as file:
                file.write(res)

        except Exception as e:
            print('Error in decoding', e)

    def printNodes(self):
        try:
            print(self.codes)
        except Exception as e:
            print("Unknown error: ", e)
