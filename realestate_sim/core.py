from sympy import symbols, Eq, IndexedBase

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

# IPMT represents the array of yearly interest payments
IPMT = IndexedBase("IPMT", shape=(50,))
# IPMT[i] represents the interest payment for year i+1

rent_monthly, rent_discount = symbols(
    "rent_monthly rent_discount", real=True, positive=True
)
# rent_monthly = monthly rent
# rent_discount = rent discount (fees, taxes, vacancy, etc.)

net_yearly_cashflow = symbols("net_yearly_cashflow", real=True, positive=True)

ALL_VARIABLES = [
    P,
    fn,
    fa,
    full_price,
    w,
    wlev,
    value_after_work,
    dp,
    A,
    r,
    n,
    PMT,
    rent_monthly,
    rent_discount,
    net_yearly_cashflow,
]

# Keep only the core equations
equations = [
    Eq(PMT, A * r / 12 * (1 + r / 12) ** (n * 12) / ((1 + r / 12) ** (n * 12) - 1)),
    Eq(full_price, P * (1 + fn) * (1 + fa)),
    Eq(value_after_work, P + w * wlev),
    Eq(A, full_price + w - dp),
    Eq(net_yearly_cashflow, rent_monthly * 12 * (1 - rent_discount) - PMT * 12),
]


def calculate_ipmt(A, r, n, PMT):
    """Calculate yearly interest payments after main variables are solved."""
    ipmt_values = []
    for i in range(50):
        if i >= n:  # If beyond loan duration, interest payment is 0
            ipmt_values.append(0)
            continue
        # Calculate remaining balance at start of year i
        remaining_balance = A * (1 + r / 12) ** (12 * i) - PMT * (
            (1 + r / 12) ** (12 * i) - 1
        ) / (r / 12)
        # Calculate total interest for the year
        yearly_interest = 0
        monthly_balance = remaining_balance
        for m in range(1, 13):
            # Calculate interest for this month
            monthly_interest = monthly_balance * (r / 12)
            yearly_interest += monthly_interest
            # Update balance for next month (reduce by payment minus interest)
            monthly_balance = monthly_balance - (PMT - monthly_interest)
        ipmt_values.append(float(yearly_interest))
    return ipmt_values
