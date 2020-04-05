
import hashlib as hasher

# global encrypt function
def to_sha(string):
    sha = hasher.sha256()
    sha.update(string.encode('utf-8'))
    return sha.hexdigest()
