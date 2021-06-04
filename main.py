import compression as c
huf = c.Huffman()
ham = c.Hamming()
enc = c.Encryption()

enc.Encrypt('hah.txt', 'encrypted.txt')
huf.encode('encrypted.txt', 'huffman_encoded.txt')
ham.encode('huffman_encoded.txt', 'hamming_encoded.txt')
ham.makeError('hamming_encoded.txt', 'hamming_encoded_witherrors.txt')
ham.ErrorCorrection('hamming_encoded_witherrors.txt', 'hamming_encoded_corrected.txt')
ham.decode('hamming_encoded_corrected.txt', 'hamming_decoded.txt')
huf.decode('hamming_decoded.txt', 'huffman_decoded.txt')
enc.Decrypt('huffman_decoded.txt', 'decrypted.txt')

