import compression as c

enc = c.Encryption()
huf = c.Huffman()
ham = c.Hamming()

enc.Encrypt('hh.txt', 'files/encrypted.txt')
huf.encode('files/encrypted.txt', 'files/huffman_encoded.txt')
ham.encode('files/huffman_encoded.txt', 'files/hamming_encoded.txt')

ham.makeError('files/hamming_encoded.txt', 'files/hamming_encoded_with_errors.txt')

ham.ErrorCorrection('files/hamming_encoded_with_errors.txt', 'files/hamming_encoded_corrected.txt')
ham.decode('files/hamming_encoded_corrected.txt', 'files/hamming_decoded.txt')
huf.decode('files/hamming_decoded.txt', 'files/huffman_decoded')
enc.Decrypt('files/huffman_decoded', 'files/decrypted')

