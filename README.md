# BondPriceCalculator
Fast calculator of simple and callable bonds prices

There are T periods of discrete time, counting the current period t = 0, for which we wish to calculate the values of coupons.

The simple bond pays principal P at the last period T - 1, and coupons c * P at periods t = 1, ..., T - 1.

The callable bond can be paid off at each period T: one can exercise the option of repaying the entire principal P at once instead of continuing the future coupon payments.

Interest rate at starting period t = 0 is equal to r. It then evolves according to the geometric random walk: during the next period t + 1 it can be either r * exp(s) with probability p, or r * exp(-s) with probability 1 - p. Therefore there are t + 1 possible states of interest rates for the period t. 

Start by calculating nested array "interest" with (T + 1) * T / 2 total  elements. Its element interest[t] is an array of length t + 1 containing interest rates of period t. By convention interest[t][0] is the largest possible interest rate r * exp(t * s) of period t.

The algorithm is based on representation of possible states in terms of a triangle on a plane with coordinates x, y, bounded by the x and y axis, and the line x + y = T - 1. At each level t we have x + y = t, where state (x, y) = (t, 0) has the interest rate r * exp(t * s).

The value of bond at each period is calculated just after paying the coupon. Therefore the value of bond at period T is equal to the principal P; both for simple and for callable bond. 
