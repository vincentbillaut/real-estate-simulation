from sympy import symbols, Eq, nsolve
from core import *
from config import assumptions
from scenarios import test_scenario


def solve_scenario(scenario_assumptions):
    """
    Solve the real estate scenario with given assumptions.

    Args:
        scenario_assumptions (dict): Dictionary of known variable values

    Returns:
        dict: All variable values after solving
    """
    # Combine default assumptions with scenario-specific ones
    all_assumptions = assumptions.copy()
    all_assumptions.update(scenario_assumptions)

    # Create a list of equations to solve
    eqs_to_solve = equations.copy()

    # Create initial guess for variables
    initial_guess = {
        P: 300000,  # Default purchase price
        fn: 0.08,  # Default notary fees
        fa: 0.05,  # Default agency fees
        w: 50000,  # Default work value
        dp: 60000,  # Default down payment
    }

    # Update initial guess with known values
    initial_guess.update(all_assumptions)

    # First substitute known values in equations
    substituted_eqs = []
    for eq in eqs_to_solve:
        new_eq = eq
        for var, value in all_assumptions.items():
            new_eq = new_eq.subs(var, value)
        substituted_eqs.append(new_eq)

    # Create a list of variables to solve for (only unknowns)
    variables = []
    for var in [
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
    ]:
        if var not in all_assumptions:
            variables.append(var)

    # Create initial values for unknown variables
    initial_values = [initial_guess.get(var, 1.0) for var in variables]

    print("Equations to solve:", substituted_eqs)
    print("Variables to solve for:", variables)
    print("Initial values:", initial_values)

    # Solve the system of equations
    solution = nsolve(substituted_eqs, variables, initial_values)

    # Create result dictionary starting with known values
    result = all_assumptions.copy()

    # Add solved values
    for var, val in zip(variables, solution):
        result[var] = float(val)

    return result


def print_results(results):
    """Print the results in a readable format."""
    print("\nReal Estate Scenario Results:")
    print("=" * 30)

    print(f"Purchase Price (P): €{results[P]:,.2f}")
    print(f"Notary Fees (fn): {results[fn]*100:.1f}%")
    print(f"Agency Fees (fa): {results[fa]*100:.1f}%")
    print(f"Full Price: €{results[full_price]:,.2f}")
    print(f"Work Value (w): €{results[w]:,.2f}")
    print(f"Work Value Leverage (wlev): {results[wlev]:.1f}x")
    print(f"Value After Work: €{results[value_after_work]:,.2f}")
    print(f"Down Payment (dp): €{results[dp]:,.2f}")
    print(f"Loan Amount (A): €{results[A]:,.2f}")
    print(f"Interest Rate (r): {results[r]*100:.1f}%")
    print(f"Loan Duration (n): {results[n]:.0f} years")
    print(f"Monthly Payment (PMT): €{results[PMT]:,.2f}")
    print(f"Monthly Rent: €{results[rent_monthly]:,.2f}")
    print(f"Rent Discount: {results[rent_discount]*100:.1f}%")
    print(f"Net Yearly Cashflow: €{results[net_yearly_cashflow]:,.2f}")


if __name__ == "__main__":
    # Example scenario
    results = solve_scenario(test_scenario)
    print_results(results)
