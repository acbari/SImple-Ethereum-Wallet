from eth_account import Account
from eth_account.messages import encode_defunct
import json, random, subprocess
    
def createAccount(randomString):
    acct = Account.create(randomString)
    return acct
    
def createAccountAuto():
    Account.enable_unaudited_hdwallet_features()
    acct, mnemonic = Account.create_with_mnemonic()
    return acct, mnemonic

def loadAccount(param, mode=0):
    if mode == 0:#privatekey
        acct = Account.from_key(param)
    elif mode == 1:#mnemonic
        acct = Account.from_mnemonic(param)
    elif mode == 2:#raw_transaction
        acct = Account.recover_transaction(param)
    return acct

def encryptAccount(acct, password, fsave = ""):
    encrypted = Account.encrypt(acct.key, password)
    if fsave != "":
        with open(fsave, 'w') as f: 
            f.write(json.dumps(encrypted))
    else:
        return encrypted

def decryptAccount(encrypted, password, fromfile = False):
    if fromfile:
        encStr = ""
        with open(encrypted, 'r') as f: 
            encStr = json.loads(f.read())
    else:
        encStr = encrypted
    try:
        acct_key = Account.decrypt(encStr, password)
        acc = loadAccount(acct_key)
        return acc
    except:
        return None
def signMessage(acct, mesage):
    msghash = encode_defunct(text=mesage)
    signedMsg = Account.sign_message(msghash, acct.key)
    return signedMsg

def signTransaction(acct, transaction, tosend=False, w3 = None):
    signed = Account.sign_transaction(transaction, acct.key)
    if tosend and w3 != None:
        w3.eth.sendRawTransaction(signed.rawTransaction)
    return signed 
 
if __name__ == "__main__":
    def genRandomStr():
        val = str(random.randint(1000000, 9999999))
        for i in range(3):
            val += " " + str(random.randint(1000000, 9999999))
        return val
        
    #create & load account
    acc1 = createAccount( genRandomStr() )
    print(acc1.address)
    print(acc1.key.hex())
    acc2, mnemonic = createAccountAuto()
    print(acc2.address)
    print(mnemonic)
    load_acc1 = loadAccount(acc1.key, 0)
    load_acc2 = loadAccount(mnemonic, 1)
    if acc1 == load_acc1: print("True")
    if acc2 == load_acc2: print("True")
    
    #encrypt & decrypt account
    pwd = genRandomStr()
    enc1 = encryptAccount(acc1, pwd )
    dec1 = decryptAccount(enc1, pwd )
    print(enc1)
    print(dec1.address)
    print(acc1.address)
    if acc1 == dec1: print("True")
    
    #encrypt & decrypt account with file
    pwd = genRandomStr()
    encryptAccount(acc2, pwd, "acc2.enc" )
    dec2 = decryptAccount("acc2.enc", pwd, True )
    print(dec2.address)
    print(acc2.address)
    if acc2 == dec2: print("True")
    
    #sign a message
    msg1 = signMessage(acc1, "Hello world")
    print(msg1)
    print(msg1['signature'].hex())
    
    #sign a transaction
    nonce = 1 #in real test, it must be set to the real nonce of acc1
    transaction = {
        'from': acc1.address,
        'to': acc2.address,
        'value': 1000000000,
        'gas': 2000000,
        'gasPrice': 1000000000,
        'nonce': nonce,
        'chainId': 4
    }
    trx = signTransaction(acc1, transaction)
    print(trx) 
    print(trx['hash'].hex()) 
    