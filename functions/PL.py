from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Dane do odszyfrowania
iv = b'v\x0fK\x81\x1c\xcb\xd9t\x18w\xf2\x91'
full_key = b"Q?\xf8\xc2\x0b\xae>\xa1\x94\xbb\xbd\xe92\xb1\x08s\xb3\xa8v\x8a\xa8\x9a'_\xe0\xbba\t\x0c\x7fN\x88"
ciphertext = b'\x1c\xa4\x82o\xf5g\xc4\x9e\xe3\xa2\xb2\xb9\xd3\x95\x98\x80\xf8F\x8aN\xa2\xb3\x96Q\x95\xfb\xb5\xb5\x1f\xb4\x8b\xaa\xb0,^(\xe1;6\x8b\xde\xf9\x90;\x8b'
tag = b'\x10.\xb4\xc97\xb4^g\x1f\x7f\xdd\x96\x8c\xb2\xcf\xf3'

# Połączenie ciphertext i tag
ciphertext_with_tag = ciphertext + tag

# Tworzenie instancji AES-GCM
aesgcm = AESGCM(full_key)

# Odszyfrowywaprint(f"IV: {iv.hex()}")
print(f"IV: {iv.hex()}")
print(f"Full Key: {full_key.hex()}")
print(f"Ciphertext: {ciphertext.hex()}")
print(f"Tag: {tag.hex()}")
plaintext = aesgcm.decrypt(iv, ciphertext_with_tag, None)
print("Odszyfrowane dane:", plaintext.decode('utf-8'))

