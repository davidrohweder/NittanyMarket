import hashlib

class Session:
    def __init__(self, isBuyer, isSeller, isVendor, isReady):
        self.isBuyer = isBuyer
        self.isSeller = isSeller
        self.isVendor = isVendor
        self.isReady = isReady
        self.userID = "NULL"
        self.password = hashlib.sha256(self.userID.encode()).hexdigest()

    
    def setIsReady(self, arg):
        self.isReady = arg 

    def setUserID(self, userID):
        self.userID = userID

    def setIsBuyer(self, arg):
        self.isBuyer = arg

    def setIsVendor(self, arg):
        self.isVendor = arg

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

    def returnIsVendor(self):
        return self.isVendor

    def returnIsReady(self):
        return self.isReady