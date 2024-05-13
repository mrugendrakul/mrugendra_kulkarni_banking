from Model.entity import Customer
from Util.PropertyUtil import DBConnUtil
from dao.AccountType import SavingAccount, CurrentAccount
from dao.CustomerServiceProviderImpl import CustomerServiceProviderImpl
from dao.IBankServiceProvider import IBankServiceProvider

# conn = DBConnUtil().makeConnection()
class BankServiceProviderImpl(CustomerServiceProviderImpl, IBankServiceProvider):

    def __init__(self, accounts, branch_name, brance_address, connection):
        super().__init__(connection)
        self.__accounts = accounts
        self.__branch_address = brance_address
        self.__branch_name = branch_name
        self.__conn = connection

    def create_account(self, customer: Customer, acc_no, accType, balance):
        # self.__customer = customer
        stmt = self.__conn.cursor()
        stmt.execute(f"insert into accounts (customer_id,account_type,balance) VALUES (  {customer.get_customer_info()["customer_id"]}, \'{accType}\', {balance});")
        stmt.execute(
            f"select * from accounts order by account_id desc limit 1;"
        )
        account = stmt.fetchone()
        if account[2] == "savings":
            account = SavingAccount(account_id=account[0], customer=customer, balance=account[3])
        else:
            account = CurrentAccount(account_id=account[0], customer=customer, balance=account[3])
        print(f"Account information : ")
        print(account.get_account_info())

        stmt.close()
        return account

    def listAccounts(self):
        stmt = self.__conn.cursor()
        stmt.execute("select * from accounts;")
        accounts = stmt.fetchall()
        accounts_arr = []
        for account in accounts:
            if(account[2] == "savings"):
                accounts_arr.append(SavingAccount(account_id= account[0], customer=Customer(account[1],"","","","",0,""), balance=account[3]))
            else:
                accounts_arr.append(CurrentAccount(account_id= account[0], customer=Customer(account[1],"","","","",0,""), balance=account[3]))
        self.__accounts=accounts_arr
        return accounts_arr

    def calculateInterest(self):
        pass