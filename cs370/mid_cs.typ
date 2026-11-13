#set page(
  paper: "a4",
  margin: (x: 0.8cm, y: 0.55cm),
  columns: 2,
)
#set text(size: 8pt, font: "New Computer Modern")
#set par(justify: true, leading: 0.45em, spacing: 0.45em)
#show heading.where(level: 1): it => block(
  fill: rgb("#dbe5f5"),
  inset: (x: 5pt, y: 2.5pt),
  radius: 2pt,
  width: 100%,
  above: 6pt,
  below: 3pt,
  text(weight: "bold", size: 9.5pt, it.body),
)
#show heading.where(level: 2): it => block(
  above: 5pt,
  below: 1.5pt,
  stroke: (left: 2pt + rgb("#8fb0e0")),
  inset: (left: 5pt),
  text(weight: "bold", size: 8.5pt, it.body),
)

= Preliminaries

- *Taylor series* of $f$ about $a$:
  $ f(x) = sum_(n=0)^infinity (f^((n))(a))/(n!) (x - a)^n $

= Floating-Point Systems

System $\{beta, t, L, U\}$: base $beta$, $t$ digits, exponent range $L <= p <= U$. Represents
$ plus.minus 0. d_1 d_2 dots.c d_t times beta^p $
- *Real $x$ to floating point*: (1) express $x$ in base $beta$; (2) normalize to $plus.minus bar(x) times beta^p$ so $bar(x)$ starts with $0.$; (3) round (nearest) or truncate / chop $bar(x)$ to $t$ digits.
- *Underflow*: exponent $p$ too small. *Overflow*: exponent $p$ too large.
- IEEE single: $t = 24$ ($1 + 23$ fraction bits), $L = -125$, $U = 128$; layout sign (1) | exp (8) | fraction (23).
- IEEE double: $t = 53$ ($1 + 52$), $L = -1021$, $U = 1024$; layout sign (1) | exp (11) | fraction (52).

== Errors
- $E_"abs" = |x_"exact" - x_"approx"|$
- $E_"rel" = (|x_"exact" - x_"approx"|)/(|x_"exact"|)$; a result is roughly correct to $s$ digits if $E_"rel" approx 10^(-s)$.
- *Machine epsilon* $epsilon$: the smallest value with $op("fl")(1 + epsilon) > 1$; when rounding $epsilon = 1/2 beta^(1-t)$, when truncating $epsilon = beta^(1-t)$.
- $op("fl")(x) = x (1 + delta)$ with $|delta| <= epsilon$, and $w ⊕ z = op("fl")(w + z) = (w + z)(1 + delta)$.
- FP arithmetic is *not associative*; to minimize error, sum numbers of approximately the same size and sign.
- *Cancellation*: differing signs with similar magnitudes give large $E_"rel"$; adding large + small numbers swamps the smaller digits; subtracting nearby numbers amplifies error.
- *Ill-conditioned*: small $Delta I arrow.r$ large $Delta O$ (opposite: well-conditioned). *Stable algorithm*: initial error is not magnified.

= Interpolation

- *Vandermonde*: fit an $(n-1)$-degree polynomial to $(x_1, y_1), dots.c, (x_n, y_n)$ by solving for its $n$ coefficients:
  $ mat(1, x_1, dots.c, x_1^(n-1); dots.v, dots.v, dots.down, dots.v; 1, x_n, dots.c, x_n^(n-1)) vec(c_1, dots.v, c_n) = vec(y_1, dots.v, y_n) $
  $V$ is a Vandermonde matrix: nonsingular for distinct $x_i$, so always solvable.
- *Monomial basis*: $\{1, x, x^2, dots.c, x^(n-1)\}$ (degree $<= n-1$, $n$ coefficients).
- *Lagrange basis*:
  $ p(x) = sum_(k=1)^n y_k L_k (x), quad L_k (x) = product_(j != k) (x - x_j)/(x_k - x_j) $
  the $k$-th factor is omitted from both products; $L_i (x_j) = delta_(i,j)$.

== Hermite & splines
- Notation: $Delta x_i = x_(i+1) - x_i$; secant slope $y'_i = (y_(i+1) - y_i)/(Delta x_i)$; $s_i$ = given slope at $x_i$.
- *2-point Hermite* on $[x_i, x_(i+1)]$:
  $ p_i (x) = a_i + b_i (x - x_i) + c_i (x - x_i)^2 + d_i (x - x_i)^3 $
  $ a_i = y_i, quad b_i = s_i, quad c_i = (3y'_i - 2s_i - s_(i+1))/(Delta x_i), quad d_i = (s_(i+1) + s_i - 2y'_i)/(Delta x_i)^2 $
- *Cubic spline*: piecewise cubic with $C^2$ continuity,
  $ S_i (x_i) = y_i, quad S_i (x_(i+1)) = y_(i+1), quad S'_i (x_(i+1)) = S'_(i+1)(x_(i+1)), quad S''_i (x_(i+1)) = S''_(i+1)(x_(i+1)) $
- Solve the slope system for $i = 2, dots.c, n-1$:
  $ Delta x_i s_(i-1) + 2(Delta x_(i-1) + Delta x_i) s_i + Delta x_(i-1) s_(i+1) = 3(Delta x_i y'_(i-1) + Delta x_(i-1) y'_i) $
- Boundary conditions:
  - *Clamped*: $S'(x_1) = s_1$ and $S'(x_n) = s_n$ specified.
  - *Free / natural*: $S''(x_1) = S''(x_n) = 0$, adding $s_1 + s_2/2 = 3/2 y'_1$ and $s_(n-1)/2 + s_n = 3/2 y'_(n-1)$.
  - *Periodic*: $S'(x_1) = S'(x_n)$, $S''(x_1) = S''(x_n)$; *not-a-knot*: $S'''_1 (x_2) = S'''_2 (x_2)$, $S'''_(n-2)(x_(n-1)) = S'''_(n-1)(x_(n-1))$.
- After solving for the slopes $s_i$, plug them into the Hermite formula. *Knots*: points where the piecewise polynomials join.

== Parametric curves
- Coordinates as functions of $t$: $(x(t), y(t))$; parametric splines need not be functions.
- *Arc-length parameterization*: choose $t$ = distance along the curve,
  $ t_(i+1) = t_i + norm(p_i - p_(i+1))_2, quad t_1 = 0 $ (or simply $t_i = i$).

= Ordinary Differential Equations

- *IVP*: $y'(t) = f(t, y(t))$, $y(t_0) = y_0$; find $y_i approx y(t_i)$.
- *Local truncation error*: $|y_(n+1) - y(t_(n+1))|$ assuming exact data $y_n = y(t_n)$.
- *Global error*: $|y_n - y(t_n)|$; $"GE" <= "LE" dot O(h^(-1))$, i.e. one order lower than the LTE.
- *Time-stepping*: explicit vs implicit; single-step vs multistep; fixed vs variable $h$; equivalently "integrating" $y'(t)$.
- *Higher-order ODEs*: for $y^((n))(t) = f(t, y, y', dots.c, y^((n-1)))$, set $y_i = y^((i-1))$ and solve $y'_i = y_(i+1)$, $y'_n = f(t, y_1, dots.c, y_(n-1))$.

== One-step / Runge-Kutta methods
- *Forward Euler* (explicit; LTE $O(h^2)$; stable iff $h < 2/lambda$, rectangular integration):
  $ y_(n+1) = y_n + h f(t_n, y_n) $
- *Improved Euler* (explicit, predictor-corrector; LTE $O(h^3)$; $h < 2/lambda$):
  $ y^*_(n+1) = y_n + h f(t_n, y_n) \
    y_(n+1) = y_n + h/2 [f(t_n, y_n) + f(t_(n+1), y^*_(n+1))] $
- *Trapezoidal / Crank-Nicolson* (implicit; LTE $O(h^3)$; unconditionally stable, trapezoidal integration):
  $ y_(n+1) = y_n + h/2 [f(t_n, y_n) + f(t_(n+1), y_(n+1))] $
- *Backward (implicit) Euler / BDF1* (implicit; LTE $O(h^2)$; unconditionally stable; root-finding each step):
  $ y_(n+1) = y_n + h f(t_(n+1), y_(n+1)) $
- *Explicit midpoint* (explicit RK; LTE $O(h^3)$):
  $ k_1 = h f(t_n, y_n), quad k_2 = h f(t_n + h/2, y_n + k_1/2) $
  $ y_(n+1) = y_n + k_2 $
- *Fourth-order Runge-Kutta (RK4)* (explicit; LTE $O(h^5)$):
  $ k_1 = h f(t_n, y_n) \
    k_2 = h f(t_n + h/2, y_n + k_1/2) \
    k_3 = h f(t_n + h/2, y_n + k_2/2) \
    k_4 = h f(t_n + h, y_n + k_3) \
    y_(n+1) = y_n + 1/6 (k_1 + 2k_2 + 2k_3 + k_4) $

== Multistep methods
- *BDF2* (implicit, multistep; LTE $O(h^3)$):
  $ y_(n+1) = 4/3 y_n - 1/3 y_(n-1) + 2/3 h f(t_(n+1), y_(n+1)) $
- *Adams-Bashforth (AB2)* (explicit, multistep; LTE $O(h^3)$):
  $ y_(n+1) = y_n + h/2 [3 f(t_n, y_n) - f(t_(n-1), y_(n-1))] $
- *Deriving BDF*: (1) fit a Lagrange interpolant $p$ to $(t_(n-s+1), y_(n-s+1)), dots.c, (t_n, y_n)$; (2) require $p'(t_(n+1)) = f(t_(n+1), y_(n+1))$; (3) rearrange for $y_(n+1)$.

== Scheme summary
#table(
  columns: (1fr, auto, auto, auto, auto),
  inset: 3pt,
  align: (left, center, center, center, left),
  stroke: 0.4pt,
  table.header([*Scheme*], [*MS*], [*Imp*], [*LTE*], [*Stability*]),
  [Forward Euler], [✗], [✗], [$O(h^2)$], [$h < 2/lambda$],
  [Trapezoidal Rule], [✗], [✓], [$O(h^3)$], [unconditional],
  [Improved Euler], [✗], [✗], [$O(h^3)$], [$h < 2/lambda$],
  [Backwards Euler], [✗], [✓], [$O(h^2)$], [unconditional],
  [Midpoint Method], [✗], [✗], [$O(h^3)$], [$h < 2/lambda$],
  [BDF2], [✓], [✓], [$O(h^3)$], [unconditional],
)
#text(size: 6.5pt)[MS = multi-step, Imp = implicit.]

== Global error & stability
- $"GE" approx sum_j "LTE"_j approx "LTE" times O(1/h) = O(h^p)$; the order of the GE is one less than that of the LTE.
- *Test equation*: $y' = -lambda y$, $"Re"(lambda) > 0$ (eigenvalue $-lambda$, so the exact solution decays); a stable scheme requires $lim_(n -> infinity) epsilon_n = 0$, where $epsilon_n = y^((p))_n - y_n$.
- *Forward Euler*: $y_(n+1) = y_0 (1 - h lambda)^n$, so $epsilon_n = epsilon_0 (1 - h lambda)^n -> 0$ iff $|1 - h lambda| < 1$, i.e. $h < 2/lambda$.
- Consistency: $"LTE" -> 0$ as $h -> 0$. Zero-stability: solution bounded as $h -> 0$. Convergence: numerical $arrow.r$ true solution as $h -> 0$.
- Absolute stability: bounded for given $h$ as $n -> infinity$; *A-stability*: absolutely stable for all $"Re"(lambda) > 0$; *stability region*: set of $h lambda$ that are absolutely stable.
- *Stiff equations*: transients decay much faster than the solution, so $h$ is limited by stability, not accuracy; implicit methods are preferred.

== Adaptive time-stepping
- Smaller $h$ reduces LTE but needs more steps; pick $h$ so error $<=$ tolerance with minimal effort.
- Algorithm: (1) compute two solutions $y^A, y^B$ with schemes of different order; (2) estimate error $= |y^A_(n+1) - y^B_(n+1)|$; (3) while error $> "tol"$, set $h <- h/2$ and recompute; (4) predict the next step
  $ h_"new" = h_"old" ( ("tol") / (|y^A_(n+1) - y^B_(n+1)| ))^(1/p) $
  where $p$ is the lower order of the two schemes; repeat until the end time.

== Recipes
- *Test stability of a scheme*: (1) apply it to $y' = -lambda y$; (2) find the closed form of $epsilon_n = y^((p))_n - y_n$; (3) find the condition on $h$ ensuring $epsilon_n -> 0$.
- *Find the LTE of an unknown method*: (1) replace RHS approximations with exact values ($y_(n-1) -> y(t_(n-1))$, $f(t_n, y_n) -> y'(t_n)$); (2) Taylor-expand all RHS quantities about $t_n$; (3) Taylor-expand the exact solution $y(t_(n+1))$; (4) $"LTE" = y(t_(n+1)) - y_(n+1)$, keeping the lowest non-cancelling power of $h$.
