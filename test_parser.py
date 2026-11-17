# from backend.app.ast_parser import extract_functions

# test1--------------------------------
# code = """
# def authenticate_user():
#     print("Authenticating")


# class PaymentService:

#     def process_payment(self):
#         print("Processing")

#     def validate_payment(self):
#         print("Validating")


# def outer_function():

#     def inner_function():
#         print("Nested")

#     inner_function()
# """

# test2--------------------------------
# code = """
# class UserService:
#     def create_user(self):
#         pass

# class PaymentService:
#     def process_payment(self):
#         pass

# def helper():
#     pass
# """

# test3--------------------------------
# code = """
# def outer():
#     def middle():
#         def inner():
#             pass
# """

# test4--------------------------------
# code = ""

# test5--------------------------------
# code = """
# def hello(
#     print("Hello")
# """

# test6--------------------------------
# code = """
# import os
# import numpy as np

# from fastapi import FastAPI
# from pathlib import Path

# class UserService:

#     def create_user(name, email, age=18):
#         pass

# class PaymentService:

#     def process_payment(self, amount):
#         pass

# def authenticate():
#     pass
    
# def calculate_total(price: float, quantity: int = 2) -> float:
#     return price * quantity

# @staticmethod
# def calculate(x, y):
#     return x + y

# @property
# def username(self):
#     return self._username

# @route("/users", methods=["GET"])
# def get_users():
#     pass
    
# async def fetch_data():
#     pass
# """

# result = extract_functions(code)

# print(result)


# from backend.app.parsers.python_parser import PythonParser


# parser = PythonParser()

# code = """
# def authenticate(username, password):
#     return True

# class PaymentService:

#     def process_payment(self, amount):
#         return amount

#     def refund_payment(self, transaction_id):
#         return True
# """

# result = parser.parse(code)

# print(result)


from backend.app.parsers.javascript_parser import JavaScriptParser

parser = JavaScriptParser()

code = """
function authenticate(username, password) {
    return true;
}

class PaymentService {

    processPayment(amount) {
        return amount;
    }

    refundPayment(transactionId) {
        return true;
    }
}

const greet = (name) => {
    return "Hello " + name;
};

const add = (a, b) => a + b;

const multiply = (a, b) => {
    return a * b;
};
"""

result = parser.parse(code)

print(result)