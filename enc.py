"""imports"""
import rsa


def generate_key():
    """ generate_key"""
    (pbk, prk)= rsa.newkeys(1024)
    with open('keys/publicKey.pem', 'wb') as part:
        part.write(pbk.save_pkcs1('PEM'))
    with open('keys/privateKey.pem', 'wb') as part:
        part.write(prk.save_pkcs1('PEM'))
    return pbk, prk


def load_key():
    """ load_key"""
    with open('keys/publicKey.pem', 'rb') as part:
        pbk = rsa.PublicKey.load_pkcs1(part.read())
    with open('keys/privateKey.pem', 'rb') as part:
        prk = rsa.PrivateKey.load_pkcs1(part.read())
    return pbk,prk


def decrypt(message):
    """ decryot a message"""
    pbk, prk= load_key() # pylint: disable=unused-variable
    try:
        return rsa.decrypt(message, prk).decode('ascii')
    except: # pylint: disable=bare-except
        return False


def encrypt(message):
    """ encrypt"""
    pbk, prk= load_key() # pylint: disable=unused-variable
    try:
        return rsa.encrypt(message.encode('ascii'), pbk)
    except: # pylint: disable=bare-except
        return False


#def save_encrypt(message):
 #   cipher= encrypt(message)
  #  if(cipher jFalse):
   #     print("No key")
    #else:
     #   with open('keys/cipher.txt', 'wb') as part:
      #      part.write(cipher)
