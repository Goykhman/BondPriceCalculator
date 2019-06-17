"""

    Calculate values of simple and callable coupon bonds in the random-walk binomial interest rate model.

"""

class CouponBond:
    
    def __init__(self, T, principal, couponRate, startingInterest, volatility, probUp):
        self.T = T
        self.P = principal
        self.c = couponRate
        self.r = startingInterest
        self.s = volatility
        self.p = probUp
        self.interest = []
        self.simpleValues = []
        self.callableValues = []
        
    def calculateInterest(self):
        self.interest = [[self.r]] # starting interest rate
        for t in range(self.T-1): # go over periods
            childrenInterest = [] # interest rates of period t + 1
            for x in range(t + 1): # go over nodes of given period t
                childrenInterest += [self.interest[t][x] * np.exp(self.s)]
            childrenInterest += [self.interest[t][x] * np.exp(-self.s)]
            self.interest += [childrenInterest]
            
    def calculateValues(self):
        # we start with the known values at the last period T - 1:
        self.simpleValues += [[self.P * (1 + self.c) for _ in range(self.T)]]
        self.callableValues += [[self.P * (1 + self.c) for _ in range(self.T)]]
        for t in range(self.T - 1)[::-1]: # go over periods in reversed order
            simple_values = []
            callable_values = []
            for x in range(t + 1): # go over nodes of given period
                simple_values += [(self.p * (self.c * self.P + self.simpleValues[0][x]) + (1 - self.p) * (self.c * self.P + self.simpleValues[0][x + 1])) / (1 + self.interest[t][x])]
                callable_values += [min(self.P, (self.p * (self.c * self.P + self.callableValues[0][x]) + (1 - self.p) * (self.c * self.P + self.callableValues[0][x + 1]))/ (1 + self.interest[t][x]))]
            # prepend the values:
            self.simpleValues = [simple_values] + self.simpleValues
            self.callableValues = [callable_values] + self.callableValues

'''
    Example:
        30 paying periods (T = 31)
        Principal = 100
        Coupon rate = 9%
        Starting interest rate = 8%
        Interest rate volatility = 16%
        Probability for interest rate to go up = 50%
'''

CB = CouponBond(31, 100, 0.09, 0.08, 0.16, 0.5)

CB.calculateInterest()
CB.calculateValues()

print "Simple bond value = {}".format(CBOpt1.simpleValues[0][0])
print "Callable bond value = {}".format(CBOpt1.callableValues[0][0])