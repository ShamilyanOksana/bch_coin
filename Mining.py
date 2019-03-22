import Network
import rsa
import hashlib
from base64 import b64decode, b64encode
import json
from EncDec import enc, dec
import RSASign
import time
import os


class Mining:
    hash = '48d881084fe2b32bc8a629a622946e0b1070983b5f6012d55071dbd995c04ac5'
    net = Network.Network()

    # def block_size(self):
        # while True:
            # id = DatabaseBC.DataBaseBC().get_my_len()
            # timestamp = int(DatabaseBC.DataBaseBC().timestamp(id))
            # now = int(time.time())
            # delta = now - timestamp
            # if delta > (20):
            #     self.collecting_block(2)

    def collecting_block(self, block_size):
        block = {}
        with open(self.hash+'.txt', 'r') as key_file:
            info = key_file.readline()
        info = json.loads(info)
        ok = json.loads(info.get('ok'))
        ck = json.loads(info.get('ck'))
        miner_hash = info.get('hash')
        ok = rsa.PublicKey(e=ok.get('e'), n=ok.get('n'))
        ck = rsa.PrivateKey(e=ck.get('e'), n=ck.get('n'), d=ck.get('d'), p=ck.get('p'), q=ck.get('q'))
        tx_for_block = []
        tx = []
        with open('tx_buffer.txt', 'r') as tx_buffer:
            header = tx_buffer.readline()
            for i in range(block_size):
                row = tx_buffer.readline()
                if not row:
                    break
                else:
                    tx.append(json.loads(row))
        if not tx:
            return False
        else:
            print(tx)
            for current_tx in tx:
                hash_from = current_tx.get('from')
                ok_from = RSASign.RSASign().find_ok(hash_from)
                try:
                    print('trans_for_block', current_tx)
                    RSASign.RSASign().verif_sign_trans(current_tx, ok_from)
                except:
                    print('MAINING: TRANS VERIF -- FAIL')
                else:
                    tx_for_block.append(json.dumps(current_tx, sort_keys=True))
        chain_len = len(os.listdir('C:\\Users\\USER\\PycharmProjects\\Blockchain-master\\chain'))
        block.update({'number': chain_len})
        block.update({'tx': tx_for_block})
        block.update({'miner_hash': miner_hash})
        pre_hash = self.get_prehash()
        block.update({'pre_hash': pre_hash})
        block.update({'nonce': '0'})
        block = self.count_nonce(block)
        block.update({'time': time.time()})

        # подписали блок
        block = RSASign.RSASign().get_sign(block, ck)
        block.update({'type': "block"})
        print('MAINING BLOCK:', block)
        self.send_block(block)
        self.delete_proof_transacton(tx_for_block)

    def get_prehash(self):
        pre_file = os.listdir('C:\\Users\\USER\\PycharmProjects\\Blockchain-master\\chain')[-1]
        path = 'C:\\Users\\USER\\PycharmProjects\\Blockchain-master\\chain\\'+pre_file
        with open(path, 'r') as pre_block:
            block = pre_block.readline()
            block = json.loads(block)
            return block.get('hash')

    def count_nonce(self, block):
        nonce = 0
        while True:
            block = json.dumps(block, sort_keys=True).encode()
            hash = hashlib.sha256(block).hexdigest()
            if hash[-4:] == '0000':
                block = json.loads(block.decode())
                block.update({'hash': hash})
                break
            else:
                nonce += 1
                block = json.loads(block.decode())
                block.update({'nonce': str(nonce)})
        print(nonce, ':', hash)
        return block

    def send_block(self, block):
        block = enc(block)
        self.net.send_message(block)

    def delete_proof_transacton(self, tx_for_block):
        buf = []
        with open('tx_buffer.txt', 'r') as tx_buffer:
            for row in tx_buffer:
                buf.append(row)
        for i in range(len(tx_for_block)):
            for j in range(1, len(buf)):
                tx1 = json.loads(tx_for_block[i])
                sign1 = tx1.get('sign')
                tx2 = json.loads(buf[j])
                sign2 = tx2.get('sign')
                if sign1 == sign2:
                    buf.pop(j)
                    break
        with open('tx_buffer.txt', 'w')as tx_buffer:
            for row in buf:
                tx_buffer.write(row)


