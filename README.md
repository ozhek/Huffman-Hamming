# Huffman

It is interpretation of huffman algorithm

Hot to use:
  As you see in main.py, we declate object of Huffman class.
  Then we use method Huffman.encode(filename) to encode, and Huffman.decode() for decoding that encoded text.
  Encoded thext will be written in encoded_text.txt file, and decoded text in decoded_text.txt file.
  Also there added hamming encoding for error checking and correction. 
  Hamming implemented as:
    For encoding: we divide encoded code for 4 bits blocks and last one doesn't matter how many bits.
    For decoding: we divide hamming encoded text for 7 bits(4 bits encodes to 7 bits, 3 redunnat bits added)
  For cheking hamming code we add some errors(Huffman.__generateErrorCodes())
  

How works Huffman encoding:
  1. Find frequency for every character.
  2. Make nodes for implementing tree.
  3. Add these nodes into heap, because at every iterate we need character with minimum frequency.
  4. Create binary tree and get root node(how it works exactly you can see in code or watch youtube).
  5. Going further by root node we apply for every leaf node some code, and finally we create map assigning for every character some code.
  6. Iterate text and rewrite it by map we created.

How works Decoding:
  1. Iterate encoded text by root node
  2. If current bit is 0 then go to the left node, otherwise go right
  3. Check if it is leaf node, if it is, write character this node is stores, and make current node root again.
  4. Do 2 and 3 until we reach end of file.
  5. Finally we get our text
 
 How we implement Hamming:
  For encoding by Hamming we use general code.
  1. Finding number of parity bits
  2. Add parity bits in indexes os 2'th power
  3. Generate matrix
  4. Find values of parity bits
  For error checking and correction:
  1. Do same as in encoding
  2. Create binary number by values of parity bits
  3. if it is 0 then no errors are finded
  4. Else error is at position of values of binary number
  
