import hashlib

class Session:
    def __init__(self, isBuyer, isSeller):
        self.isBuyer = isBuyer
        self.isSeller = isSeller
        self.userID = "NULL"
        self.password = hashlib.sha256(self.userID.encode()).hexdigest()

    def setUserID(self, userID):
        self.userID = userID

    def setIsBuyer(self, arg):
        self.isBuyer = arg

    def setIsSeller(self, arg):
        self.isSeller = arg

    def setHashedPassword(self, password):
        self.password = password

    def returnHashedPassword(self):
        return self.password
    
    def returnUserID(self):
        return self.userID
    
    def returnIsSeller(self):
        return self.isSeller

    def returnIsBuyer(self):
        return self.isBuyer