import json
import rsa
import hashlib
import os


class Auth:
    user_address=None
    def genezis(self):
        path ='C:\\Users\\USER\\PycharmProjects\\Blockchain-master\\chain'
        if os.path.exists(path):
            return False
        else:
            os.mkdir(path)
            null = {'number': '0', 'timestamp': '1545258173', 'tx': [], 'pre_hash': '0', 'nonce': '0'}
            null = json.dumps(null, sort_keys=True).encode()
            hash = hashlib.sha256(null).hexdigest()
            null = json.loads(null.decode())
            null.update({'hash': hash})
            null = json.dumps(null, sort_keys=True)
            with open(path+'\\block0.txt', 'w') as gen_block:
                gen_block.write(null)

    def get_hash(self, data):
        data = data.encode()
        hash = hashlib.sha256(data).hexdigest()
        return hash

    def new_user(self, password):
        pass_hash = self.get_hash(password)
        p_k, pr_k = rsa.newkeys(512)
        pub_key = {
            'e': p_k.e,
            'n': p_k.n
        }
        priv_key = {
            'e': pr_k.e,
            'n': pr_k.n,
            'q': pr_k.q,
            'p': pr_k.p,
            'd': pr_k.d
        }
        pub_key = json.dumps(pub_key, sort_keys=True)
        priv_key = json.dumps(priv_key, sort_keys=True)
        hash = self.get_hash(pub_key)
        keys = {'ok': pub_key, 'ck': priv_key, 'hash': hash, 'pass_hash': pass_hash}
        keys = json.dumps(keys, sort_keys=True)
        # file_name = str(hash) + "_keys.txt"
        # print(file_name)
        with open(hash+'.txt', 'w') as f:
            f.write(keys)
        with open('ok-hash.txt', 'a') as f:
            f.write(json.dumps({'hash': hash, 'ok': pub_key, 'pass_hash':pass_hash})+'\n')
        return hash

    def auth(self, hash, password):
        with open('ok-hash.txt', 'r') as hash_file:
            for row in hash_file:
                current = json.loads(row)
                if current.get('hash') == hash:
                    pass_hash = self.get_hash(password)
                    if pass_hash == current.get('pass_hash'):
                        self.user_address = hash
                        return True
                    else:
                        return False


