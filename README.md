# real-estate-simulation

This project models real estate investment scenarios by encoding financial relationships (e.g., down payment, loan terms, rent, fees) and allowing both forward and reverse analysis of outcomes like **annualized return rates**.

### 🔧 Key Features
- **Symbolic modeling** using `SymPy` for transparent algebraic relationships (e.g., loan payments, returns, cap rates).
- **Numerical solving** with `scipy.optimize` for inverting complex functions (e.g., solving for interest rate given monthly payment).
- Easily plug in parameters like purchase price, down payment, interest rate, or rent, and analyze results.
- Run simulations to explore or optimize variables (e.g., "what rent makes this deal hit a 10% return?").

### 💡 Example Use Cases
- Calculate monthly payments from loan terms
- Solve for required rent to achieve target ROI
- Analyze sensitivity to down payment or interest rate
- Backsolve interest rate from known loan + payment