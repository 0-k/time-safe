from password import Password
from printer import Printer
import os
import pandas as pd
import time
import datetime

class Pipeline():
    def __init__(self):
        self.__master = None
        self.printer = Printer()

    def execute(self):
        self.__startProgram()
        self.__runNormally()

    def __runNormally(self):
        self.__chooseOption()

    def __startProgram(self):
        if self.__masterPasswordExists():
            self.__checkMasterPassword()
        else:
            self.__setMasterPassword()

    def __masterPasswordExists(self):
        return os.path.isfile('./safe/.m_hash.dat') and os.path.isfile('./safe/.m_salt.dat')

    def __checkMasterPassword(self):
        self.printer.checkMasterPassword()
        passwordToCheck = Password()
        passwordToCheck.checkPassword()
        self.__master = passwordToCheck

    def __setMasterPassword(self):
        master = Password()
        self.printer.setMasterPassword()
        master.setPassword()
        master.hash()
        master.saveHash('m_')
        master.saveSalt('m_')
        self.printer.masterPasswordIsSet()

    def __chooseOption(self):
        while True:
            self.printer.chooseOptions()
            self.printer.showOptions()
            userInput = input()
            if userInput in self.printer.newService:
                self.__createNewService()
                self.__runNormally()
            if userInput in self.printer.retrievePassword:
                self.__retrievePassword()
                self.__runNormally()
            if userInput in self.printer.setMaster:
                self.__setMasterPassword()
                self.__runNormally()
            if userInput in self.printer.exit:
                exit()
            if userInput in self.printer.showServices:
                self.__showAllServices()
                self.__runNormally()
            else:
                self.printer.blank()
                self.printer.incorrectInput()

    def __createNewService(self):
        password = Password()
        password.serviceName = self.__getServiceName()  # TODO: encrypt this name
        password.generatePassword()
        password.encryptPassword(self.__master)
        password.lockdownPeriodInHours = self.__getLockdownPeriod()
        password.calcLockedUntil()
        password.savePasswordObject(password.serviceName)
        self.printer.createdPassword()

    def __getServiceName(self):
        while True:
            self.printer.tellService()
            userInput = input()
            if (type(userInput) == str) and (len(userInput) != 0):
                return userInput

    def __getLockdownPeriod(self):
        while True:
            self.printer.specifyLockdownPeriod()
            userInput = input()
            if (type(userInput) == str) and (len(userInput) != 0):
                return int(userInput)

    def __retrievePassword(self):
        password = Password()
        serviceName = self.__getServiceName()  # TODO: here: check if service available
        password.serviceName = serviceName
        password.openPasswordObject(password.serviceName)
        if (password.lockedUntil - datetime.datetime.now() < (datetime.timedelta(hours=int(password.lockdownPeriodInHours)) - datetime.timedelta(minutes=5))) and not (password.lockedUntil < datetime.datetime.now()):
            self.printer.stillLocked(until=password.lockedUntil)
            return
        df = pd.DataFrame([password.decryptPassword(self.__master)])
        df.to_clipboard(index=False, header=False)
        self.printer.copiedPasswordToClipboard()
        time.sleep(30)
        df = pd.DataFrame([])
        df.to_clipboard(index=False, header=False)
        self.printer.passwordCleared()
        password.calcLockedUntil()
        password.savePasswordObject(password.serviceName)

    def __showAllServices(self):
        for file in os.listdir("./safe/"):
            if file.endswith(".h"):
                serviceName = file.split('.')[1]
                password = Password()
                password.serviceName = serviceName
                password.openPasswordObject(serviceName)
                self.printer.serviceNameAndLockedUntil(password)
