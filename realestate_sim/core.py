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

rent_monthly, rent_discount = symbols(
    "rent_monthly rent_discount", real=True, positive=True
)
# rent_monthly = monthly rent
# rent_discount = rent discount (fees, taxes, vacancy, etc.)

appr = symbols("appr", real=True, positive=True)
# appr = real estate appreciation (e.g 1%)

net_yearly_cashflow = symbols("net_yearly_cashflow", real=True, positive=True)

## ARRAYS ##

# IPMT represents the array of yearly interest payments
IPMT = IndexedBase("IPMT", shape=(50,))
# IPMT[i] represents the interest payment for year i+1

# valuation of the asset
valuation = IndexedBase("valuation", shape=(50,))

# cumulative interest paid
cumulated_interests = IndexedBase("cumulated_interests", shape=(50,))

# principal owed at each year
principal_owed = IndexedBase("principal_owed", shape=(50,))

# capital owned at each year
capital_owned = IndexedBase("capital_owned", shape=(50,))

# revenue at each year
revenue = IndexedBase("revenue", shape=(50,))

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
    appr,
    net_yearly_cashflow,
]

## EQUATIONS ##

# Keep only the core equations (removing valuation equations)
equations = [
    Eq(PMT, A * r / 12 * (1 + r / 12) ** (n * 12) / ((1 + r / 12) ** (n * 12) - 1)),
    Eq(full_price, P * (1 + fn) * (1 + fa)),
    Eq(value_after_work, P + w * wlev),
    Eq(A, full_price + w - dp),
    Eq(net_yearly_cashflow, rent_monthly * 12 * (1 - rent_discount) - PMT * 12),
]


def calculate_valuation(value_after_work, appr):
    """Calculate property valuations over 50 years based on appreciation rate."""
    valuations = []
    for i in range(50):
        yearly_value = value_after_work * (1 + appr) ** i
        valuations.append(float(yearly_value))
    return valuations


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


def calculate_cumulated_interests(ipmt_values):
    """Calculate cumulated interests paid up to each year."""
    cumulated = []
    running_sum = 0
    for interest in ipmt_values:
        running_sum += interest
        cumulated.append(float(running_sum))
    return cumulated


def calculate_principal_owed(A, PMT, cumulated_interests, n):
    """Calculate principal owed at each year."""
    principal = []
    for i in range(50):
        if i >= n:  # If beyond loan duration, nothing is owed
            principal.append(0)
        else:
            # Principal owed = initial loan - (yearly payments - cumulated interests)
            # This is equivalent to: A - i*PMT*12 + cumulated_interests[i]
            # But we need to ensure it's never negative
            yearly_payments = PMT * 12 * (i + 1)
            owed = max(0, A - yearly_payments + cumulated_interests[i])
            principal.append(float(owed))
    return principal


def calculate_capital_owned(valuations, principal_owed):
    """Calculate capital owned at each year."""
    capital = []
    for val, prin in zip(valuations, principal_owed):
        capital.append(float(val - prin))
    return capital


def calculate_revenue(rent_monthly, rent_discount, appr):
    """Calculate yearly revenue over time."""
    yearly_rent = rent_monthly * 12
    net_rent = yearly_rent * (1 - rent_discount)
    revenues = []
    for i in range(50):
        # Revenue increases with property appreciation
        yearly_revenue = net_rent * (1 + appr) ** i
        revenues.append(float(yearly_revenue))
    return revenues
