from passlib.hash import sha256_crypt

def hash(hashpass):
    hashpass = (sha256_crypt.encrypt(hashpass))
    print ("\n", hashpass)
    return (hashpass)



hash(hashpass = input("Password to Hash: "))
