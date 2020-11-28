import time

class Printer:

    def __init__(self):
        self.newService = ['N', 'n']
        self.retrievePassword = ['R', 'r']
        self.setMaster = ['M', 'm']
        self.exit = ['E', 'e']
        self.showServices = ['S', 's']

    def serviceEmpty(self):
        print('Entered service is empty, please select name.')

    def validName(self):
        print('Please use valid name (letters and numbers).')

    def shortPassword(self):
        print('Please use longer password.')

    def setMasterPassword(self):
        print('Please set master password (>12 characters)')

    def checkMasterPassword(self):
        print('Please enter master password')

    def masterPasswordIsSet(self):
        print('Master password has been changed successfully')

    def incorrectPassword(self):
        print('Incorrect password')

    def showOptions(self):
        print('N: Create new online service password')
        print('R: Retrieve online service password')
        print('M: Set master password')
        print('S: Show all services and lockdown times')
        print('E: Exit')

    def chooseOptions(self):
        print('Please choose one of the following options')

    def incorrectInput(self):
        print('Incorrect input')

    def blank(self):
        print()

    def tellService(self):
        print('Please tell the name of the service.')

    def createdPassword(self):
        print('Password has been created.')

    def copiedPasswordToClipboard(self):
        print('Password copied to clipboard. Will be cleared in 30 seconds.')

    def passwordCleared(self):
        print('Password cleared.')

    def specifyLockdownPeriod(self):
        print('Please specify lockdown period in hours. Suggestion: 72.')

    def stillLocked(self, until=''):
        print('Could not retrieve password, still time-locked until %s.' % until)

    def waitingBar(self):
        print('.', end ="")

    def serviceNameAndLockedUntil(self, password):
        print(password.serviceName + ', locked until: ' + password.lockedUntil.strftime("%m/%d/%Y, %H:%M"))