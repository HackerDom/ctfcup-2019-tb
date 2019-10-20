MOD = 256

def KSA(key):
    key_length = len(key)
    S = range(MOD)  # [0,1,2, ... , 255]
    j = 0
    for i in range(MOD):
        j = (j + S[i] + key[i % key_length]) % MOD
        S[i], S[j] = S[j], S[i]  # swap values

    return S


def PRGA(S):
    i = 0
    j = 0
    while True:
        i = (i + 1) % MOD
        j = (j + S[i]) % MOD

        S[i], S[j] = S[j], S[i]  # swap values
        K = S[(S[i] + S[j]) % MOD]
        yield K


def get_keystream(key):
    S = KSA(key)
    return PRGA(S)


def encrypt(key, plaintext):
    key = [ord(c) for c in key]
    keystream = get_keystream(key)

    res = []
    for c in plaintext:
        val = ("%02X" % (ord(c) ^ next(keystream)))
        res.append(val)
    return ''.join(res)


def decrypt(key, ciphertext):
    ciphertext = ciphertext.decode('hex')
    res = encrypt(key, ciphertext)
    return res.decode('hex')

if __name__ == '__main__':

    key = 'this_is_not_flag' 
    encrypted = "e\xf9E\xce\x8a`\xe0\x90\xfef\xffg\xef\x1b\xd1.\xf1k\xa4\x0f\x96\x9e\xbe\xc0\x0b\x88\xc3@\x06'Z\xd2\xdf\xa6\x15\r\x8d\xef\xcf)\x83\xa4D=\xd7\x9b\xf4\x9e\x87gM\xcfNZ\xe0k\xf4\x13\xe1\xdc\xbb\xces\x14\xee\t\xe3OF".encode('hex')
    print decrypt( key, encrypted )
