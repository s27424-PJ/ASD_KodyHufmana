from collections import Counter

class HuffmanNode:
    def __init__(self, char=None, freq=None):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

def extract_min(Q):
    build_min_heap(Q)
    return Q.pop(0)

def insert(Q, node):
    Q.append(node)

def min_heapify(A, heapsize, i):
    l = 2 * i + 1
    r = 2 * i + 2
    if l < heapsize and A[l].freq < A[i].freq:
        smallest = l
    else:
        smallest = i
    if r < heapsize and A[r].freq < A[smallest].freq:
        smallest = r
    if i != smallest:
        A[i], A[smallest] = A[smallest], A[i]
        min_heapify(A, heapsize, smallest)

def build_min_heap(A):
    heapsize = len(A)
    for i in range(heapsize // 2 - 1, -1, -1):
        min_heapify(A, heapsize, i)

def huffman(text):
    character_counts = count_characters(text)
    Q = [HuffmanNode(char, freq) for char, freq in character_counts.items()]
    n = len(Q)
    huffman_codes = {}

    for i in range(1, n):
        x = extract_min(Q)
        y = extract_min(Q)
        z = HuffmanNode()
        z.left = x
        z.right = y
        z.freq = x.freq + y.freq
        insert(Q, z)

    root = extract_min(Q)

    def generate_codes(node, code=''):
        if node:
            if node.char is not None:
                huffman_codes[node.char] = code
            generate_codes(node.left, code + '0')
            generate_codes(node.right, code + '1')

    generate_codes(root)

    return huffman_codes

def count_characters(text):
    return Counter(text)

def encode_with_huffman(text):
    huffman_codes = huffman(text)
    print("Huffman codes:")
    for char, code in sorted(huffman_codes.items()):
        print(f"{char}: {code}")

    encoded_text = ''.join(huffman_codes[char] for char in text)
    return encoded_text

def decode_with_huffman(encoded_text, huffman_codes):
    reverse_codes = {code: char for char, code in huffman_codes.items()}
    decoded_text = ""
    code = ""
    for bit in encoded_text:
        code += bit
        if code in reverse_codes:
            decoded_text += reverse_codes[code]
            code = ""
    return decoded_text

def encrypt_with_huffman(input_file, output_file):
    with open(input_file, 'r') as f:
        text = f.read()

    huffman_codes = huffman(text)
    print("Huffman codes:")
    for char, code in sorted(huffman_codes.items()):
        print(f"{char}: {code}")

    encoded_text = ''.join(huffman_codes[char] for char in text)

    padding_size = (8 - len(encoded_text) % 8) % 8
    padded_encoded_text = encoded_text + '0' * padding_size

    with open(output_file, 'wb') as f:
        for char, code in sorted(huffman_codes.items()):  # Writing Huffman codes to the binary file
            f.write(f"{char}: {code}\n".encode())

        f.write(bytes([padding_size]))

        byte_array = bytearray([int(padded_encoded_text[i:i + 8], 2) for i in range(0, len(padded_encoded_text), 8)])
        f.write(byte_array)

    return huffman_codes




    # Write the decoded text to the output file
    with open(output_file, 'w') as f:
        f.write(decoded_text)


input_file = "input.txt"
output_file = "encrypted.bin"
huffman_codes = encrypt_with_huffman(input_file, output_file)

