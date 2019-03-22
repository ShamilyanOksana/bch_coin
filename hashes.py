import rsa
import json
import hashlib

ok = {"e": 65537, "n": 8220103910420267009636642534860083281822640433133017925619815390901060678957545192038293138567098679744332394050345993049702154191225984450956749513346491}
ok = json.dumps(ok, sort_keys=True)

hash_ok = hashlib.sha256(ok.encode()).hexdigest()
current = json.dumps({'ok': ok, 'hash': hash_ok}, sort_keys=True)

with open('ok-hash.txt', 'a') as hash_file:
    hash_file.write(current+'\n')
