import secrets
import string
import os
import hashlib
import base64
import datetime
import getpass
import warnings
import pandas as pd
from printer import Printer
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)



class Password():
    def __init__(self, service=None):
        self.serviceName = service
        self.__printer = Printer()
        self.__password = None
        self.__salt = None
        self.__hash = None
        self.__token = None
        self.lockedUntil = None
        self.lockdownPeriodInHours = 24
        self.__generateSalt()

    def checkPassword(self):
        while True:
            password = getpass.getpass()
            self.__password = bytes(password, 'utf-8')
            self.openSalt('m_')
            self.hash()
            hashToCheck = self.openHash('m_')
            if self.__hash == hashToCheck:
                break
            else:
                self.__printer.incorrectPassword()

    def setPassword(self):
        while True:
            password = getpass.getpass()
            if password is None:
                self.__printer.validName()
            elif len(password) < 12:
                self.__printer.shortPassword()
            elif type(password) != str:
                self.__printer.validName()
            else:
                break
        self.__generateSalt()   # enforce that new salt is created for new password
        self.__password = bytes(password, 'utf-8')

    def generatePassword(self, length=20):
        if int(length) < 12:
            raise AssertionError('Password needs to have minimum length of 12')
        alphabet = string.ascii_letters + string.digits + '#%&$§*_'
        while True:
            password = ''.join(secrets.choice(alphabet) for i in range(int(length)))
            if self.__hasNumbers(password) and self.__hasExtraStrings(password):
                self.__password = bytes(password, 'utf-8')
                self.__generateSalt()  # enforce that new salt is created for new password
                break

    def __hasExtraStrings(self, inputString):
        chars = set('#%&$§*_')
        return any((c in chars) for c in inputString)

    def __hasNumbers(self, inputString):
        return any(char.isdigit() for char in inputString)

    def __generateSalt(self):
        self.__salt = os.urandom(32)

    def hash(self):
        if self.__salt is None:
            raise BrokenPipeError('Salt needs to be added first.')
        elif self.__password is None:
            raise BrokenPipeError('Password is not set yet.')
        self.__hash = hashlib.sha512(self.__password + self.__salt).hexdigest()

    def encryptPassword(self, master):
        if self.__password is None:
            raise BrokenPipeError('Password has not been set yet.')
        self.__generateSalt()
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=self.__salt, iterations=100000, backend=default_backend())
        key = base64.urlsafe_b64encode(kdf.derive(master.__password))
        f = Fernet(key)
        self.__token = f.encrypt(self.__password)

    def decryptPassword(self, master):
        if self.__token is None:
            raise BrokenPipeError('Password not yet in encrypted form.')
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=self.__salt, iterations=100000, backend=default_backend())
        key = base64.urlsafe_b64encode(kdf.derive(master.__password))
        f = Fernet(key)
        return f.decrypt(self.__token).decode()

    def saveHash(self, savingString):
        if self.__hash is None:
            raise BrokenPipeError('Password has not been hashed yet.')
        hashed_password = open('./safe/.%shash.dat' % savingString, 'w')
        hashed_password.write(self.__hash)
        hashed_password.close()

    def saveSalt(self, extraString=''):
        if self.__salt is None:
            raise BrokenPipeError('Salt needs to be added first.')
        salted = open('./safe/.%ssalt.dat' % extraString, 'wb')
        salted.write(self.__salt)
        salted.close()

    def savePasswordObject(self, extraString=''):
        dataframe = pd.DataFrame()
        dataframe['salt'] = [self.__salt]
        dataframe['token'] = [self.__token]
        dataframe['lockdownPeriodInHours'] = [self.lockdownPeriodInHours]
        dataframe['lockedUntil'] = [self.lockedUntil]
        dataframe.to_hdf('./safe/.%s.h' % extraString, key='data')

    def openSalt(self, extraString=''):
        salt = open('./safe/.%ssalt.dat' % extraString, 'rb')
        self.__salt = salt.read()

    def openHash(self, extraString=''):
        hash = open('./safe/.%shash.dat' % extraString, 'r')
        return hash.read()

    def openPasswordObject(self, extraString=''):
        data = pd.read_hdf('./safe/.%s.h' % extraString)
        self.__salt = data['salt'][0]
        self.__token = data['token'][0]
        self.lockdownPeriodInHours = data['lockdownPeriodInHours'][0]
        self.lockedUntil = data['lockedUntil'][0]
        print()

    def setService(self, service):
        while True:
            if (service is not None) and (type(service) == str) and (len(service) != 0):
                self.serviceName = service
                break

    def calcLockedUntil(self):
        now = datetime.datetime.now()
        self.lockedUntil = now + datetime.timedelta(hours=int(self.lockdownPeriodInHours))

    @property
    def serviceName(self):  #TODO: this has changed
        return self.__service

    @serviceName.setter
    def serviceName(self, service):
        if service is None:
            pass
        elif len(service) == 0:
            self.__printer.serviceEmpty()
        elif type(service) != str:
            self.__printer.validName()
        else:
            self.__service = service

