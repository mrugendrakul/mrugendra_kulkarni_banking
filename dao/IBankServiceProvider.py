from abc import ABC,abstractmethod

from Model.entity import Customer


class IBankServiceProvider(ABC):
    @abstractmethod
    def create_account(customer: Customer, accNo,accType,balance):
        pass

    @abstractmethod
    def listAccounts(self):
        pass

    @abstractmethod
    def calculateInterest(self):
        pass