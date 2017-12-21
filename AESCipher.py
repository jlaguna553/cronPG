from Crypto.Cipher import AES
import hashlib
import sys
import binascii
import Padding

#plaintext='ZIIFPHXM4ckqHCVlLFqwJw=='


#plaintext = 'e3l0z92_252X9QkT'
plaintext ='VYYvTw7ywu4WISQ+C17qVVVgJUe98e3Vc4PvP0mYvh4='

#plaintext = 'QPM5TUWAu+5DZUMEdHnZcVVgJUe98e3Vc4PvP0mYvh4='
key = '05160f048ec6f52e924837c2bf84d665'
iv= 'd24ac216d2292c8f'



def encrypt(plaintext,key,iv):
    plaintext = Padding.appendPadding(plaintext,blocksize=Padding.AES_blocksize,mode=0)
    encobj = AES.new(key,AES.MODE_OFB,iv)
    return(binascii.b2a_base64(encobj.encrypt(plaintext)))

def decrypt(ciphertext,key,iv):
    cipher = binascii.a2b_base64(ciphertext)
    encobj = AES.new(key,AES.MODE_OFB,iv)
    return(Padding.removePadding(encobj.decrypt(cipher),mode=0))


#print encrypt(plaintext,key,iv)
print decrypt(plaintext,key,iv)

#ciphertext = encrypt(plaintext,key,AES.MODE_OFB,iv)
#print "Cipher (OFB): "+binascii.b2a_base64(bytearray(ciphertext))

#plaintext = decrypt2(binascii.a2b_base64("YvRsPlLW+e4BEh4LF2bcdVVgJUe98e3Vc4PvP0mYvh4="),key,AES.MODE_OFB,iv)
#plaintext = Padding.removePadding(plaintext,mode=0)
#print "  decrypt: "+plaintext
