from sympy import symbols, Eq

# PARAMETERS
P, fn, fa, full_price = symbols("P fn fa full_price", real=True, positive=True)
# P = purchase price
# fn = frais de notaire
# fa = frais d'agence

w, wlev, value_after_work = symbols("w wlev value_after_work", real=True, positive=True)
# w = work value
# wlev = work value leverage
# value_after_work = value after work

dp, A, r, n, PMT = symbols("dp A r n PMT", real=True, positive=True)
# dp = down payment
# A = loan amount
# r = interest rate
# n = number of years
# PMT = monthly payment

rent_monthly, rent_discount = symbols(
    "rent_monthly rent_discount", real=True, positive=True
)
# rent_monthly = monthly rent
# rent_discount = rent discount (fees, taxes, vacancy, etc.)

net_yearly_cashflow = symbols("net_yearly_cashflow", real=True, positive=True)

equations = [
    Eq(PMT, A * r / 12 * (1 + r / 12) ** (n * 12) / ((1 + r / 12) ** (n * 12) - 1)),
    Eq(full_price, P * (1 + fn) * (1 + fa)),
    Eq(value_after_work, P + w * wlev),
    Eq(A, full_price + w - dp),
    Eq(net_yearly_cashflow, rent_monthly * 12 * (1 - rent_discount) - PMT * 12),
]
