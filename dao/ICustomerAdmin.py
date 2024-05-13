from abc import ABC,abstractmethod

from Model.entity import Customer


class ICustomerAdmin(ABC):
    @abstractmethod
    def create_customer(self, customer: Customer):
        pass

    @abstractmethod
    def get_customer(self,customer_id):
        pass