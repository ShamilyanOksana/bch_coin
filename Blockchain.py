import json
import rsa
from EncDec import enc, dec
import RSASign
import os

class BlockChain():
    path = 'C:\\Users\\USER\\PycharmProjects\\Blockchain-master'
    def get_package(self, package):
        '''
        Исходя из типа пакета, который пришел из сети, определяем, что с ним делать дальше
        :param package:
        :return:
        '''
        # package = dec(package)
        if package.get('type') == 'tx':
            package.pop('type')
            self.proc_transaction(package)
        elif package.get('type') == 'block':
            package.pop('type')
            self.proc_block(package)
        elif package.get('type') == 'synchronize':
            package.pop('type')
            self.synchronize(package)


    def proc_transaction(self, trans):
        '''
        проверка подписи транзакции
        '''
        hash = trans.get('from')
        ok = RSASign.RSASign().find_ok(hash)
        try:
            verif = RSASign.RSASign().verif_sign_trans(trans, ok)
        except Exception:
            print('Verification failed')
            verif = False
        else:
            if verif:
                with open('tx_buffer.txt', 'a') as buffer:
                    buffer.write(json.dumps(trans, sort_keys=True)+'\n')
        return verif

    def proc_block_transaction(self, trans):
        for i in range(len(trans)):
            current_tx = json.loads(trans[i])
            hash = current_tx.get('from')
            ok = RSASign.RSASign().find_ok(hash)
            try:
                verif = RSASign.RSASign().verif_sign_trans(current_tx, ok)
            except Exception:
                print('Verification failed')
                return False
        return True

    def proc_block(self, block):
        miner_hash = block.get('miner_hash')
        miner_ok = RSASign.RSASign().find_ok(miner_hash)

        try:
            verif_block, block = RSASign.RSASign().verif_sign_block(block, miner_ok)
            print(' Verification BLOCK OK')
        except Exception:
            print(' Verification BLOCK failed')
            return 0
        else:
            trans = block.get('tx')
            if self.proc_block_transaction(trans):
                chain_len = len(os.listdir(self.path+'\\chain'))
                with open(self.path+'\\chain\\block'+str(chain_len)+'.txt', 'w') as block_file:
                    block_file.write(json.dumps(block, sort_keys=True))
                self.create_input(block)
                tx = block.get('tx')
                for i in tx:
                    tx_i = json.loads(i)
                    hash_from = tx_i.get('from')
                    value = tx_i.get('value')
                    count = self.get_money(hash_from, value)
                    self.delete_used_inputs(hash_from, count, value)
                return True

    def synchronize(self, pack):
        id = int(pack.get('chain'))
        ip = pack.get('ip')
        my_len = len(os.listdir(self.path+'\\chain'))
        if my_len > id:
            for i in range(id+1, my_len+1):
                with open(self.path+'\\chain\\block'+str(i)+'.txt', 'r') as block:
                    row = block.readline()
                    row = json.loads(row)
                    row.update({'type': 'block'})
                    row = json.dumps(row, sort_keys=True)
                    # Network.Network().send_to_user(ip, row)

    def create_input(self, block):
        tx = block.get('tx')
        #СПИСОК ТРАНЗАКЦИЙ!!
        for i in tx:
            tx_i = json.loads(i)
            user = tx_i.get('to')
            input = {
            'from': tx_i.get('from'),
            'value': tx_i.get('value')
            }
            _input = {
                'value': tx_i.get('value')
            }
            input = json.dumps(input) + '\n'
            _input = json.dumps(_input) + '\n'
            file_name = user + '_inputs.txt'
            _file_name = user + '_useful_inputs.txt'
            with open(file_name, 'a') as f:
                f.write(input)
            with open(_file_name, 'a') as f:
                f.write(_input)

    def get_money(self, hash, value):
        value = int(value)
        inputs = open(hash+'_useful_inputs.txt')
        count = 0
        money = 0
        for line in inputs:

            if value >= money:
                line = line[:-1]
                line = json.loads(line)
                line = int(line.get('value'))
                money += line
                count += 1
            else:
                break
        if value > money:
            inputs.close()
            return 0
        else:
            inputs.close()
            return count

    def delete_used_inputs(self, hash, count, value):
        with open(hash+'_useful_inputs.txt') as inputs:
            money = 0
            cashback = 0
            for line in range(count):
                line = inputs.readline()
                line = line[:-1]
                line = json.loads(line)
                line = int(line.get('value'))
                money += line
            cashback = int(money) - int(value)
        with open(hash+'_useful_inputs.txt') as inputs:
            useful = []
            for i in range(count):
                inputs.readline()
            while True:
                a = inputs.readline()
                if a != '':
                    useful.append(a)
                else:
                    break
        f = open(hash+'_useful_inputs.txt', 'w').close()
        with open(hash+'_useful_inputs.txt', 'a') as inputs:
            for i in useful:
                inp = i
                inputs.write(inp)
        return cashback

    def get_priv_key(self, hash):
        f = open(hash+'.txt', 'r')
        keys = f.readline()
        f.close()
        keys = json.loads(keys)
        priv_key = json.loads(keys.get('ck'))
        priv_key = rsa.PrivateKey(n=priv_key.get('n'), e=priv_key.get('e'), d=priv_key.get('d'), p=priv_key.get('p'), q=priv_key.get('q'))
        f.close()
        return priv_key

    def money_transfer(self, hash_to, value, hash_from):
        rsasign = RSASign.RSASign()
        tx = {
        'from': hash_from,
        'to': hash_to,
        'value': value
        }
        if self.get_money(hash_from, value):
            _tx = json.dumps(tx)
            _tx = json.dumps(tx).encode()
            private = self.get_priv_key(hash_from)
            tx = rsasign.get_sign(tx, private)
            # sign = rsa.sign(_tx, self.get_priv_key(hash_from), 'SHA-256')
            # sign = b64encode(sign).decode()
            # tx.update({'sign': sign})
            tx.update({'type': 'tx'})
            return tx
        else:
            return False
    def get_balance(self, hash):
        if os.path.exists(self.path+'\\'+hash+'_useful_inputs.txt'):
            self.inputs = open(hash+'_useful_inputs.txt')
            money = 0
            for line in self.inputs:
                line = json.loads(line)
                line = int(line.get('value'))
                money += line
            self.inputs.close()
            return money
        else:
            self.inputs = open(hash+'_useful_inputs.txt', 'w')
            balance = {'value': '100'}
            balance = json.dumps(balance, sort_keys=True)
            self.inputs.write(balance+'\n')
            self.inputs.close()
            return balance

