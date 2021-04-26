# Huffman

It is interpretation of huffman algorithm

Hot to use:
  As you see in main.py, we declate object of Huffman class.
  Then we use method Huffman.encode(filename) to encode, and Huffman.decode() for decoding that encoded text.
  Encoded thext will be written in encoded_text.txt file, and decoded text in decoded_text.txt file.
  
How works encoding:
  First of all, we find probabilities of each unique symbol,
  then we save this probabilities to min heap,
  we use min heap to create huffman tree,
  next step is creating dictionary with codes,
  then just writing result

How works decoding:
  We just use huffman tree.

