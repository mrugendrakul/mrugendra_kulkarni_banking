import unittest

from BankApp import BankApp
from Exception.Exceptions import CustomerNotFoundException, InvalidAccountException
from Model.entity import Customer
from dao.CustomerAdmin import CustomerAdmin


class test_cases(unittest.TestCase):
    def setUp(self):
        self.customer = CustomerAdmin()
        self.BankApp = BankApp(Customer(0,"","","","","",""))


    def test_create_customer(self):
        temp_cust = self.customer.create_customer(Customer(0, first_name="someone", last_name="newone", dob="1968-02-04", email="someone@example.com", phone_number = "2898512618", address = "Nanded"))

        self.assertNotEqual(temp_cust,None)

    def test_get_customer(self):
        with self.assertRaises(CustomerNotFoundException):
            temp_cust = self.customer.get_customer(customer_id=20)


    def test_get_transactions(self):
        with self.assertRaises(InvalidAccountException):
            self.BankApp.set_current_account()
            transactions = self.BankApp.getTransactions()
