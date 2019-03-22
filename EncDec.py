import json


def enc(pack):
    pack = json.dumps(pack, sort_keys=True)
    pack = pack.encode()
    return pack


def dec(pack):
    pack = pack.decode()
    pack = json.loads(pack)
    return pack