from abc import ABC , abstractmethod

class Account(ABC) :
    @abstractmethod
    def deposit(self , amount):
        pass
    @abstractmethod
    def withdraw(self , amount):
        pass

class BankAccount(Account):
    def __init__(self , account_number ,name , password , balance):
        self.account_number = account_number
        self.name = name
        self.__password = password
        self.__balance = int(balance)
    def get_password(self):
        return self.__password
    def get_balance(self):
        return self.__balance
    def deposit(self, amount):
        self.__balance += amount
    def withdraw(self, amount):
        if amount > self.__balance :
            return False
        self.__balance -= amount
        return True
    def __str__(self):
        return f'{self.account_number} {self.name} {self.__balance}'
  