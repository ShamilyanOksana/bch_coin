import Auth
import Functions
# import Blockchain
import json
auth = Auth.Auth()
func = Functions.Functions()

# hash = auth.new_user('123')


hash = '48d881084fe2b32bc8a629a622946e0b1070983b5f6012d55071dbd995c04ac5'
auth.auth(hash, '123')
print(func.get_balance(hash))
# tx = func.money_transfer('9d0074f6ceb9d3b945cfc53d54ad69d7bf03bbc30d4baa0cf14086a5850a787f', '10', '48d881084fe2b32bc8a629a622946e0b1070983b5f6012d55071dbd995c04ac5')
# print(tx)
