class InsufficientFundsException(Exception): #For insufficient Funds
    def __init__(self, message = "Insufficient Funds in the Account!"):
        self.message = message
        super().__init__(self.message)


class NonExistingBankAccountException(Exception): #To Check a valid account
    def __init__(self, message = "Bank Account does not exist"):
        self.message = message
        super().__init__(self.message)


class InvalidAccountInformationException(Exception): #To Validate an account
    def __init__(self, message="Invalid account information provided"):
        self.message = message
        super().__init__(self.message)