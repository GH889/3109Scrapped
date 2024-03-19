def checkPadding(plainText):
    lastByte = int(plainText[-2:],16) 
    if(lastByte<=(len(plainText)/2) and lastByte>0):
        for i in range(lastByte):
            if(int(plainText[len(plainText)-(2*(i+1)):len(plainText)-(2*i)],16)!=lastByte):
               return False
        return True
    else:
        return False
def addPadding(plainText):
    padding =8 - (int(len(plainText)/2)%8)
    for _ in range(padding):
        plainText+= (hex(padding)[2:]).zfill(2)
    return plainText
def removePadding(plainText):
    return plainText[:-2*int(plainText[-2:])]

def modifyBlock(plainText,key):
    plainText = hex(int(plainText, 16) ^ int(key, 16))[2:]
   
    k = int(key[int(key[7],16)],16)%4
    newPlainText=""
    for i in range(len(plainText),0,-(2**k)):
        newPlainText+= plainText[i-(2**k):i]
    
    plainText = hex(int(newPlainText, 16) ^ int(key, 16))[2:]
    return plainText

def blockChainingEncrypt(IV,plainText,key):
    cipherText = ""
    for i in range(len(plainText)//16):
        block = plainText[i*16:(i+1)*16]
        block = hex(int(block, 16) ^ int(IV, 16))[2:]
        block = modifyBlock(block,key)
        cipherText += block
    return cipherText
def blockChainingDecrypt(IV,cipherText,key):
    plainText = ""
    for i in range(len(cipherText)//16):
        block = cipherText[i*16:(i+1)*16]
        block = modifyBlock(block,key)
        block = hex(int(block, 16) ^ int(IV, 16))[2:]
        plainText += block
    return plainText

def isHex(hex):
    if(len(hex)//2 == len(hex)/2):
        try:
            for i in range(len(hex)//2):
              int(hex[i*2:(i+1)*2],16)
            return True
        except:
            return False
    else:
        return False
def makeCipherText(text,IV,key):   
    plainText = text.encode("utf-8").hex()
    plainText = addPadding(plainText)
    return blockChainingEncrypt(IV,plainText,key)
def giveToServer(cipherText,IV,key):
    if(isHex(cipherText)):
        plainText = blockChainingDecrypt(IV,cipherText,key)
        if(checkPadding(plainText[-16:])):
            plainText = removePadding(plainText)
            #print(bytearray.fromhex(plainText).decode())
            print("Correct padding")
        else:
            print("Incorrect padding")
    else:
        print("Incorrect input")

key = "11f2334455667788"
IV  = "1a2b3c4d5e6f7081"
text = "A+ grade please"

cipherText = makeCipherText(text,IV,key)
print(cipherText)

giveToServer(cipherText,IV,key)