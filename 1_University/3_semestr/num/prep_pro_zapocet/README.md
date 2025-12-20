# KI-NUM

## Table of Content
1. [**Usecases**](usecases.md)
    - [Numerical Integration](usecases.md#numerical-integration)
    - [Linear Systems Solvers](usecases.md#linear-systems-solvers)
    - [Matrix Decomposition](usecases.md#matrix-decomposition)
    - [Polynomial Interpolation](usecases.md#polynomial-interpolation)
    - [Polynomial Evaluation](usecases.md#polynomial_evaluation)
    - [Polynomial Approximation](usecases.md#polynomial-approximation)
    - [Root Finding](usecases.md#root-finding)
    - [ODE Solvers](usecases.md#ode-solvers)
    - [Nonlinear Regression](usecases.md#nonlinear-regression)
2. [**Methods**](methods.md)
    - [Midpointrule](methods.md#midpointrule)
    - [Gauss](methods.md#gauss)
    - [GaussPivot](methods.md#gausspivot)
    - [GaussLU](methods.md#gausslu)
    - [GaussSeidel](methods.md#gaussseidel)
    - [Jacobi](methods.md#jacobi)
    - [LUDecompose](methods.md#ludecompose)
    - [Lagrange](methods.md#lagrange)
    - [Vandermonde](methods.md#vandermonde)
    - [Horner](methods.md#horner)
    - [NewtonInterpolation](methods.md#newtoninterpolation)
    - [NewtonEvaluation](methods.md#newtonevaluation)
    - [SimpsonRule](methods.md#simpsonrule)
    - [Least Squares Approximation (LSA)](methods.md#least-squares-approximation-lsa)
    - [Bisection](methods.md#bisection)
    - [EulerStep](methods.md#eulerstep)
    - [NonlinearFit](methods.md#nonlinearfit)
    - [Least Squares Solution (LSS)](methods.md#least-squares-solution-lss)
3. [**Documents**](#documents)

## Quick Guide: How to Choose Numerical Methods

This guide helps you quickly recognize which numerical method to use for typical computational and exam problems. It summarizes the main clues and recommended routines from the KI-NUM toolkit.

---

### 1. Numerical Integration

**Clues:**  
- Integral sign (∫), area under a curve, estimate a definite integral, analyze error vs. n.

**Examples:**  
- “Compute ∫₁² (1/x) dx using Newton-Cotes, plot error.”

**Recommended Methods:**  
- `SimpsonRule`
- `MidpointRule`
- `TrapezoidalRule`

---

### 2. Solving Linear Systems (Ax = b)

**Clues:**  
- Matrix equation Ax = b, "solve for x", matrix entries defined by integrals.

**Examples:**  
- “Solve Ax = b where A_ij = ∫₀¹ t^{i+j-2} dt.”

**Recommended Methods:**  
- `Gauss`
- `GaussPivot`
- `GaussSeidel`
- `Jacobi`

---

### 3. Interpolation

**Clues:**  
- "Find a polynomial through all data points", "interpolate", curve must pass through all given points.

**Examples:**  
- “Fit a polynomial exactly through given data, plot result.”

**Recommended Methods:**  
- `Lagrange`
- `NewtonInterpolation`
- `Vandermonde`

---

### 4. Approximation / Regression / Least Squares

**Clues:**  
- “Best fit”, “approximate”, “regression”, “trend”, “minimize sum of squared errors”, noisy data.

**Examples:**  
- “Fit a polynomial of degree 2 to experimental data.”

**Recommended Methods:**  
- `LSA` (Least Squares Approximation)
- `LSS` (Least Squares Solution)

---

### 5. Nonlinear Fit / Parameter Estimation

**Clues:**  
- “Fit a nonlinear model”, e.g. a(p) = am * bp / (1+bp), “estimate model parameters”.

**Examples:**  
- “Fit a(p) model to data, estimate am and b.”

**Recommended Methods:**  
- `NonlinearFit`

---

### 6. Root Finding

**Clues:**  
- “Find where f(x)=0”, “find intersection”, “where do two curves cross”.

**Examples:**  
- “Find x such that f(x) = 0”, or intersection of two fitted curves.

**Recommended Methods:**  
- `Bisection`
- (Newton/Secant if implemented)

---

### 7. Practical Decision Table

| Problem Type         | Keywords / Signs                   | Use These Methods         |
|----------------------|------------------------------------|--------------------------|
| Definite Integral    | ∫, area under curve, “estimate”   | SimpsonRule, MidpointRule, TrapezoidalRule |
| Linear System        | Ax = b, solve for x               | Gauss, GaussPivot, GaussSeidel, Jacobi     |
| Interpolation        | through all points, “interpolate” | Lagrange, NewtonInterpolation, Vandermonde |
| Approximation/Trend  | “Best fit”, regression, trend     | LSA, LSS                 |
| Nonlinear Fit        | Model with parameters, a(p), etc. | NonlinearFit             |
| Root/Intersection    | f(x)=0, intersection, “crosses”   | Bisection                |

---

### 8. Quick Decision Flow

- **Exact fit through all points?** → Use Interpolation methods.
- **Best fit/trend (not exact)?** → Use Regression/Approximation.
- **System of equations?** → Use Linear Solvers.
- **Integral/area under curve?** → Use Numerical Integration.
- **Root/intersection/zero?** → Use Root Finding.
- **Estimate parameters in a nonlinear formula?** → Use NonlinearFit.

---