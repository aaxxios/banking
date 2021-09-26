import crudOps
import datetime as dt
import getpass
import hashlib
import pyperclip
from random import randint
import re
import time
import utils

crudOps.setup_db()


class InvalidAmount(Exception):
    pass


class UnregisteredAccount(Exception):
    pass


class Bank:
    def __init__(self):
        self._logged_in = False
        self.login_msg = "YOU MUST LOGIN!!!"
        self.act_num = None
        self.balance = None
        self.name = None

    def logged_in(self):
        return self._logged_in

    def _log(self):
        self._logged_in = True

    loggedIn = property(logged_in, _log)

    def __encrypt_pin(self, pin, name):
        hash_string = (pin + name)
        hash_string = hash_string.encode("utf8")
        return hashlib.sha256(hash_string).hexdigest()

    def _getname(self):
        regez = re.compile(r"((?:\w{2,10})(?: \w{2,10})( \w{2,10})?)")
        name = input("Enter your full names: \n")
        match = regez.search(name)
        try:
            name = match.group()
        except Exception:
            print("No match found\n")
            name = self._getname()
        else:
            validate = re.search(r"[0-9]*", name)
            if validate is None:
                print("Name cannot contain number\n")
                name = self._getname()
        return name.title()

    def _verify(self, pin, name):
        for _ in range(3):
            password = getpass.getpass()
            password = self.__encrypt_pin(password, name)
            if password == pin:
                break
        if password == pin:
            return True
        return False

    def _hibernate(self, act_num):
        sec = time.time() + 30
        crudOps.hibernate_user(act_num, sec)

    def _isHibernated(self, wait):
        if wait > dt.datetime.now():
            return f"Account hibernated for {wait - dt.datetime.now()}"
        return False

    def _userInfo(self, act_num):
        return crudOps.get_user_by_number(act_num)

    def _updateBalance(self, act_num, bal):
        crudOps.update_balance(act_num, bal)

    @property
    def _getPin(self):
        msg = "Choose a PIN to secure your account: \n"
        pin = getpass.getpass(prompt=msg)
        while len(pin) < 5:
            utils.warn("Password too short")
            pin = getpass.getpass(prompt=msg)
        return pin

    @property
    def _setNumber(self):
        while True:
            num = randint(100000000, 999999999)
            num = "0" + str(num)
            if not crudOps.get_user_by_number(num):
                break
        return num

    def _createAccount(self, act_num, name, phone, pin):
        crudOps.add_user(act_num, name, phone, pin)

    def create_account(self):
        msg = "*" * 4 + "WELCOME TO BotBank" + "*" * 4
        print(msg, end="\n")
        print("\t<provide your details \n\tto create account>")
        name = self._getname()
        act_num = self._setNumber
        phone = input("Enter your phone number: ")
        pin = self._getPin
        dispPin = pin
        pin = self.__encrypt_pin(pin, name)
        self._createAccount(act_num, name, phone, pin)
        utils.refresh()
        print("Your account has been created\n=====DETAILS=====\n")
        utils.info(
            f"Name: {name}\nAccount Number: {act_num}\nPassword:\
            {dispPin}\nLogin to access your account\n")
        copy = input('Copy accout number to clipboard? y/n: ')
        copy = copy.lower()
        while copy not in 'yn':
            copy = input('Copy accout number to clipboard? y/n: ')
        if copy == 'y':
            pyperclip.copy(act_num)

    def login(self):
        if self._logged_in:
            utils.warn("You are logged in!")
            return 0
        msg = "Enter your account number: "
        act_num = input(msg)
        user = crudOps.get_user_by_number(act_num)[0]
        while not user:
            print(f"{act_num} is not registered with BotBank")
            act_num = input(msg)
        wait = user[-1]
        b = self._isHibernated(wait)
        if b:
            return b
        if self._verify(user[2], user[1]):
            self._log()
            self.act_num = user[0]
            self.name = user[1]
            self.balance[3]
            utils.info(f"Welcome back {user[0]}, You are now logged in\n")
        else:
            self._hibernate(act_num)
            utils.warn("Maximum password attempts exceeded and\
            account has been hibernated for 30 minutes\n")

    def deposit(self):
        if not self._logged_in:
            utils.warn("You must login")
            return
        msg = "Enter amount to deposit: \n"
        try:
            amount = (input(msg))
            amount = int(amount)
        except TypeError:
            raise InvalidAmount(amount) from None
        else:
            if amount > 0:
                crudOps.update_balance(self.act_num)
                utils.info(f"${amount} has been credited to your account and\
                    new balance is {self.balance + amount}\n")
            else:
                utils.warn("Amount cannot be less than 1")

    def transfer(self):
        if not self._logged_in:
            return self.login_msg
        msg = "Enter amount to transfer: \n"
        try:
            amount = input(msg)
            amount = int(amount)
        except TypeError:
            raise InvalidAmount(amount) from None
        else:
            if amount <= self.balance:
                msg = "Enter recepient account number: \n"
                account = input(msg)
                recipient = crudOps.get_user_by_number(account)
                if not recipient:
                    raise UnregisteredAccount(account) from None
                crudOps.transfer(self.act_num, recipient[0], amount)
                self.balance -= amount
                utils.info('Succesful')

    def withdraw(self):
        if not self._logged_in:
            utils.warn(self.login_msg)
            return
        msg = "Enter amount to withdraw: \n"
        try:
            amount = input(msg)
            amount = int(amount)
        except TypeError:
            raise InvalidAmount(amount) from None
        else:
            if amount <= self.balance:
                crudOps.update_balance(self.act_num, amount, -1)
                utils.info('Successful!')
            else:
                utils.warn("Insufficient funds\n")

    def check_balance(self):
        if not self._logged_in:
            utils.warn(self.login_msg)
            return 0
        utils.info("Available Balance:\n{} ".format(self.balance))

    def logout(self):
        if not self._logged_in:
            return ("YOU ARE NOT LOGGED IN\n")
        self._logged_in = False
        utils.info(f"Logged out {self.name}")
