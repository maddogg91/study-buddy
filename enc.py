import rsa





def generateKey():
    (pbk, prk)= rsa.newkeys(1024)
    with open('keys/publicKey.pem', 'wb') as p:
        p.write(pbk.save_pkcs1('PEM'))
    with open('keys/privateKey.pem', 'wb') as p:
        p.write(prk.save_pkcs1('PEM'))
    return pbk, prk
        
def loadKey():
    with open('keys/publicKey.pem', 'rb') as p:
        pbk = rsa.PublicKey.load_pkcs1(p.read())
    with open('keys/privateKey.pem', 'rb') as p:
        prk = rsa.PrivateKey.load_pkcs1(p.read())
    return pbk,prk
    
def decrypt(message):
    pbk, prk= loadKey()
    try:
        return rsa.decrypt(message, prk).decode('ascii')
    except:
        return False
        
            
def encrypt(message):
    pbk, prk= loadKey()
    try:
        return rsa.encrypt(message.encode('ascii'), pbk)
    except:
        return False
        
def saveEncrypt(message):
    cipher= encrypt(message)
    if(cipher == False):
        print("No key")
    else:
        with open('keys/cipher.txt', 'wb') as p:
            p.write(cipher)
    


