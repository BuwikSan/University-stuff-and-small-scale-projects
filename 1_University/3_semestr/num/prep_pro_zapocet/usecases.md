# Usecases

## Table of Content
0. [README](README.md)
1. [Usecases](usecases.md)
    - [Numerical Integration](#numerical-integration)
    - [Linear Systems Solvers](#linear-systems-solvers)
    - [Matrix Decomposition](#matrix-decomposition)
    - [Polynomial Interpolation](#polynomial-interpolation)
    - [Polynomial Evaluation](#polynomial_evaluation)
    - [Polynomial Approximation](#polynomial-approximation)
    - [Root Finding](#root-finding)
    - [ODE Solvers](#ode-solvers)
    - [Nonlinear Regression](#nonlinear-regression)

## Numerical Integration

- [MidpointRule](methods.md#midpointrule)  
    Use for a simple and fast estimate of definite integrals, especially when the function is smooth and you want a quick, reasonably accurate result. Works best for functions without sharp changes over the interval.
- [SimpsonRule](methods.md#simpsonrule)  
    Use for higher accuracy on smooth functions, especially polynomials up to degree three. Requires an even number of subintervals. Generally more accurate than the midpoint or trapezoidal rule for the same number of intervals.

## Linear Systems Solvers

- [Gauss](methods.md#gauss)  
    Use for small to medium-sized, well-conditioned linear systems where you don’t expect zeros or very small numbers on the diagonal. It’s a direct method (gives an exact solution in finite steps).
- [GaussPivot](methods.md#gausspivot)  
    Use when your system might have zeros or very small values on the diagonal, or if you want better numerical stability. Partial pivoting helps avoid division by small numbers and reduces rounding errors.
- [GaussSeidel](methods.md#gaussseidel)  
    Use for large, sparse, or diagonally dominant systems. It’s an iterative method, so it’s good when you don’t need exact precision or when the system is too big for direct methods. Often converges faster than Jacobi.
- [Jacobi](methods.md#jacobi)  
    Use for large, sparse, or diagonally dominant systems, especially if you want a simple, parallelizable iterative method. It’s less efficient than Gauss-Seidel but easier to implement in parallel.

## Matrix Decomposition

- [GaussLU](methods.md#gausslu)  
    Use when you want to perform LU decomposition using Gaussian elimination and return a new matrix containing both L and U factors, leaving the original matrix unchanged. Good for functional-style code or when you need to preserve the input.
- [LUDecompose](methods.md#ludecompose)  
    Use when you want to decompose a matrix in-place for memory efficiency, especially in object-oriented code. This method modifies the original matrix to store the LU factors directly.

## Polynomial Interpolation

- [Lagrange](methods.md#lagrange)  
    Use for a straightforward, formula-based approach to interpolation. Good for small datasets and when you want a direct mathematical expression, but not efficient for repeated evaluations or large numbers of points.
- [Vandermonde](methods.md#vandermonde)  
    Use when you want to solve for polynomial coefficients by setting up and solving a linear system with a Vandermonde matrix. Suitable for small systems, but can be numerically unstable for large datasets or closely spaced points.
- [NewtonInterpolation](methods.md#newtoninterpolation)  
    Use when you want efficient, incremental interpolation—especially if you may add new data points later. Newton’s method is numerically stable and allows for fast evaluation using divided differences.

## Polynomial Evaluation

- [Horner](methods.md#horner)  
    Use for fast and numerically stable evaluation of polynomials in standard (power) form. Ideal when you have explicit coefficients for ( a_0 + a_1x + a_2x^2 + ... ).
- [NewtonEvaluation](methods.md#newtonevaluation)  
    Use for efficient evaluation of polynomials in Newton’s form, especially when you have divided difference coefficients from Newton interpolation. Useful if you’re working with Newton’s method or need to add points incrementally.

## Polynomial Approximation
 
- [Least Squares Approximation (LSA)](methods.md#least-squares-approximation-lsa)  
    Use when you want to fit a polynomial (or other function) to data that may not be exactly interpolatable, especially if you have noisy measurements or more data points than the degree of the polynomial. LSA finds the polynomial that minimizes the sum of squared differences between the data and the fit, making it ideal for trend estimation, data smoothing, or regression analysis. It does not guarantee the curve passes through all points, but provides the best overall fit in the least squares sense.
- [Least Squares Solver (LSS)](methods.md#lss)  
    Use when you need to solve a general linear least squares problem \(A\vec{x} = \vec{y}\), not limited to polynomials. LSS finds the vector \(\vec{x}\) that minimizes the sum of squared residuals, making it suitable for fitting any linear model to data, including but not limited to polynomial regression, trend estimation, and overdetermined systems.
- [NonlinearFit](methods.md#nonlinearfit)  
    Use when you need to fit a nonlinear model (such as \( a(p) = a_m \frac{b p}{1 + b p} \)) to experimental data. NonlinearFit minimizes the sum of squared errors between the model and the data, making it suitable for parameter estimation in nonlinear systems, curve fitting in physical sciences, and modeling real-world phenomena that cannot be captured by polynomials alone.

## Root Finding

- [Bisection](methods.md#bisection)  
    Use when you need to find a root of a continuous function in a known interval where the function changes sign. Bisection is robust and guarantees convergence if the function is continuous and the initial interval brackets a root. Ideal for simple, reliable root finding when speed is less critical than certainty.

## ODE Solvers

- [EulerStep](methods.md#eulerstep)  
    Use for numerically solving ordinary differential equations (ODEs) of the form \( y' = f(x, y) \) with a given initial value. Euler’s method is simple and fast, suitable for problems where high accuracy is not required or as a first step before using more advanced ODE solvers.

## Nonlinear Regression

- [NonlinearFit](methods.md#nonlinearfit)  
    Use when you need to fit a nonlinear model to data, such as in physical sciences, biology, or engineering. NonlinearFit is ideal for parameter estimation in models that are not linear in their parameters, especially when the relationship between variables is complex or follows a known nonlinear law.
