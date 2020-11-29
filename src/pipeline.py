from src.password import Password
from src.printer import Printer
import os
import pandas as pd
import time
import datetime


class Pipeline:
    def __init__(self):
        self.__master = None
        self.printer = Printer()

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

    def __master_password_exists(self):
        return os.path.isfile('../safe/.m_hash.dat') and os.path.isfile('../safe/.m_salt.dat')

    def __check_master_password(self):
        self.printer.check_master_password()
        password_to_check = Password()
        password_to_check.check_validity()
        self.__master = password_to_check

    def __set_master_password(self):
        master = Password()
        self.printer.set_master_password()
        master.set()
        master.hash()
        master.save_hash('m_')
        master.save_salt('m_')
        self.printer.master_password_is_set()

    def __choose_option(self):
        while True:
            self.printer.choose_options()
            self.printer.show_options()
            user_input = input()
            if user_input in self.printer.new_service:
                self.__create_new_service()
                self.__run_normally()
            if user_input in self.printer.retrieve_password:
                self.__retrieve_password()
                self.__run_normally()
            if user_input in self.printer.set_master:
                self.__set_master_password()
                self.__run_normally()
            if user_input in self.printer.exit:
                exit()
            if user_input in self.printer.show_services:
                self.__show_all_services()
                self.__run_normally()
            else:
                self.printer.blank()
                self.printer.incorrect_input()

    def __create_new_service(self):
        password = Password()
        password.service_name = self.__get_service_name()  # TODO: encrypt this name
        password.generate()
        password.encrypt_password(self.__master)
        password.lockout_period_in_hours = self.__get_lockdown_period()
        password.calc_locked_until()
        password.save_password_object(password.service_name)
        self.printer.created_password()

    def __get_service_name(self):
        while True:
            self.printer.tell_service()
            user_input = input()
            if (type(user_input) == str) and (len(user_input) != 0):
                return user_input

    def __get_lockdown_period(self):
        while True:
            self.printer.specify_lockout_period()
            user_input = input()
            if (type(user_input) == str) and (len(user_input) != 0):
                return int(user_input)

    def __retrieve_password(self):
        password = Password()
        service_name = self.__get_service_name()  # TODO: here: check if service available
        password.service_name = service_name
        password.open_password_object(password.service_name)
        if (password.locked_until - datetime.datetime.now() < (datetime.timedelta(hours=int(password.lockout_period_in_hours)) - datetime.timedelta(minutes=5))) and not (password.locked_until < datetime.datetime.now()):
            self.printer.still_locked(until=password.locked_until)
            return
        df = pd.DataFrame([password.decrypt_password(self.__master)])
        df.to_clipboard(index=False, header=False)
        self.printer.copied_password_to_clipboard()
        time.sleep(30)
        df = pd.DataFrame([])
        df.to_clipboard(index=False, header=False)
        self.printer.password_cleared()
        password.calc_locked_until()
        password.save_password_object(password.service_name)

    def __show_all_services(self):
        for file in os.listdir("../safe/"):
            if file.endswith(".h"):
                service_name = file.split('.')[1]
                password = Password()
                password.service_name = service_name
                password.open_password_object(service_name)
                self.printer.service_name_and_locked_until(password)
