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
    for var in ALL_VARIABLES:
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

    # Calculate IPMT values after solving main system
    result[IPMT] = calculate_ipmt(result[A], result[r], result[n], result[PMT])

    # Calculate valuation over time after solving main system
    result[valuation] = calculate_valuation(result[value_after_work], result[appr])

    # Calculate cumulated interests
    result[cumulated_interests] = calculate_cumulated_interests(result[IPMT])

    # Calculate principal owed
    result[principal_owed] = calculate_principal_owed(
        result[A], result[PMT], result[cumulated_interests], result[n]
    )

    # Calculate capital owned
    result[capital_owned] = calculate_capital_owned(
        result[valuation], result[principal_owed]
    )

    # Calculate revenue
    result[revenue] = calculate_revenue(
        result[rent_monthly], result[rent_discount], result[appr]
    )

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
    print(f"Appreciation rate: {results[appr]*100:.1f}%")

    print("\nTemporal Analysis:")
    print("=" * 30)
    # Print the data in a table format with columns
    print(
        f"{'Year':<5} {'Property Value':<15} {'Principal Owed':<15} {'Capital Owned':<15} {'Revenue':<15} {'Interest Paid':<15} {'Cumulative Interest':<20}"
    )
    print("-" * 100)

    # Print data for specific years (0, 5, 10, 15, 20, 25, 30)
    years_to_display = [0, 5, 10, 15, 20, 25, 30]
    for year in years_to_display:
        if year < 50:  # Ensure we don't go beyond our data
            print(
                f"{year:<5} "
                + f"€{results[valuation][year]:,.2f}".ljust(15)
                + " "
                + f"€{results[principal_owed][year]:,.2f}".ljust(15)
                + " "
                + f"€{results[capital_owned][year]:,.2f}".ljust(15)
                + " "
                + f"€{results[revenue][year]:,.2f}".ljust(15)
                + " "
                + (
                    f"€{results[IPMT][year]:,.2f}".ljust(15)
                    if year < len(results[IPMT])
                    else "€0.00".ljust(15)
                )
                + " "
                + f"€{results[cumulated_interests][year]:,.2f}".ljust(20)
            )

    # Calculate total interest paid
    total_interest = sum(results[IPMT])
    print(f"\nTotal interests paid over the loan duration: €{total_interest:,.2f}")


if __name__ == "__main__":
    # Example scenario
    results = solve_scenario(test_scenario)
    print_results(results)
