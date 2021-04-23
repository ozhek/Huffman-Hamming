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
        self.heap = []
        self.codes = {}

    def getFreq(self, txt):  # gets probability of each character into Counter object
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

    def makeHeap(self, freq):
        try:
            for k in freq:
                node = Node(k, freq[k])
                heapq.heappush(self.heap, node)
        except Exception as e:
            print("Unknown error in makeHeap: ", e)

    def makeTree(self):
        try:
            while len(self.heap) > 1:
                node1 = heapq.heappop(self.heap)
                node2 = heapq.heappop(self.heap)

                merged = Node(None, node1.freq + node2.freq)
                merged.left = node1
                merged.right = node2
                heapq.heappush(self.heap, merged)
        except Exception as e:
            print("Unknown error in makeTree: ", e)

    def makeCodes(self, node, cd):
        try:
            if node.char is not None:
                self.codes[node.char] = cd
            else:
                self.makeCodes(node.left, cd + '0')
                self.makeCodes(node.right, cd + '1')
        except Exception as e:
            print("Unknown error on makeCodes", e)

    def writeResult(self, txt):
        try:
            ans = ''
            for i in txt:
                ans += self.codes[i]
            with open('result.txt', 'w') as fil:
                fil.write(ans)

        except Exception as e:
            print("Error on writeResult", e)

    def encode(self, fileName):
        try:
            with open(fileName, 'r') as file:
                txt = file.read()
                freq = self.getFreq(txt)

            self.makeHeap(freq)
            self.makeTree()
            root = heapq.heappop(self.heap)
            self.makeCodes(root, '')
            self.writeResult(txt)
        except Exception as e:
            print("Unknown error: ", e)

    def printNodes(self):
        try:
            print(self.codes)
        except Exception as e:
            print("Unknown error: ", e)
