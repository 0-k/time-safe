class Printer:

    def __init__(self):
        self.new_service = ['N', 'n']
        self.retrieve_password = ['R', 'r']
        self.set_master = ['M', 'm']
        self.exit = ['E', 'e']
        self.show_services = ['S', 's']

    def service_empty(self):
        print('Entered service is empty, please select name.')

    def valid_name(self):
        print('Please use valid name (letters and numbers).')

    def short_password(self):
        print('Please use longer password.')

    def set_master_password(self):
        print('Please set master password (>12 characters)')

    def check_master_password(self):
        print('Please enter master password')

    def master_password_is_set(self):
        print('Master password has been changed successfully')

    def incorrect_password(self):
        print('Incorrect password')

    def show_options(self):
        print('N: New online service password')
        print('R: Retrieve online service password')
        print('M: Master password reset')
        print('S: Show all services and lockout times')
        print('E: Exit')

    def choose_options(self):
        print('Please choose one of the following options')

    def incorrect_input(self):
        print('Incorrect input')

    def blank(self):
        print()

    def tell_service(self):
        print('Please tell the name of the service.')

    def created_password(self):
        print('Password has been created.')

    def copied_password_to_clipboard(self):
        print('Password copied to clipboard. Will be cleared in 30 seconds.')

    def password_cleared(self):
        print('Password cleared.')

    def specify_lockout_period(self):
        print('Please specify lockout period in hours. Suggestion: 72.')

    def still_locked(self, until=''):
        print('Could not retrieve password, still time-locked until %s.' % until)

    def waiting_bar(self):
        print('.', end ="")

    def service_name_and_locked_until(self, password):
        print(password.service_name + ', locked until: ' + password.locked_until.strftime("%m/%d/%Y, %H:%M"))