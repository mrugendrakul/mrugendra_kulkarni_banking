import datetime

from Exception.Exceptions import InvalidAccountException, InsufficientFundException
from Model.entity import Customer, Account, Transaction
from Util.PropertyUtil import DBConnUtil
from dao.AccountType import SavingAccount, CurrentAccount
from dao.ICustomerServiceProvider import ICustomerServiceProvider


# class Bank():
#     def __init__(self,account:Account):
#         self.__Account = account
#
#     def deposit(self,amount):
#         self.__Account.deposit(amount)
#
#     def withdraw(self,amount):
#         if self.__Account.get_account_info()["balance"] > amount:
#             self.__Account.withdraw(amount)
#
#     def calculate_interest(self):
#         self.__Account.calculate_interest()
# conn = DBConnUtil().makeConnection()
class CustomerServiceProviderImpl(ICustomerServiceProvider):

    def __init__(self, connection):
        self.__conn = connection

    def create_account(self, customer: Customer, acc_no, accType, balance):
        stmt = self.__conn.cursor()
        if accType == "savings":
            result = stmt.execute(
            f"insert into accounts (customer_id,account_type,balance) VALUES ( {customer.get_customer_info()["customer_id"]}, 'savings', {balance});")
            print(result)
        else:
            result = stmt.execute(
                f"insert into accounts (customer_id,account_type,balance) VALUES ( {customer.get_customer_info()["customer_id"]}, 'current', {balance});")
            print(result)
        self.__conn.commit()
        stmt.execute(f"select account_id from accounts order by account_id desc limit 1;")
        account_id = stmt.fetchone()
        account_id = account_id[0]
        print(account_id)
        # stmt.commit()
        stmt.close()
        if accType == "savings":
            return SavingAccount(account_id, customer, balance)
        elif accType == "current":
            return CurrentAccount(account_id, customer, balance)

    def get_account_balance(self, account_number):
        stmt = self.__conn.cursor()
        stmt.execute(f"select balance,account_type from accounts where account_id = {account_number};")
        rows = stmt.fetchone()
        if len(rows) == 0:
            raise InvalidAccountException()
        tempdict = {
            "balance": rows[0],
            "account_type": rows[1]
        }
        # stmt.close()
        return tempdict

    def deposit(self, account: Account, amount):
        stmt = self.__conn.cursor()
        stmt.execute(
            f"insert into transactions (account_id,transaction_type,amount,transaction_date) VALUES ( {account.get_account_info()["account_id"][0]}, 'deposit', {amount}, '{datetime.date.today()}');")
        stmt.execute(
            f"update accounts set balance = balance + {amount} where account_id = {account.get_account_info()["account_id"][0]};")
        print(self.get_account_balance(account.get_account_info()["account_id"][0]))
        # stmt.commit()
        stmt.close()

    def withdraw(self, account: Account, amount):
        balance = self.get_account_balance(account.get_account_info()["account_id"][0])

        if amount > balance["balance"]:
            raise InsufficientFundException()
            return

        stmt = self.__conn.cursor()
        stmt.execute(f"insert into transactions (account_id,transaction_type,amount,transaction_date) VALUES ( {account.get_account_info()["account_id"][0]}, 'withdrawal', {amount}, '{datetime.date.today()}');")
        stmt.execute(f"update accounts set balance = balance - {amount} where account_id = {account.get_account_info()["account_id"][0]};")
        print(self.get_account_balance(account.get_account_info()["account_id"][0]))
        # stmt.commit()
        stmt.close()

    def transfer(self, from_account: Account, to_account_number, amount):
        balance = self.get_account_balance(from_account.get_account_info()["account_id"][0])

        if amount > balance["balance"]:
            raise InsufficientFundException()
            return

        stmt = self.__conn.cursor()
        stmt.execute(
            f"insert into transactions (account_id,transaction_type,amount,transaction_date) VALUES ( {from_account.get_account_info()["account_id"][0]}, 'transfer', {amount}, '{datetime.date.today()}')")
        stmt.execute(
            f"update accounts set balance = balance + {amount} where account_id = {to_account_number};")
        stmt.execute(
            f"update accounts set balance = balance - {amount} where account_id = {from_account.get_account_info()["account_id"][0]};")
        # print(self.get_account_balance(from_account.get_account_info()["account_id"]))
        # stmt.commit()
        stmt.close()

    def get_account_details(self, account_number):
        stmt = self.__conn.cursor()
        stmt.execute(
            f"select * from accounts where account_id ={account_number};"
        )
        account = stmt.fetchall()
        if len(account) == 0:
            raise InvalidAccountException()
            return

        stmt.execute(
            f"select * from customers where customer_id in ( select customer_id from accounts where account_id = {account_number});"
        )
        customer = stmt.fetchone()
        customer = Customer(customer[0], customer[1], customer[2], customer[3], customer[4], customer[5], customer[6])
        print("Customer information : ")
        print(customer.get_customer_info())

        stmt.execute(
            f"select * from accounts where account_id ={account_number};"
        )
        account = stmt.fetchone()
        if account[2] == "savings":
            account = SavingAccount(account_id= account[0], customer=customer, balance=account[3])
        else:
            account = CurrentAccount(account_id= account[0], customer=customer, balance=account[3])
        print(f"Account information : ")
        print(account.get_account_info())

        stmt.close()
        return account

    def get_transactions(self,account:Account):
        stmt = self.__conn.cursor()

        stmt.execute(
            f"select * from transactions where account_id = {account.get_account_info()["account_id"][0]};"
        )
        transactions = stmt.fetchall()
        tran_arr = []
        for transaction in transactions:
            tran_arr.append(Transaction(transaction_id=transaction[0],account=account,transaction_type=transaction[2],amount=transaction[3],transaction_date=transaction[4]))
        return tran_arr