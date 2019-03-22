import  Auth
import threading
import Network
class Cli:
    Station = str()
    AuthStation = None
    Comand = str()
    auth = Auth.Auth()
    Blockchain_main = Network.Network()
    Hash = str()
    #Func = Functions.Functions()
    def help(self):
        print("Чтобы пройти авторизацию введите кшоманду auth ")
        print("Чтобы зарегестрироватся введите команду reg")
        print("Чтобы вывести открытый ключь введите команд openkey")
        print("Чтобы вывести закрытый ключь введите команд closekey")
        print("Чтобы вывести транзакцию введите команду transaction")
        print("Чтобы посмотреть hash введите print_hash")
        print("Чтобы узнать баланс введите get_balance")
        print("Чтобы переслать деньги введите команду send_money")
        print("Чтобы выйти введите exit")
    def _auth(self):
        print("auth")
        print("Введите хэш")
        hash = input()
        print("Введите пароль")
        password = input()
        self.AuthStation =  self.auth.auth(hash, password)
        print(self.AuthStation)
        if self.AuthStation == True:
            print("Вы вошли в систему")
            self.Hash = hash
        else:
            print("Не правельный хэш или пароль")
    def regestrtion(self):
        print("reg")
        print("Введите пароль")
        password = input()
        hesh = self.auth.new_user(password)
        self.auth.genezis()
        print("Ваш хэш "+ hesh)
    def printOpenKey(self):
        print("OpenKey")
    def printCloseKey(self):
        print("CloseKey")
    def printTransaction(self):
        print("Transaction")
    def sendMoney(self):
        if self.AuthStation==True:
            print("Введите хэш пользователя котрому хотите перевести")
            Hash_to = input()
            print("Введите количестов денег")
            Money = input()
            tx = self.Blockchain_main.bch.money_transfer(Hash_to, Money, self.Hash)
            if tx:
                self.Blockchain_main.send_message(tx)
                print("Отправленно пользователю "+Hash_to)
            else:
                print("Не достаточно средств")
        else:
            print("Вы не вошли в систему")

    def getBalance(self):
        if self.AuthStation==True:
            #thread = threading.Thread( target=self.Func.get_balance,args={self.Hash})
            #thread.start()
            balance = self.Blockchain_main.bch.get_balance(self.Hash)
            print(balance)
            #del self.Func
        else:
            print("Вы не вошли в систему")
    def printHash(self):
        if self.AuthStation == True:
            print(self.Hash)
        else:
            print("Вы не вошли в систему")
    def mainLoop(self):
        print("Welcome")
        while True:
            self.Comand = input()
            if self.Comand =="help":
                self.help()
            elif self.Comand =="auth":
                self._auth()
            elif self.Comand =="reg":
                self.regestrtion()
            elif self.Comand=="openkey":
                if self.AuthStation == True:
                    self.printOpenKey()
                else:
                    print("Вы не вошли в систему")
            elif self.Comand == "closekey":
                if self.AuthStation == True:
                    self.printOpenKey()
                else:
                    print("Вы не вошли в систему")
            elif self.Comand == "transaction":
                if self.AuthStation == True:
                    self.printTransaction()
                else:
                    print("Вы не вошли в систему")
            elif self.Comand == "print_hash":
                self.printHash()
            elif self.Comand =="get_balance":
                self.getBalance()
            elif self.Comand == "send_money":
                self.sendMoney()


            elif self.Comand =="exit":
                exit()
            else:
                print("Такой команды не существует")


CLI = Cli()
CLI.mainLoop()