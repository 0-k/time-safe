import secrets
import string
import os
import hashlib
import base64
import datetime
import getpass
import warnings
import pandas as pd
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

from src.printer import Printer

warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)


class Password:
    def __init__(self, service_name=None):
        self.service_name = service_name
        self.__printer = Printer()
        self.__password = None
        self.__salt = None
        self.__hash = None
        self.__token = None
        self.locked_until = None
        self.lockout_period_in_hours = 24
        self.__generate_salt()

    def check_validity(self):
        while True:
            password = getpass.getpass()
            self.__password = bytes(password, 'utf-8')
            self.open_salt('m_')
            self.hash()
            hash_to_check = self.open_hash('m_')
            if self.__hash == hash_to_check:
                break
            else:
                self.__printer.incorrect_password()

    def set(self):
        while True:
            password = getpass.getpass()
            if password is None:
                self.__printer.valid_name()
            elif len(password) < 12:
                self.__printer.short_password()
            elif type(password) != str:
                self.__printer.valid_name()
            else:
                break
        self.__generate_salt()   # enforce that new salt is created for new password
        self.__password = bytes(password, 'utf-8')

    def generate(self, length=20):
        if int(length) < 12:
            raise AssertionError('Password needs to have minimum length of 12')
        alphabet = string.ascii_letters + string.digits + '#%&$§*_'
        while True:
            password = ''.join(secrets.choice(alphabet) for i in range(int(length)))
            if self.__has_numbers(password) and self.__has_extra_strings(password):
                self.__password = bytes(password, 'utf-8')
                self.__generate_salt()  # enforce that new salt is created for new password
                break

    @staticmethod
    def __has_extra_strings(input_string):
        chars = set('#%&$§*_')
        return any((c in chars) for c in input_string)

    @staticmethod
    def __has_numbers(input_string):
        return any(char.isdigit() for char in input_string)

    def __generate_salt(self):
        self.__salt = os.urandom(32)

    def hash(self):
        if self.__salt is None:
            raise BrokenPipeError('Salt needs to be added first.')
        elif self.__password is None:
            raise BrokenPipeError('Password is not set yet.')
        self.__hash = hashlib.sha512(self.__password + self.__salt).hexdigest()

    def encrypt_password(self, master):
        if self.__password is None:
            raise BrokenPipeError('Password has not been set yet.')
        self.__generate_salt()
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=self.__salt, iterations=100000, backend=default_backend())
        key = base64.urlsafe_b64encode(kdf.derive(master.__password))
        f = Fernet(key)
        self.__token = f.encrypt(self.__password)

    def decrypt_password(self, master):
        if self.__token is None:
            raise BrokenPipeError('Password not yet in encrypted form.')
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=self.__salt, iterations=100000, backend=default_backend())
        key = base64.urlsafe_b64encode(kdf.derive(master.__password))
        f = Fernet(key)
        return f.decrypt(self.__token).decode()

    def save_hash(self, saving_string):
        if self.__hash is None:
            raise BrokenPipeError('Password has not been hashed yet.')
        hashed_password = open('../safe/.%shash.dat' % saving_string, 'w')
        hashed_password.write(self.__hash)
        hashed_password.close()

    def save_salt(self, extra_string=''):
        if self.__salt is None:
            raise BrokenPipeError('Salt needs to be added first.')
        salted = open('../safe/.%ssalt.dat' % extra_string, 'wb')
        salted.write(self.__salt)
        salted.close()

    def save_password_object(self, extra_string=''):
        dataframe = pd.DataFrame()
        dataframe['salt'] = [self.__salt]
        dataframe['token'] = [self.__token]
        dataframe['lockout_period_in_hours'] = [self.lockout_period_in_hours]
        dataframe['locked_until'] = [self.locked_until]
        dataframe.to_hdf('../safe/.%s.h' % extra_string, key='data')

    def open_salt(self, extra_string=''):
        salt = open('../safe/.%ssalt.dat' % extra_string, 'rb')
        self.__salt = salt.read()

    @staticmethod
    def open_hash(extra_string=''):
        hash = open('../safe/.%shash.dat' % extra_string, 'r')
        return hash.read()

    def open_password_object(self, extra_string=''):
        data = pd.read_hdf('../safe/.%s.h' % extra_string)
        self.__salt = data['salt'][0]
        self.__token = data['token'][0]
        self.lockout_period_in_hours = data['lockout_period_in_hours'][0]
        self.locked_until = data['locked_until'][0]
        print()

    def set_service(self, service_name):
        while True:
            if (service_name is not None) and (type(service_name) == str) and (len(service_name) != 0):
                self.service_name = service_name
                break

    def calc_locked_until(self):
        now = datetime.datetime.now()
        self.locked_until = now + datetime.timedelta(hours=int(self.lockout_period_in_hours))

    @property
    def service_name(self):
        return self.__service_name

    @service_name.setter
    def service_name(self, service_name):
        if service_name is None:
            pass
        elif len(service_name) == 0:
            self.__printer.service_empty()
        elif type(service_name) != str:
            self.__printer.valid_name()
        else:
            self.__service_name = service_name

