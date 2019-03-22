import Network
import json
import rsa
import hashlib
import RSASign

rsasign = RSASign.RSASign()
net = Network.Network()
# net.add_new_ip('192.168.40.198')
# net.get_all_ip()
hash = 'ae0250e67d0810a36e089bd8a06262fa0337ed927696ae7806efd9d1e58b720f'
with open(hash + '.txt', 'r') as key_file:
    keys = key_file.readline()
keys = json.loads(keys)
my_hash = keys.get('hash')
private = json.loads(keys.get('ck'))
public = json.loads(keys.get('ok'))
slava_hash = 'c6b62c8393f4bcf4a74a7435f49377e4fd256297473d3cdcd2e9b8a2f6647c60'
private = rsa.PrivateKey(private.get('n'), private.get('e'), private.get('d'), private.get('p'), private.get('q'))
for i in range(1, 7):
    tx = {'from': my_hash,
          'to': slava_hash,
          'value': str(i*10)}
    tx = rsasign.get_sign(tx, private)
    # print(tx.get('sign'))
    tx.update({'type': 'tx'})
    net.send_message(tx)