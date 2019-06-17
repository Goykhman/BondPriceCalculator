"""

    Calculate values of simple and callable coupon bonds in the random-walk binomial interest rate model.

There are T periods of discrete time, counting the current period t = 0, for which we wish to calculate
the values of coupons.

The bond pays principal P at the last period T - 1, and coupons c * P at periods t = 1, ..., T - 1.

Interest rate at starting period t = 0 is equal to r. It then evolves according to geometric random walk:
during the next period t + 1 it can be either r * exp(s) with probability p, or r * exp(-s) with probability
1 - p. Therefore there are t + 1 possible states of interest rates for the period t. 

Start by calculating nested array "interest" with (T + 1) * T / 2 total  elements. Its element interest[t]
is an array of length t + 1 containing interest rates of period t. By convention interest[t][0] is the largest
possible interest rate r * exp(t * s) of period t.

The algorithm is based on representation of possible states in terms of a triangle on a plane with coordinates
x, y, bounded by the x and y axis, and the line x + y = T - 1. At each level t we have x + y = t, where state
(x, y) = (t, 0) has the interest rate r * exp(t * s).

Callable bond is structured so that at each period one can pay up the principal P instead of the subsequent
series of coupon payments (and P at the end).

The value of bond at each period is calculated just after paying the coupon. Therefore the value of bond at
period T is equal to the principal P.

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

print "Simple coupon value = {}".format(CBOpt1.simpleValues[0][0])
print "Callable coupon value = {}".format(CBOpt1.callableValues[0][0])