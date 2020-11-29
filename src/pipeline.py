from src.password import Password
from src.userinput import UserInput
from src.printer import Printer
import os
import pandas as pd
import time
import datetime


class Pipeline:
    def __init__(self):
        self.__master = None
        self.user_input = UserInput()

    def execute(self):
        self.__start_program()
        self.__run_normally()

    def __run_normally(self):
        self.__choose_option()

    def __start_program(self):
        if self.__master_password_exists():
            self.__check_master_password()
        else:
            self.__set_master_password()

    @staticmethod
    def __master_password_exists():
        return os.path.isfile('../safe/.m_hash.dat') and os.path.isfile('../safe/.m_salt.dat')

    def __check_master_password(self):
        Printer.check_master_password()
        password_to_check = Password()
        password_to_check.check_validity()
        self.__master = password_to_check

    @staticmethod
    def __set_master_password():
        master = Password()
        Printer.set_master_password()
        master.set()
        master.hash()
        master.save_hash('m_')
        master.save_salt('m_')
        Printer.master_password_is_set()

    def __choose_option(self):
        while True:
            Printer.choose_options()
            Printer.show_options()
            user_input = input()
            if user_input in self.user_input.new_service:
                self.__create_new_service()
                self.__run_normally()
            if user_input in self.user_input.retrieve_password:
                self.__retrieve_password()
                self.__run_normally()
            if user_input in self.user_input.set_master:
                self.__set_master_password()
                self.__run_normally()
            if user_input in self.user_input.exit:
                exit()
            if user_input in self.user_input.show_services:
                self.__show_all_services()
                self.__run_normally()
            else:
                Printer.blank()
                Printer.incorrect_input()

    def __create_new_service(self):
        password = Password()
        password.service_name = self.__get_service_name()  # TODO: encrypt this name
        password.generate()
        password.encrypt_password(self.__master)
        password.lockout_period_in_hours = self.__get_lockout_period()
        password.calc_locked_until()
        password.save_password_object(password.service_name)
        Printer.created_password()

    @staticmethod
    def __get_service_name():
        while True:
            Printer.tell_service()
            user_input = input()
            if (type(user_input) == str) and (len(user_input) != 0):
                return user_input

    @staticmethod
    def __get_lockout_period():
        while True:
            Printer.specify_lockout_period()
            user_input = input()
            if (type(user_input) == str) and (len(user_input) != 0):
                return int(user_input)

    def __retrieve_password(self):
        password = Password()
        service_name = self.__get_service_name()  # TODO: here: check if service available
        password.service_name = service_name
        password.open_password_object(password.service_name)
        if (password.locked_until - datetime.datetime.now() < (datetime.timedelta(hours=int(password.lockout_period_in_hours)) - datetime.timedelta(minutes=5))) and not (password.locked_until < datetime.datetime.now()):
            Printer.still_locked(until=password.locked_until)
            return
        df = pd.DataFrame([password.decrypt_password(self.__master)])
        df.to_clipboard(index=False, header=False)
        Printer.copied_password_to_clipboard()
        time.sleep(30)
        df = pd.DataFrame([])
        df.to_clipboard(index=False, header=False)
        Printer.password_cleared()
        password.calc_locked_until()
        password.save_password_object(password.service_name)

    @staticmethod
    def __show_all_services():
        for file in os.listdir("../safe/"):
            if file.endswith(".h"):
                service_name = file.split('.')[1]
                password = Password()
                password.service_name = service_name
                password.open_password_object(service_name)
                Printer.service_name_and_locked_until(password)
