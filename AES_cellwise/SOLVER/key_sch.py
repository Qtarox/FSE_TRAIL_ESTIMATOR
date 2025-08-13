import config.config as config
s_box=config.Sbox
rcon=config.rcon

def rot_word(word):
    return word[1:] + word[:1]

def sub_word(word):
    return [s_box[b] for b in word]

def xor_words(w1, w2):
    return [b1 ^ b2 for b1, b2 in zip(w1, w2)]

def key_expansion(master_key):
    assert isinstance(master_key, list) and len(master_key) == 16
    for byte in master_key:
        assert 0 <= byte <= 0xFF, "Each byte must be in 0..255"

    # Step 1: Divide master key into four 4-byte words
    w = [master_key[i:i+4] for i in range(0, 16, 4)]

    # Step 2: Generate remaining 40 words (AES-128 = 4 initial + 40 = 44 total words)
    for i in range(4, 44):
        temp = w[i - 1]
        if i % 4 == 0:
            temp = xor_words(sub_word(rot_word(temp)), [rcon[i//4 - 1], 0, 0, 0])
        w.append(xor_words(w[i - 4], temp))

    # Step 3: Form 11 round keys (each is 4 words = 16 bytes)
    round_keys = [sum(w[i:i+4], []) for i in range(0, 44, 4)]
    return round_keys

#  Example Input (array of 16 bytes)
master_key = [0x2b, 0x7e, 0x15, 0x16,
              0x28, 0xae, 0xd2, 0xa6,
              0xab, 0xf7, 0x15, 0x88,
              0x09, 0xcf, 0x4f, 0x3c]

#  Generate round keys
round_keys = key_expansion(master_key)

#  Print round keys
for i, rk in enumerate(round_keys):
    print(f"Round {i:2}: {rk}")