class Printer:
    @staticmethod
    def service_empty():
        print('Entered service is empty, please select name.')

    @staticmethod
    def valid_name():
        print('Please use valid name (letters and numbers).')

    @staticmethod
    def short_password():
        print('Please use longer password.')

    @staticmethod
    def set_master_password():
        print('Please set master password (>12 characters)')

    @staticmethod
    def check_master_password():
        print('Please enter master password')

    @staticmethod
    def master_password_is_set():
        print('Master password has been changed successfully')

    @staticmethod
    def incorrect_password():
        print('Incorrect password')

    @staticmethod
    def show_options():
        print('N: New online service password')
        print('R: Retrieve online service password')
        # print('M: Master password reset')  # TODO: implement master password reset properly,
        print('S: Show all services and lockout times')
        print('E: Exit')

    @staticmethod
    def choose_options():
        print('Please choose one of the following options')

    @staticmethod
    def incorrect_input():
        print('Incorrect input')

    @staticmethod
    def blank():
        print()

    @staticmethod
    def tell_service():
        print('Please tell the name of the service.')

    @staticmethod
    def created_password():
        print('Password has been created.')

    @staticmethod
    def copied_password_to_clipboard():
        print('Password copied to clipboard. Will be cleared in 30 seconds.')

    @staticmethod
    def password_cleared():
        print('Password cleared.')

    @staticmethod
    def specify_lockout_period():
        print('Please specify lockout period in hours. Suggestion: 72.')

    @staticmethod
    def still_locked(until=''):
        print('Could not retrieve password, still time-locked until %s.' % until)

    @staticmethod
    def waiting_bar():
        print('.', end ="")

    @staticmethod
    def service_name_and_locked_until(password):
        print(password.service_name + ', locked until: ' + password.locked_until.strftime("%m/%d/%Y, %H:%M"))