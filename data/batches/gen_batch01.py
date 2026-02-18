#!/usr/bin/env python3
"""Generate chain-of-thought solutions for JEE Advanced batch_01 questions."""
import json

input_path = "/Users/apple/jee-finetune/data/batches/batch_01.jsonl"
output_path = "/Users/apple/jee-finetune/data/batches/batch_01_solutions.jsonl"

# Read all questions
questions = []
with open(input_path, 'r') as f:
    for line in f:
        line = line.strip()
        if line:
            questions.append(json.loads(line))

print(f"Read {len(questions)} questions")

# Solutions indexed by line number (0-based)
solutions = {}

# Q0: Chem - Raoult's law positive deviation, gold=AB
solutions[0] = (
r"""**Key Concepts:** Positive deviation from Raoult's law occurs when A-B interactions are weaker than A-A and B-B interactions.

**Analysis of each mixture:**

(A) **Carbon tetrachloride + methanol:** $\text{CCl}_4$ is nonpolar while methanol is strongly polar with hydrogen bonding. The A-B interactions are much weaker than the strong H-bonds in pure methanol. This leads to **positive deviation**. $\checkmark$

(B) **Carbon disulphide + acetone:** $\text{CS}_2$ is nonpolar while acetone is polar (dipole-dipole interactions). The unlike interactions are weaker than the like interactions. This leads to **positive deviation**. $\checkmark$

(C) **Benzene + toluene:** Both are nonpolar aromatic hydrocarbons with very similar structures and intermolecular forces. This mixture is nearly ideal — **no significant deviation**. $\times$

(D) **Phenol + aniline:** Phenol and aniline can form strong intermolecular hydrogen bonds (O-H$\cdots$N). The A-B interactions are stronger than A-A and B-B, leading to **negative deviation**. $\times$

**Answer:** AB"""
)

# Q1: Chem - CCP structure, gold=BCD
solutions[1] = (
r"""**Key Concepts:** Cubic close packed (ccp) = face-centred cubic (FCC). Properties: coordination number 12 (bulk), packing efficiency 74%, octahedral voids per atom = 1, tetrahedral voids per atom = 2, $a = 2\sqrt{2}r$.

**(A)** An atom in the **topmost layer** (surface) does NOT have 12 nearest neighbours — only bulk atoms do. Surface atoms have fewer (typically 9). **Incorrect.** $\times$

**(B)** Packing efficiency:
$$\eta = \frac{4 \times \frac{4}{3}\pi r^3}{(2\sqrt{2}\,r)^3} = \frac{\pi}{3\sqrt{2}} \approx 0.7405 = 74\%$$
**Correct.** $\checkmark$

**(C)** In FCC: 4 atoms, 4 octahedral voids, 8 tetrahedral voids per unit cell. Per atom: 1 octahedral void and 2 tetrahedral voids. **Correct.** $\checkmark$

**(D)** Face diagonal $= 4r = a\sqrt{2}$, so $a = 2\sqrt{2}\,r$. **Correct.** $\checkmark$

**Answer:** BCD"""
)

# Q2: Chem - Extraction of copper, gold=ABC
solutions[2] = (
r"""**Key Concepts:** Metallurgy of copper from copper pyrite ($\text{CuFeS}_2$).

**(A)** The ore is crushed and concentrated by **froth flotation** (sulphide ores float due to preferential wetting by oil). **Correct.** $\checkmark$

**(B)** During smelting, iron is removed as slag: $\text{FeO} + \text{SiO}_2 \to \text{FeSiO}_3$. **Correct.** $\checkmark$

**(C)** Self-reduction (Bessemerisation):
$$2\text{Cu}_2\text{S} + 3\text{O}_2 \to 2\text{Cu}_2\text{O} + 2\text{SO}_2$$
$$\text{Cu}_2\text{S} + 2\text{Cu}_2\text{O} \to 6\text{Cu} + \text{SO}_2$$
Blister copper is formed with $\text{SO}_2$ evolution. **Correct.** $\checkmark$

**(D)** Blister copper is refined by **electrolytic refining**, NOT carbon reduction. **Incorrect.** $\times$

**Answer:** ABC"""
)

# Q3: Chem - HNO3 + P4O10, gold=BD
solutions[3] = (
r"""**Key Concepts:** $\text{P}_4\text{O}_{10}$ is a powerful dehydrating agent. It dehydrates $\text{HNO}_3$ to $\text{N}_2\text{O}_5$:
$$4\text{HNO}_3 + \text{P}_4\text{O}_{10} \to 2\text{N}_2\text{O}_5 + 4\text{HPO}_3$$

**Analysis of $\text{N}_2\text{O}_5$ (the nitrogen-containing product):**

**(A)** $\text{P}_4 + \text{HNO}_3$ gives $\text{H}_3\text{PO}_4$ and $\text{NO}_2$, not $\text{N}_2\text{O}_5$. **Incorrect.** $\times$

**(B)** $\text{N}_2\text{O}_5$ has structure $\text{O}_2\text{N}-\text{O}-\text{NO}_2$ with all electrons paired. It is **diamagnetic**. **Correct.** $\checkmark$

**(C)** The two nitrogen atoms are connected through an oxygen bridge ($\text{N}-\text{O}-\text{N}$), not directly bonded. There is **no N-N bond**. **Incorrect.** $\times$

**(D)** $\text{N}_2\text{O}_5$ reacts with Na metal, and the vigorous reaction produces $\text{NO}_2$ (brown gas):
$$\text{N}_2\text{O}_5 \to 2\text{NO}_2 + \frac{1}{2}\text{O}_2$$
**Correct.** $\checkmark$

**Answer:** BD"""
)

# Q4: Chem - Invert sugar, gold=BC
solutions[4] = (
r"""**Key Concepts:** Invert sugar is produced by acid hydrolysis of sucrose into D-(+)-glucose and D-(-)-fructose.

**(A)** Invert sugar comes from **sucrose** hydrolysis, not maltose. Maltose gives two glucose molecules. **Incorrect.** $\times$

**(B)** Invert sugar is an equimolar mixture of D-(+)-glucose and D-(-)-fructose. The D-enantiomers have opposite rotations to the given L-forms: D-glucose = $+52°$, D-fructose = $-92°$. **Correct.** $\checkmark$

**(C)** Specific rotation of invert sugar:
$$[\alpha] = \frac{(+52°) + (-92°)}{2} = \frac{-40°}{2} = -20°$$
**Correct.** $\checkmark$

**(D)** $\text{Br}_2$ water oxidizes glucose to gluconic acid (not saccharic acid). Saccharic acid requires stronger oxidation (e.g., $\text{HNO}_3$) of both terminal groups. **Incorrect.** $\times$

**Answer:** BC"""
)

# Q5: Math - Matrix P^50, gold=B
solutions[5] = (
r"""**Key Concepts:** Nilpotent matrix decomposition and binomial theorem.

Write $P = I + N$ where $N = \begin{bmatrix} 0 & 0 & 0 \\ 4 & 0 & 0 \\ 16 & 4 & 0 \end{bmatrix}$.

Compute $N^2$:
$$N^2 = \begin{bmatrix} 0 & 0 & 0 \\ 0 & 0 & 0 \\ 16 & 0 & 0 \end{bmatrix}$$

$N^3 = \mathbf{0}$ (nilpotent of order 3).

$$P^{50} = (I+N)^{50} = I + 50N + \binom{50}{2}N^2 = I + 50N + 1225N^2$$

$$P^{50} = \begin{bmatrix} 1 & 0 & 0 \\ 200 & 1 & 0 \\ 50(16) + 1225(16) & 50(4) & 1 \end{bmatrix} = \begin{bmatrix} 1 & 0 & 0 \\ 200 & 1 & 0 \\ 20400 & 200 & 1 \end{bmatrix}$$

$Q = P^{50} - I$: $q_{31} = 20400$, $q_{32} = 200$, $q_{21} = 200$.

$$\frac{q_{31} + q_{32}}{q_{21}} = \frac{20400 + 200}{200} = \frac{20600}{200} = 103$$

**Answer:** B"""
)

# Q6: Math - AP vs GP, gold=B
solutions[6] = (
r"""**Key Concepts:** Comparison between AP and GP using convexity (AM-GM inequality).

Since $\log_e b_k$ is in AP with common difference $\log_e 2$, $b_k = b_1 \cdot 2^{k-1}$ forms a GP with ratio 2.

The $a_k$ are in AP with $a_1 = b_1$ and $a_{51} = b_{51} = b_1 \cdot 2^{50}$.

**Comparing $s = \sum_{k=1}^{51} a_k$ and $t = \sum_{k=1}^{51} b_k$:**

Both sequences share endpoints $a_1 = b_1$ and $a_{51} = b_{51}$. The AP interpolates linearly while the GP grows exponentially (convex). By the property that a linear function lies above a convex function between shared endpoints (for intermediate points), $a_k \geq b_k$ for $1 \leq k \leq 51$.

Therefore $s > t$.

**Comparing $a_{101}$ and $b_{101}$:**

$a_{101} = b_1 + 100d$ where $d = \frac{b_1(2^{50}-1)}{50}$, so $a_{101} = b_1(2^{51} - 1)$.

$b_{101} = b_1 \cdot 2^{100}$.

Since $2^{100} \gg 2^{51} - 1$, we have $a_{101} < b_{101}$.

**Answer:** B"""
)

# Q7: Math - Integral, gold=A
solutions[7] = (
r"""**Key Concepts:** Symmetric integral property and integration by parts.

Let $I = \int_{-\pi/2}^{\pi/2} \frac{x^2 \cos x}{1+e^x}\,dx$.

Substituting $x \to -x$:
$$I = \int_{-\pi/2}^{\pi/2} \frac{x^2 \cos x \cdot e^x}{1+e^x}\,dx$$

Adding:
$$2I = \int_{-\pi/2}^{\pi/2} x^2 \cos x\,dx = 2\int_0^{\pi/2} x^2 \cos x\,dx$$

So $I = \int_0^{\pi/2} x^2 \cos x\,dx$.

Integration by parts:
$$\int x^2 \cos x\,dx = x^2 \sin x - 2\int x \sin x\,dx = x^2 \sin x + 2x\cos x - 2\sin x + C$$

Evaluating:
$$I = \left[\frac{\pi^2}{4}(1) + 0 - 2\right] - [0] = \frac{\pi^2}{4} - 2$$

**Answer:** A"""
)

# Q8: Math - Image of point, plane equation, gold=C
solutions[8] = (
r"""**Key Concepts:** Reflection of a point in a plane, equation of plane through a point and a line.

**Step 1:** Image of $(3,1,7)$ in plane $x - y + z = 3$.

Normal direction: $(1,-1,1)$. Parametric line: $(3+t, 1-t, 7+t)$.

Foot of perpendicular satisfies: $(3+t)-(1-t)+(7+t) = 3 \Rightarrow 9+3t = 3 \Rightarrow t = -2$.

Image $P = (3+2(-2), 1-2(-2), 7+2(-2)) = (-1, 5, 3)$.

**Step 2:** Plane through $P(-1,5,3)$ containing line $\frac{x}{1}=\frac{y}{2}=\frac{z}{1}$.

Line passes through $O(0,0,0)$ with direction $\vec{d}=(1,2,1)$.

$\vec{OP} = (-1,5,3)$. Normal: $\vec{n} = \vec{d} \times \vec{OP}$:
$$\vec{n} = \begin{vmatrix} \hat{i}&\hat{j}&\hat{k}\\1&2&1\\-1&5&3 \end{vmatrix} = (6-5)\hat{i}-(3+1)\hat{j}+(5+2)\hat{k} = (1,-4,7)$$

Plane: $x - 4y + 7z = 0$.

Verify: $P(-1,5,3)$: $-1-20+21 = 0$ $\checkmark$

**Answer:** C"""
)

# Q9: Math - Differentiability, gold=AB
solutions[9] = (
r"""**Key Concepts:** Differentiability analysis at points where absolute values create potential corners.

$f(x) = a\cos(|x^3-x|) + b|x|\sin(|x^3+x|)$

**Checking (A): $a=0, b=1$ at $x=0$.**

$f(x) = |x|\sin(|x^3+x|)$. Near $x=0$: $|x^3+x| = |x|(x^2+1)$.

For $x > 0$: $f(x) = x\sin(x(x^2+1))$. For $x < 0$: $f(x) = (-x)\sin((-x)(x^2+1)) = (-x)(-\sin(x(x^2+1))) = x\sin(x(x^2+1))$.

So $f(x) = x\sin(x(1+x^2))$ everywhere near 0 — smooth. **Differentiable at $x=0$.** $\checkmark$

**Checking (B): $a=1, b=0$ at $x=1$.**

$f(x) = \cos(|x^3-x|)$. At $x=1$: $|x^3-x|=0$, so $f(1)=1$.

$f'(x) = -\sin(|x^3-x|) \cdot \frac{d}{dx}|x^3-x|$. Since $\sin(0)=0$ at $x=1$, regardless of the derivative of $|x^3-x|$, we get $f'(1) = 0$. **Differentiable at $x=1$.** $\checkmark$

**Checking (C): $a=1, b=0$ at $x=0$.**

$f(x) = \cos(|x^3-x|) = \cos(|x||x^2-1|)$. Near 0: $= \cos(|x|(1-x^2))$. This is even in $x$ and smooth (cosine of a function that vanishes at 0). $f'(0) = 0$ exists. So $f$ IS differentiable. **(C) says NOT differentiable — Incorrect.** $\times$

**Checking (D): $a=1, b=1$ at $x=1$.**

Both $\cos(|x^3-x|)$ and $|x|\sin(|x^3+x|)$ are differentiable at $x=1$ (by similar analysis). **Differentiable, so (D) is incorrect.** $\times$

**Answer:** AB"""
)

# Q10: Math - Local minimum and function properties, gold=AD
solutions[10] = (
r"""**Key Concepts:** L'Hopital's rule, second derivative test.

Given: $f: \mathbb{R} \to (0,\infty)$, $f'(2) = g(2) = 0$, $f''(2) \neq 0$, $g'(2) \neq 0$.

$$\lim_{x \to 2} \frac{f(x)g(x)}{f'(x)g'(x)} = 1$$

Both numerator $\to f(2)\cdot 0 = 0$ and denominator $\to 0 \cdot g'(2) = 0$. Apply L'Hopital:

$$\lim_{x \to 2} \frac{f'(x)g(x) + f(x)g'(x)}{f''(x)g'(x) + f'(x)g''(x)} = \frac{0 + f(2)g'(2)}{f''(2)g'(2) + 0} = \frac{f(2)}{f''(2)} = 1$$

So $f''(2) = f(2) > 0$.

**(A)** $f'(2) = 0$ and $f''(2) > 0$: **local minimum** at $x = 2$. $\checkmark$

**(B)** Local maximum requires $f''(2) < 0$. **Incorrect.** $\times$

**(C)** $f''(2) > f(2)$: But $f''(2) = f(2)$. **Incorrect.** $\times$

**(D)** $f(x) - f''(x) = 0$ for at least one $x$: At $x = 2$, $f(2) - f''(2) = 0$. **Correct.** $\checkmark$

**Answer:** AD"""
)

# Q11: Math - Floor function discontinuity, gold=BC
solutions[11] = (
r"""**Key Concepts:** Discontinuities of $[y]$ (greatest integer function) and differentiability.

$f(x) = [x^2 - 3]$ on $[-1/2, 2]$; $g(x) = (|x| + |4x-7|)f(x)$.

**Discontinuities of $f$:** $[y]$ jumps at integers. $x^2 - 3$ passes through integers at:
- $x^2 = 1 \Rightarrow x = 1$: $x^2-3$ crosses $-2$ (from below)
- $x^2 = 2 \Rightarrow x = \sqrt{2}$: crosses $-1$
- $x^2 = 3 \Rightarrow x = \sqrt{3}$: crosses $0$
- $x^2 = 4 \Rightarrow x = 2$: crosses $1$

At $x = 0$: $x^2 - 3 = -3$ and nearby $x^2-3 > -3$, so $[x^2-3]$ jumps from $-3$ to... no, for $x$ near 0, $x^2-3$ is slightly above $-3$, so $[x^2-3] = -3$ everywhere near 0. **Not discontinuous** at $x=0$.

Discontinuities at $x = 1, \sqrt{2}, \sqrt{3}, 2$: **four points**. **(B) Correct.** $\checkmark$

**Non-differentiability of $g$:** On $(-1/2, 2)$: $|x| = x$ (since $x > 0$ in interior away from endpoints). $|4x-7|$ changes at $x = 7/4$.

$g$ is non-differentiable where $f$ is discontinuous (if the multiplier is nonzero) and where $|4x-7|$ has a corner (if $f \neq 0$).

At $x = 1, \sqrt{2}$: $f$ discontinuous, multiplier nonzero. Non-differentiable. At $x = \sqrt{3}$: $f$ jumps from $-1$ to $0$, non-differentiable. At $x = 7/4$: $f(7/4) = [(7/4)^2-3] = [49/16-48/16] = [1/16] = 0$. Since $f = 0$, $g = 0$ near $7/4$... but $f$ changes sign/value around $7/4$? Actually $f(x) = 0$ for $x \in [\sqrt{3}, 2)$, and $7/4 = 1.75 > \sqrt{3} \approx 1.732$. So $f = 0$ near $7/4$, making $g = 0$ near $7/4$, hence $g$ is differentiable there.

But we need to also check $x = 0$: $f(0) = [-3] = -3$. Near $0$, $|x|$ has a corner. $g(x) = (|x| + |4x-7|) \cdot (-3) = -3(|x| + 7-4x)$ near 0. The $|x|$ term makes it non-differentiable at $x = 0$, but $x = 0$ is barely inside $(-1/2, 2)$. $g'(0^+) = -3(1-4) = 9$ and $g'(0^-) = -3(-1-4) = 15$. Different, so non-differentiable at $x = 0$.

Non-differentiable points: $x = 0, 1, \sqrt{2}, \sqrt{3}$: **four points**. **(C) Correct.** $\checkmark$

**Answer:** BC"""
)

# Q12: Math - Complex locus, gold=ACD
solutions[12] = (
r"""**Key Concepts:** Locus of complex number parametrized by real variable.

$z = \frac{1}{a + ibt}$, $t \in \mathbb{R}$, $t \neq 0$.

$$z = \frac{a - ibt}{a^2 + b^2t^2}, \quad x = \frac{a}{a^2+b^2t^2}, \quad y = \frac{-bt}{a^2+b^2t^2}$$

$x^2 + y^2 = \frac{1}{a^2+b^2t^2}$, so $x = a(x^2+y^2)$.

This gives $(x-\frac{1}{2a})^2 + y^2 = \frac{1}{4a^2}$ for $a \neq 0, b \neq 0$.

**(A)** $a > 0, b \neq 0$: Circle with center $(\frac{1}{2a}, 0)$ and radius $\frac{1}{2a}$. **Correct.** $\checkmark$

**(B)** $a < 0, b \neq 0$: Center is $(\frac{1}{2a}, 0)$, which is negative. Radius is $|\frac{1}{2a}| = -\frac{1}{2a}$. Option states center $(-\frac{1}{2a}, 0)$ which would be positive — this is wrong since the actual center has negative $x$-coordinate. **Incorrect.** $\times$

**(C)** $a \neq 0, b = 0$: $z = 1/a$, a single point on the $x$-axis. Lies on $x$-axis. **Correct.** $\checkmark$

**(D)** $a = 0, b \neq 0$: $z = \frac{1}{ibt} = \frac{-i}{bt}$. So $x = 0$: lies on $y$-axis. **Correct.** $\checkmark$

**Answer:** ACD"""
)

# Q13: Math - Parabola closest point, gold=ACD
solutions[13] = (
r"""**Key Concepts:** Closest point on parabola to a given point, properties of normals and tangents.

Circle: $(x-2)^2 + (y-8)^2 = 4$, center $S = (2,8)$, radius $r = 2$.

Parabola: $y^2 = 4x$. Parametric point: $(t^2, 2t)$.

**Distance squared from $S$:** $D(t) = (t^2-2)^2 + (2t-8)^2$.

$D'(t) = 4t^3 - 32 = 0 \Rightarrow t = 2$. So $P = (4, 4)$.

**(A)** $SP = \sqrt{(4-2)^2+(4-8)^2} = \sqrt{4+16} = 2\sqrt{5}$. **Correct.** $\checkmark$

**(B)** $Q$ on circle along $SP$: $SQ = r = 2$, $QP = 2\sqrt{5}-2$.
$SQ:QP = 2:(2\sqrt{5}-2) = 1:(\sqrt{5}-1)$. Rationalizing: $= (\sqrt{5}+1):4 \neq (\sqrt{5}+1):2$. **Incorrect.** $\times$

**(C)** Normal to parabola at $(t^2,2t)$: $y + tx = 2t + t^3$. At $t=2$: $y + 2x = 12$. Setting $y=0$: $x = 6$. **Correct.** $\checkmark$

**(D)** Slope of $SP = \frac{4-8}{4-2} = -2$. The tangent to the circle at $Q$ is perpendicular to radius $SQ$, which lies along $SP$. Slope of tangent $= 1/2$. **Correct.** $\checkmark$

**Answer:** ACD"""
)

# Q14: Math - System of linear equations, gold=BCD
solutions[14] = (
r"""**Key Concepts:** Determinant analysis for 2-equation system.

$$ax + 2y = \lambda, \quad 3x - 2y = \mu$$

Determinant: $\Delta = -2a - 6$.

**(A)** $a = -3$: $\Delta = 0$. Equations become $-3x+2y = \lambda$ and $3x-2y = \mu$. Adding: $0 = \lambda+\mu$. Need $\lambda+\mu = 0$ for any solution. Not true for all $\lambda,\mu$. **Incorrect.** $\times$

**(B)** $a \neq -3$: $\Delta \neq 0$, unique solution by Cramer's rule for all $\lambda,\mu$. **Correct.** $\checkmark$

**(C)** $\lambda+\mu = 0$, $a = -3$: Second equation is $-1$ times the first. Infinitely many solutions. **Correct.** $\checkmark$

**(D)** $\lambda+\mu \neq 0$, $a = -3$: Adding gives $0 = \lambda+\mu \neq 0$. Contradiction. No solution. **Correct.** $\checkmark$

**Answer:** BCD"""
)

# Q15: Math - Unit vectors cross product, gold=BC
solutions[15] = (
r"""**Key Concepts:** Cross product constraints, perpendicularity.

$|\hat{u}\times\vec{v}| = 1$ and $\hat{w}\cdot(\hat{u}\times\vec{v}) = 1$ with $|\hat{w}| = 1$.

Since $|\hat{w}||\hat{u}\times\vec{v}|\cos\theta = 1$ and both magnitudes are 1, $\cos\theta = 1$, so $\hat{u}\times\vec{v} = \hat{w}$.

This requires $\hat{u} \perp \hat{w}$, i.e., $\hat{u}\cdot\hat{w} = 0$.

**(A)** $\vec{v}$ can be modified by $\vec{v} + c\hat{u}$ without changing $\hat{u}\times\vec{v}$. Not unique. **Incorrect.** $\times$

**(B)** Infinitely many $\vec{v}$ (as argued). **Correct.** $\checkmark$

**(C)** $\hat{u}$ in $xy$-plane: $u_3 = 0$. $\hat{u}\cdot\hat{w} = \frac{1}{\sqrt{6}}(u_1+u_2) = 0 \Rightarrow u_1 = -u_2 \Rightarrow |u_1| = |u_2|$. **Correct.** $\checkmark$

**(D)** $\hat{u}$ in $xz$-plane: $u_2 = 0$. $\hat{u}\cdot\hat{w} = \frac{1}{\sqrt{6}}(u_1+2u_3) = 0 \Rightarrow u_1 = -2u_3 \Rightarrow |u_1| = 2|u_3|$. Statement says $2|u_1| = |u_3|$. **Incorrect.** $\times$

**Answer:** BC"""
)

# Q16: Phy - Flat plate moving in gas, gold=ABD
solutions[16] = (
r"""**Key Concepts:** Kinetic theory — molecular collisions with moving plate at low pressure ($v \ll u$).

**Leading face:** Molecules approach with relative speed $\sim u+v$. Rate of collisions $\propto (u+v)$, momentum per collision $\propto (u+v)$. Pressure $\propto (u+v)^2$.

**Trailing face:** Pressure $\propto (u-v)^2$.

**Pressure difference:** $\Delta P \propto (u+v)^2 - (u-v)^2 = 4uv \propto uv$. **(A) Correct.** $\checkmark$

**Resistive force:** $F_{\text{res}} \propto uv \propto v$. **(B) Correct.** $\checkmark$

**(C)** Since $F_{\text{res}} \propto v$ increases with speed, the net force decreases. Acceleration is NOT constant. **Incorrect.** $\times$

**(D)** Terminal velocity is reached when $F = F_{\text{res}}$. **Correct.** $\checkmark$

**Answer:** ABD"""
)

# Q17: Phy - Stefan-Boltzmann, gold=C
solutions[17] = (
r"""**Key Concepts:** Stefan-Boltzmann law, Wien's displacement law.

$T = 310$ K, $T_0 = 300$ K, $A = 1$ m$^2$, $\sigma T_0^4 = 460$ W/m$^2$.

**(A)** Total energy **radiated** by body in 1 s: $\sigma T^4 A \approx \sigma T_0^4 (310/300)^4 \approx 460 \times 1.14 \approx 524$ J. Not close to 60 J. (The **net** radiation $\approx 60$ J, but "energy radiated" means total emission.) **Incorrect.** $\times$

**(B)** When $T_0$ decreases by $\Delta T_0$, the body still radiates the same (it's at the same $T$), but absorbs less. The body needs to **produce** more heat internally, not radiate more. The statement's formula describes the change in absorbed power, not radiated power. **Incorrect.** $\times$

**(C)** Reducing surface area $A$ reduces net radiative heat loss $\propto A$, allowing the body to maintain temperature with less metabolic energy. **Correct.** $\checkmark$

**(D)** By Wien's law, $\lambda_{\max} \propto 1/T$. Higher $T$ shifts peak to **shorter** wavelengths. **Incorrect.** $\times$

**Answer:** C"""
)

# Q18: Phy - Prism optics, gold=ACD
solutions[18] = (
r"""**Key Concepts:** Minimum deviation in prism: $\delta_m = 2i_1 - A$, $r_1 = r_2 = A/2$.

Given $\delta_m = A$: $A = 2i_1 - A \Rightarrow i_1 = A$.

Snell's law: $\sin A = \mu\sin(A/2) \Rightarrow 2\cos(A/2) = \mu$.

**(A)** At $i_1 = A$: $r_1 = A/2$. Since $r_1 = r_2 = A/2$, the ray is symmetric and parallel to the base. **Correct.** $\checkmark$

**(B)** From $\mu = 2\cos(A/2)$: $A = 2\cos^{-1}(\mu/2)$, not $\frac{1}{2}\cos^{-1}(\mu/2)$. **Incorrect.** $\times$

**(C)** $r_1 = A/2 = i_1/2$ (since $i_1 = A$). **Correct.** $\checkmark$

**(D)** For emergent ray tangential: $r_2 = C$ (critical angle, $\sin C = 1/\mu$). Then $r_1 = A - C$.
$\sin i_1 = \mu\sin(A-C) = \mu[\sin A\cos C - \cos A\sin C]$
$= \sin A\cdot\mu\cos C - \cos A\cdot 1 = \sin A\sqrt{4\cos^2(A/2)-1} - \cos A$
So $i_1 = \sin^{-1}[\sin A\sqrt{4\cos^2(A/2)-1} - \cos A]$. **Correct.** $\checkmark$

**Answer:** ACD"""
)

# Q19: Phy - Surface tension drop, gold=6
solutions[19] = (
r"""**Key Concepts:** Surface energy change when a drop splits into $K$ identical drops.

Volume conservation: $\frac{4}{3}\pi R^3 = K\cdot\frac{4}{3}\pi r^3 \Rightarrow r = R/K^{1/3}$.

$$\Delta U = S[K\cdot 4\pi r^2 - 4\pi R^2] = 4\pi S R^2[K^{1/3} - 1]$$

Substituting $R = 10^{-2}$ m, $S = \frac{0.1}{4\pi}$ N/m, $\Delta U = 10^{-3}$ J:

$$10^{-3} = 4\pi\cdot\frac{0.1}{4\pi}\cdot(10^{-2})^2\cdot[K^{1/3}-1] = 0.1\times10^{-4}\cdot[K^{1/3}-1]$$

$$K^{1/3} - 1 = \frac{10^{-3}}{10^{-5}} = 100 \Rightarrow K^{1/3} \approx 100 \Rightarrow K = 10^6$$

$\alpha = 6$.

**Answer:** 6"""
)

# Q20: Phy - Hydrogen atom transition, gold=5
solutions[20] = (
r"""**Key Concepts:** Potential energy in hydrogen atom: $V_n \propto -1/n^2$.

$$\frac{V_i}{V_f} = \frac{n_f^2}{n_i^2} = 6.25 = \frac{25}{4}$$

$$\frac{n_f}{n_i} = \frac{5}{2}$$

Smallest integers: $n_i = 2$, $n_f = 5$.

**Answer:** 5"""
)

# Q21: Phy - Beat frequency, gold=6
solutions[21] = (
r"""**Key Concepts:** Doppler effect for sound reflection.

$f_0 = 492$ Hz, car speed $v_c = 2$ m/s, $v = 330$ m/s.

Frequency received by car: $f_1 = f_0\frac{v+v_c}{v} = 492\cdot\frac{332}{330}$

Frequency reflected back to source: $f_2 = f_1\cdot\frac{v}{v-v_c} = 492\cdot\frac{332}{330}\cdot\frac{330}{328} = 492\cdot\frac{332}{328}$

Beat frequency:
$$\Delta f = f_2 - f_0 = 492\left(\frac{332}{328}-1\right) = 492\cdot\frac{4}{328} = \frac{1968}{328} = 6$$

**Answer:** 6"""
)

# Q22: Phy - Blood volume, gold=5
solutions[22] = (
r"""**Key Concepts:** Radioactive tracer dilution method.

$t_{1/2} = 8$ days, $A_0 = 2.4\times10^5$ Bq, after $t = 11.5$ hr: 2.5 ml gives 115 Bq.

Decay constant: $\lambda = \frac{0.7}{8\times24} = \frac{0.7}{192}$ hr$^{-1}$.

$\lambda t = \frac{0.7\times11.5}{192} \approx 0.042 \ll 1$

$A(t) = A_0(1 - \lambda t) = 2.4\times10^5\times0.958 \approx 2.3\times10^5$ Bq

Activity per ml: $\frac{115}{2.5} = 46$ Bq/ml.

Total volume: $V = \frac{2.3\times10^5}{46} = 5000$ ml $= 5$ L.

**Answer:** 5"""
)

# Q23: Chem - Ideal gas expansion, gold=ABC
solutions[23] = (
r"""**Key Concepts:** Thermodynamics of ideal gas processes.

**(A)** Irreversible compression against constant $p_1$ (the higher pressure): $W_{\text{on}} = p_1(V_2-V_1)$. This is maximum work on gas (more than reversible compression). **Correct.** $\checkmark$

**(B)** Free expansion: $W = 0$, $q = 0$ (adiabatic). For ideal gas, $\Delta U = 0 \Rightarrow \Delta T = 0$ (isothermal). Both simultaneously. **Correct.** $\checkmark$

**(C)** In adiabatic expansion, temperature drops, so the $P$-$V$ curve falls below the isothermal curve. Less work done in adiabatic than isothermal expansion. **Correct.** $\checkmark$

**(D)** (i) $T_1 = T_2$: $\Delta U = 0$ — correct. (ii) Adiabatic expansion: $T$ decreases, $\Delta U = nC_v(T_2-T_1) < 0$ — negative, not positive. **Incorrect.** $\times$

**Answer:** ABC"""
)

# Q24: Chem - Oxoacids, gold=ABD
solutions[24] = (
r"""**Key Concepts:** Hybridization, acidity, and basicity of oxoacids.

**(A)** Both Cl atoms in $\text{HClO}_4$ and $\text{HClO}$ are $sp^3$ hybridized (4 electron domains around Cl in each). **Correct.** $\checkmark$

**(B)** $\text{HClO}_4$ is stronger because $\text{ClO}_4^-$ has 4 equivalent resonance structures stabilizing the negative charge, while $\text{ClO}^-$ has minimal resonance stabilization. **Correct.** $\checkmark$

**(C)** $\text{Cl}_2 + \text{H}_2\text{O} \to \text{HCl} + \text{HClO}$ (not $\text{HClO}_4$). **Incorrect.** $\times$

**(D)** Since $\text{HClO}_4$ is an extremely strong acid, $\text{ClO}_4^-$ is an extremely weak base — weaker than $\text{H}_2\text{O}$. **Correct.** $\checkmark$

**Answer:** ABD"""
)

# Q25: Chem - Halogen color, gold=CD
solutions[25] = (
r"""**Key Concepts:** Electronic transitions in halogen molecules determine their color.

Going down group 17: $\text{F}_2$ (pale yellow) $\to$ $\text{Cl}_2$ (yellow-green) $\to$ $\text{Br}_2$ (brown) $\to$ $\text{I}_2$ (violet).

**(A)** Physical state doesn't determine molecular color. **Incorrect.** $\times$

**(B)** Ionization energy of atoms isn't directly responsible for molecular color. **Incorrect.** $\times$

**(C)** The color arises from $\pi^* \to \sigma^*$ transitions. The energy gap decreases down the group, shifting absorption to longer wavelengths. **Correct.** $\checkmark$

**(D)** HOMO-LUMO gap decreases down the group (equivalent to (C) stated generally). **Correct.** $\checkmark$

**Answer:** CD"""
)

# Q26: Chem - Cobalt coordination compounds, gold=BCD
solutions[26] = (
r"""**Key Concepts:** Cobalt(II) coordination chemistry — $d^7$, $\mu = 3.87$ BM (3 unpaired electrons).

X = $[\text{Co}(\text{H}_2\text{O})_6]\text{Cl}_2$ (pink, octahedral Co$^{2+}$).
Y = $[\text{Co}(\text{NH}_3)_6]\text{Cl}_3$ (Co$^{3+}$, oxidized by air, diamagnetic low-spin $d^6$, 1:3 electrolyte).
Z = $[\text{CoCl}_4]^{2-}$ (blue, tetrahedral Co$^{2+}$, 3 unpaired electrons).

**(A)** Y = $[\text{Co}(\text{NH}_3)_6]\text{Cl}_3$ gives **3** equivalents of AgCl, not 2. **Incorrect.** $\times$

**(B)** Co$^{3+}$ in Y: low-spin $d^6$, inner orbital, $d^2sp^3$ hybridization. **Correct.** $\checkmark$

**(C)** Z = $[\text{CoCl}_4]^{2-}$ is tetrahedral. **Correct.** $\checkmark$

**(D)** The equilibrium favors the octahedral (pink) form at low temperature ($0°$C) since the tetrahedral $\to$ octahedral conversion is exothermic. Solution is pink. **Correct.** $\checkmark$

**Answer:** BCD"""
)

# Q27: Chem - FCC crystal N value, gold=2
solutions[27] = (
r"""**Key Concepts:** FCC unit cell calculation.

FCC: $Z = 4$, $a = 400$ pm $= 4\times10^{-8}$ cm, $\rho = 8$ g/cm$^3$.

Volume of 256 g: $V = \frac{256}{8} = 32$ cm$^3$.

Number of unit cells: $\frac{V}{a^3} = \frac{32}{(4\times10^{-8})^3} = \frac{32}{64\times10^{-24}} = 5\times10^{23}$

Number of atoms: $4 \times 5\times10^{23} = 2\times10^{24}$

$N = 2$.

**Answer:** 2"""
)

# Q28: Chem - Conductivity, gold=6
solutions[28] = (
r"""**Key Concepts:** Molar conductivity and degree of dissociation.

$c = 0.0015$ M, $G = 5\times10^{-7}$ S, cell constant $= \ell/A = 120$ cm$^{-1}$, pH $= 4$.

$$\kappa = G \times \frac{\ell}{A} = 5\times10^{-7} \times 120 = 6\times10^{-5} \text{ S cm}^{-1}$$

$$\Lambda_m = \frac{\kappa}{c(\text{in mol/cm}^3)} = \frac{6\times10^{-5}}{1.5\times10^{-6}} = 40 \text{ S cm}^2\text{mol}^{-1}$$

Degree of dissociation: $\alpha = \frac{[\text{H}^+]}{c} = \frac{10^{-4}}{1.5\times10^{-3}} = \frac{1}{15}$

$$\Lambda_m^o = \frac{\Lambda_m}{\alpha} = 40 \times 15 = 600 = 6\times10^2$$

$Z = 6$.

**Answer:** 6"""
)

# Q29: Chem - Lone pairs count, gold=6
solutions[29] = (
r"""**Key Concepts:** VSEPR — counting lone pairs on central atoms.

**$[\text{TeBr}_6]^{2-}$:** Te: 6 valence $e^-$ + 2 (charge) = 8. Bonds = 6. Lone pairs = $\frac{8-6}{2} = 1$.

**$[\text{BrF}_2]^+$:** Br: 7 valence $e^-$ - 1 (charge) = 6. Bonds = 2. Lone pairs = $\frac{6-2}{2} = 2$.

**$\text{SNF}_3$ (i.e., $\text{NSF}_3$):** S is central. S: 6 valence $e^-$. Forms 3 S-F bonds + 1 S=N double bond = 5 bonding pairs using 10 electrons from shared pairs, but S contributes 6. With expanded octet: S has **0 lone pairs** (all 6 electrons in bonds).

**$[\text{XeF}_3]^-$:** Xe: 8 valence $e^-$ + 1 (charge) = 9. Bonds = 3. Remaining = 6 electrons = **3 lone pairs**.

Total = $1 + 2 + 0 + 3 = 6$.

**Answer:** 6"""
)

# Q30: Chem - Diamagnetic species, gold=5
solutions[30] = (
r"""**Key Concepts:** Molecular orbital theory — diamagnetic means all electrons paired.

- $\text{H}_2$: $(\sigma_{1s})^2$ — **diamagnetic** $\checkmark$
- $\text{He}_2^+$: $(\sigma_{1s})^2(\sigma^*_{1s})^1$ — 1 unpaired — **paramagnetic**
- $\text{Li}_2$: $(\sigma_{2s})^2$ — **diamagnetic** $\checkmark$
- $\text{Be}_2$: $(\sigma_{2s})^2(\sigma^*_{2s})^2$ — bond order 0, doesn't exist as stable species
- $\text{B}_2$: $(\pi_{2p})^1(\pi_{2p})^1$ — 2 unpaired — **paramagnetic**
- $\text{C}_2$: $(\pi_{2p})^4$ — **diamagnetic** $\checkmark$
- $\text{N}_2$: all paired — **diamagnetic** $\checkmark$
- $\text{O}_2^-$: $(\pi^*_{2p})^3$ — 1 unpaired — **paramagnetic**
- $\text{F}_2$: $(\pi^*_{2p})^4$ — **diamagnetic** $\checkmark$

Diamagnetic species: $\text{H}_2$, $\text{Li}_2$, $\text{C}_2$, $\text{N}_2$, $\text{F}_2$ = **5** (excluding $\text{Be}_2$ which has bond order 0).

**Answer:** 5"""
)

# Q31: Math - Hyperbola tangent, right triangle, gold=ABC
solutions[31] = (
r"""**Key Concepts:** Tangent condition for hyperbola, Pythagorean theorem.

Line $y = 2x + 1$ tangent to $\frac{x^2}{a^2} - \frac{y^2}{16} = 1$: $c^2 = a^2m^2 - b^2 \Rightarrow 1 = 4a^2 - 16 \Rightarrow a^2 = 17/4$, $a = \sqrt{17}/2$.

Check which CANNOT be sides of a right triangle (largest side squared $\neq$ sum of squares of other two):

**(A)** $\sqrt{17}/2, 4, 1$: $4^2 = 16$, $17/4 + 1 = 21/4 = 5.25 \neq 16$. $16+1 = 17 \neq 17/4$. $17/4+16 = 81/4, \neq 1$. **Cannot.** $\checkmark$

**(B)** $\sqrt{17}/2, 4, 2$: $16 \neq 17/4+4 = 33/4$. $17/4+16 = 81/4 \neq 4$. $4+16=20 \neq 17/4$. **Cannot.** $\checkmark$

**(C)** $\sqrt{17}, 8, 1$: $64 \neq 17+1 = 18$. $17+64=81 \neq 1$. $1+64 = 65 \neq 17$. **Cannot.** $\checkmark$

**(D)** $\sqrt{17}, 4, 1$: $4^2+1^2 = 17 = (\sqrt{17})^2$. This IS a right triangle. **Can.** $\times$

**Answer:** ABC"""
)

# Q32: Math - Parabola chord midpoint, gold=C
solutions[32] = (
r"""**Key Concepts:** Equation of chord with given midpoint on a parabola.

For $y^2 = 16x$, chord with midpoint $(h,k)$: $ky - 8(x+h) = k^2 - 16h$, i.e., $ky - 8x = k^2 - 8h$.

Comparing with $2x + y = p$ (i.e., $-2x - y = -p$, or $y(-1) + x(-2) = -p$):

$$\frac{k}{1} = \frac{-8}{2} \Rightarrow k = -4$$

$$\frac{k^2-8h}{p} = -4 \Rightarrow p = \frac{16-8h}{-4} = 2h - 4$$

Also need midpoint inside parabola: $k^2 < 16h \Rightarrow 16 < 16h \Rightarrow h > 1$.

**(A)** $k=-4$, $h=2$: $p = 0 \neq -2$. $\times$
**(B)** $k=-3 \neq -4$. $\times$
**(C)** $k=-4$, $h=3$: $p = 2 \checkmark$, $h > 1 \checkmark$. **Correct.** $\checkmark$
**(D)** $k=-3 \neq -4$. $\times$

**Answer:** C"""
)

# Q33: Math - IVT applications, gold=AB
solutions[33] = (
r"""**Key Concepts:** Intermediate Value Theorem for continuous functions. $f: \mathbb{R} \to (0,1)$ continuous.

**(A)** $h(x) = x^9 - f(x)$: $h(0) = -f(0) < 0$, $h(1) = 1 - f(1) > 0$. By IVT, zero in $(0,1)$. $\checkmark$

**(B)** $h(x) = x - \int_0^{\pi/2-x} f(t)\cos t\,dt$: $h(0) = -\int_0^{\pi/2} f(t)\cos t\,dt < 0$. $h(1) = 1 - \int_0^{\pi/2-1} f(t)\cos t\,dt > 1 - \sin(\pi/2-1) = 1 - \cos 1 \approx 0.46 > 0$. By IVT, zero exists. $\checkmark$

**(C)** $h(x) = e^x - \int_0^x f(t)\sin t\,dt$: $h(0) = 1 > 0$. For $x \in (0,1)$: $h(x) \geq e^0 - \int_0^1 1\cdot\sin t\,dt = 1 - (1-\cos1) \approx 0.46 > 0$. Actually $e^x > 1$ and the integral $< 1$, so $h > 0$. No zero. $\times$

**(D)** $h(x) = f(x) + \int_0^{\pi/2} f(t)\sin t\,dt > 0$ always (sum of positive terms). No zero. $\times$

**Answer:** AB"""
)

# Q34: Math - Matrix square, gold=BD
solutions[34] = (
r"""**Key Concepts:** If $A = B^2$ for real $B$, then $\det(A) = (\det B)^2 \geq 0$.

**(A)** $I$: $\det = 1 \geq 0$, and $I = I^2$. **Can be a square.** $\times$

**(B)** $\text{diag}(1,1,-1)$: $\det = -1 < 0$. Since $\det(B^2) \geq 0$, this **cannot** be $B^2$. $\checkmark$

**(C)** $\text{diag}(1,-1,-1)$: $\det = 1 \geq 0$. Take $B = \begin{bmatrix}1&0&0\\0&0&-1\\0&1&0\end{bmatrix}$, then $B^2 = \text{diag}(1,-1,-1)$. **Can be a square.** $\times$

**(D)** $-I$: $\det = -1 < 0$. **Cannot** be $B^2$. $\checkmark$

**Answer:** BD"""
)

# Q35: Math - Complex number Im condition, gold=AB
solutions[35] = (
r"""**Key Concepts:** Extracting imaginary part of a complex fraction.

$z = x+iy$, $a-b = 1$, $y \neq 0$.

$$\text{Im}\left(\frac{az+b}{z+1}\right) = \frac{y(a-b)}{(x+1)^2+y^2} = \frac{y}{(x+1)^2+y^2} = y$$

Dividing by $y \neq 0$: $(x+1)^2 + y^2 = 1$.

$$x = -1 \pm \sqrt{1-y^2}$$

This matches options (A) $x = -1+\sqrt{1-y^2}$ and (B) $x = -1-\sqrt{1-y^2}$.

**Answer:** AB"""
)

# Q36: Math - Probability, gold=AB
solutions[36] = (
r"""**Key Concepts:** Conditional probability formulas.

$P(X) = 1/3$, $P(X|Y) = 1/2$, $P(Y|X) = 2/5$.

$P(X \cap Y) = P(Y|X)\cdot P(X) = \frac{2}{5}\cdot\frac{1}{3} = \frac{2}{15}$

$P(Y) = \frac{P(X\cap Y)}{P(X|Y)} = \frac{2/15}{1/2} = \frac{4}{15}$

**(A)** $P(Y) = 4/15$. **Correct.** $\checkmark$
**(B)** $P(X'|Y) = 1 - 1/2 = 1/2$. **Correct.** $\checkmark$
**(C)** $P(X\cap Y) = 2/15 \neq 1/5$. **Incorrect.** $\times$
**(D)** $P(X\cup Y) = 1/3 + 4/15 - 2/15 = 7/15 \neq 2/5$. **Incorrect.** $\times$

**Answer:** AB"""
)

# Q37: Math - Circle and axes 3 common points, gold=2
solutions[37] = (
r"""**Key Concepts:** Circle-axes intersection analysis.

Circle: $(x+1)^2 + (y+2)^2 = p+5$. Center $(-1,-2)$, radius$^2 = p+5$.

**$x$-axis ($y=0$):** $x^2+2x-p=0$, discriminant $\Delta_x = 4+4p$.
**$y$-axis ($x=0$):** $y^2+4y-p=0$, discriminant $\Delta_y = 16+4p$.

For exactly 3 total intersection points:

**Case 1: Tangent to $x$-axis (1 point) + 2 points on $y$-axis:**
$\Delta_x = 0 \Rightarrow p = -1$. Check $\Delta_y = 16-4 = 12 > 0$: 2 points on $y$-axis. $x$-axis point: $(-1,0)$. $y$-axis points: $(0, -2\pm\sqrt{3})$. All distinct. Total = 3. $\checkmark$

**Case 2: Circle passes through origin** (shared point on both axes):
$p = 0$. $x$-axis: $x(x+2)=0$: points $(0,0),(-2,0)$. $y$-axis: $y(y+4)=0$: points $(0,0),(0,-4)$. Distinct points: $(0,0),(-2,0),(0,-4)$ = 3. $\checkmark$

**Case 3: Tangent to $y$-axis + 2 on $x$-axis:**
$\Delta_y = 0 \Rightarrow p = -4$. $\Delta_x = 4-16 = -12 < 0$: 0 points on $x$-axis. Total = 1. $\times$

Two values: $p = -1$ and $p = 0$.

**Answer:** 2"""
)

# Q38: Math - g(x) limit, gold=2
solutions[38] = (
r"""**Key Concepts:** Recognizing derivative of a product in the integrand.

$$g(x) = \int_x^{\pi/2}[f'(t)\csc t - \cot t\csc t\cdot f(t)]\,dt$$

Notice: $\frac{d}{dt}[f(t)\csc t] = f'(t)\csc t - f(t)\csc t\cot t$, which is exactly the integrand.

$$g(x) = [f(t)\csc t]_x^{\pi/2} = f(\pi/2)\csc(\pi/2) - f(x)\csc x = 3 - \frac{f(x)}{\sin x}$$

$$\lim_{x\to 0} g(x) = 3 - \lim_{x\to 0}\frac{f(x)}{\sin x} = 3 - \frac{f'(0)}{1} = 3 - 1 = 2$$

(using L'Hopital since $f(0) = \sin 0 = 0$).

**Answer:** 2"""
)

# Q39: Math - Linear system infinite solutions, gold=1
solutions[39] = (
r"""**Key Concepts:** Determinant condition for infinite solutions.

$$\det\begin{bmatrix}1&\alpha&\alpha^2\\\alpha&1&\alpha\\\alpha^2&\alpha&1\end{bmatrix} = (1-\alpha^2)^2 = 0 \Rightarrow \alpha = \pm 1$$

**$\alpha = 1$:** All rows become $[1,1,1]$, giving $x+y+z = 1$ and $x+y+z = -1$ — contradiction. No solution.

**$\alpha = -1$:** All rows become $[1,-1,1]$ (up to sign), giving $x-y+z = 1$ (consistent with RHS). Infinitely many solutions. $\checkmark$

$1 + \alpha + \alpha^2 = 1 + (-1) + 1 = 1$.

**Answer:** 1"""
)

# Q40: Math - Words counting y/9x, gold=5
solutions[40] = (
r"""**Key Concepts:** Permutations with repetition.

$x$ = number of 10-letter words using A-J with no repetition: $x = 10!$

$y$ = exactly one letter repeated twice, rest appear once:
- Choose repeated letter: $\binom{10}{1} = 10$
- Choose 8 more from remaining 9: $\binom{9}{8} = 9$
- Arrange 10 letters (one repeated twice): $\frac{10!}{2!}$

$$y = 10 \times 9 \times \frac{10!}{2}$$

$$\frac{y}{9x} = \frac{10 \times 9 \times 10!/(2)}{9 \times 10!} = \frac{10}{2} = 5$$

**Answer:** 5"""
)

# Q41: Math - Right triangle AP sides area 24, gold=6
solutions[41] = (
r"""**Key Concepts:** Sides in AP, Pythagorean theorem.

Sides in AP: $a-d$, $a$, $a+d$ (hypotenuse = largest).

$$(a+d)^2 = (a-d)^2 + a^2 \Rightarrow 4ad = a^2 \Rightarrow d = a/4$$

Sides: $3a/4$, $a$, $5a/4$ (ratio $3:4:5$).

$$\text{Area} = \frac{1}{2}\cdot\frac{3a}{4}\cdot a = \frac{3a^2}{8} = 24 \Rightarrow a^2 = 64 \Rightarrow a = 8$$

Smallest side $= 3(8)/4 = 6$.

**Answer:** 6"""
)

# Q42: Phy - Expanding sphere, gold=A
solutions[42] = (
r"""**Key Concepts:** Mass conservation with uniform density.

$M = \rho\cdot\frac{4}{3}\pi R^3 = \text{const}$, so $\rho R^3 = \text{const}$.

Differentiating: $\frac{1}{\rho}\frac{d\rho}{dt} = -\frac{3}{R}\frac{dR}{dt} = k$ (constant).

$$v = \frac{dR}{dt} = -\frac{kR}{3} \propto R$$

**Answer:** A"""
)

# Q43: Phy - Photoelectric de Broglie, gold=D
solutions[43] = (
r"""**Key Concepts:** Photoelectric effect + de Broglie wavelength.

$KE = \frac{hc}{\lambda} - \phi_0 = \frac{h^2}{2m\lambda_d^2}$

Differentiating: $-\frac{h^2}{m\lambda_d^3}\Delta\lambda_d = -\frac{hc}{\lambda^2}\Delta\lambda$

$$\frac{\Delta\lambda_d}{\Delta\lambda} = \frac{mc\lambda_d^3}{h\lambda^2} \propto \frac{\lambda_d^3}{\lambda^2}$$

**Answer:** D"""
)

# Q44: Phy - Escape velocity Sun-Earth, gold=B
solutions[44] = (
r"""**Key Concepts:** Gravitational escape from two-body system.

$M_S = 3\times10^5 M_E$, $d = 2.5\times10^4 R_E$, $v_e = 11.2$ km/s.

$$v_s^2 = \frac{2GM_E}{R_E} + \frac{2GM_S}{d} = v_e^2 + \frac{2G\cdot3\times10^5 M_E}{2.5\times10^4 R_E} = v_e^2 + 12v_e^2 = 13v_e^2$$

$$v_s = v_e\sqrt{13} = 11.2\times3.606 \approx 40.4 \text{ km/s} \approx 42 \text{ km/s}$$

**Answer:** B"""
)

# Q45: Phy - Error in well depth, gold=B
solutions[45] = (
r"""**Key Concepts:** Error propagation in indirect measurement.

$L = 20$ m, $g = 10$ m/s$^2$, $v_s = 300$ m/s, $\delta T = 0.01$ s.

$t_1 = \sqrt{2L/g} = 2$ s, $t_2 = L/v_s = 1/15$ s.

$$\frac{dT}{dL} = \frac{1}{gt_1} + \frac{1}{v_s} = \frac{1}{20} + \frac{1}{300} = \frac{16}{300}$$

$$\delta L = \frac{\delta T}{dT/dL} = \frac{0.01\times300}{16} \approx 0.1875$$

$$\frac{\delta L}{L} = \frac{0.1875}{20} \approx 0.94\% \approx 1\%$$

**Answer:** B"""
)

# Q46: Phy - Three-phase voltages, gold=AD
solutions[46] = (
r"""**Key Concepts:** Phasor subtraction for sinusoidal voltages with $120°$ phase difference.

$V_{XY} = V_X - V_Y$. Phase difference = $2\pi/3$.

Peak value: $|V_{XY}| = V_0\sqrt{1+1-2\cos(2\pi/3)} = V_0\sqrt{2+1} = V_0\sqrt{3}$

$$V_{XY}^{rms} = \frac{V_0\sqrt{3}}{\sqrt{2}} = V_0\sqrt{3/2}$$

By symmetry (all phase differences are $2\pi/3$), $V_{YZ}^{rms} = V_0\sqrt{3/2}$ as well.

**(A)** $V_{XY}^{rms} = V_0\sqrt{3/2}$. $\checkmark$
**(B)** $V_{YZ}^{rms} = V_0\sqrt{1/2}$. Wrong — it's $V_0\sqrt{3/2}$. $\times$
**(C)** $V_{XY}^{rms} = V_0$. Wrong. $\times$
**(D)** Reading is independent of terminal choice (all give $V_0\sqrt{3/2}$). $\checkmark$

**Answer:** AD"""
)

# Q47: Chem - Electrochemical cell, gold=B
solutions[47] = (
r"""**Key Concepts:** Nernst equation and Gibbs free energy.

$\text{Zn}|\text{ZnSO}_4||\text{CuSO}_4|\text{Cu}$, $E° = 1.1$ V, $n = 2$.

$[\text{Zn}^{2+}] = 10[\text{Cu}^{2+}]$, so $Q = [\text{Zn}^{2+}]/[\text{Cu}^{2+}] = 10$.

$$E = E° - \frac{RT}{nF}\ln Q = 1.1 - \frac{RT}{2F}\ln 10 = 1.1 - \frac{2.303RT}{2F}$$

$$\Delta G = -nFE = -2F\left(1.1 - \frac{2.303RT}{2F}\right) = -2.2F + 2.303RT$$

$$\Delta G = 2.303RT - 2.2F$$

**Answer:** B"""
)

# Q48: Chem - Graphite to diamond pressure, gold=A
solutions[48] = (
r"""**Key Concepts:** Pressure dependence of Gibbs free energy for equilibrium.

$$\Delta G(P) = \Delta G° + \Delta V(P - 1) = 0 \text{ at equilibrium}$$

$\Delta G° = 2900$ J/mol, $\Delta V = -2\times10^{-6}$ m$^3$/mol.

$$0 = 2900 + (-2\times10^{-6})(P-1)\times10^5$$
$$0 = 2900 - 0.2(P-1)$$
$$P - 1 = 14500 \Rightarrow P = 14501 \text{ bar}$$

**Answer:** A"""
)

# Q49: Chem - H2 gas production, gold=C
solutions[49] = (
r"""**Key Concepts:** Reactivity of metals with acids/bases.

**(A)** Fe + conc. $\text{HNO}_3$: Fe becomes passive. $\text{HNO}_3$ produces $\text{NO}_2$, not $\text{H}_2$. $\times$

**(B)** Cu + conc. $\text{HNO}_3$: Produces $\text{NO}_2$, not $\text{H}_2$. Cu is below H in activity series. $\times$

**(C)** Zn + NaOH(aq): Zn is amphoteric.
$$\text{Zn} + 2\text{NaOH} + 2\text{H}_2\text{O} \to \text{Na}_2[\text{Zn(OH)}_4] + \text{H}_2\uparrow$$
**Produces $\text{H}_2$.** $\checkmark$

**(D)** Au + NaCN + air: Forms $[\text{Au(CN)}_2]^-$ complex. No $\text{H}_2$. $\times$

**Answer:** C"""
)

# Q50: Chem - Oxidation states of P, gold=C
solutions[50] = (
r"""**Key Concepts:** Oxidation state calculation for phosphorus compounds.

- $\text{H}_3\text{PO}_2$: $3(+1) + x + 2(-2) = 0 \Rightarrow x = +1$
- $\text{H}_3\text{PO}_4$: $3(+1) + x + 4(-2) = 0 \Rightarrow x = +5$
- $\text{H}_3\text{PO}_3$: $3(+1) + x + 3(-2) = 0 \Rightarrow x = +3$
- $\text{H}_4\text{P}_2\text{O}_6$: $4(+1) + 2x + 6(-2) = 0 \Rightarrow x = +4$

Order: $\text{H}_3\text{PO}_4(+5) > \text{H}_4\text{P}_2\text{O}_6(+4) > \text{H}_3\text{PO}_3(+3) > \text{H}_3\text{PO}_2(+1)$

**Answer:** C"""
)

# Q51: Chem - Surface properties, gold=AB
solutions[51] = (
r"""**Key Concepts:** Adsorption thermodynamics, colloidal chemistry.

**(A)** Adsorption: $\Delta H < 0$ (exothermic, surface energy decreases), $\Delta S < 0$ (adsorbate becomes ordered on surface). **Correct.** $\checkmark$

**(B)** Higher critical temperature = more easily liquefiable = more easily adsorbed. Ethane ($T_c$ much higher) is adsorbed more than nitrogen ($T_c = 126$ K). **Correct.** $\checkmark$

**(C)** Cloud is an **aerosol** (liquid in gas), not an emulsion (liquid in liquid). **Incorrect.** $\times$

**(D)** Brownian motion depends on particle size — smaller particles show more vigorous motion. **Incorrect** (statement claims no size dependence). $\times$

**Answer:** AB"""
)

# Write output
with open(input_path, 'r') as f:
    lines = f.readlines()

output_lines = []
for i, line in enumerate(lines):
    data = json.loads(line.strip())
    data['cot_solution'] = solutions[i]
    output_lines.append(json.dumps(data, ensure_ascii=False))

with open(output_path, 'w') as f:
    for ol in output_lines:
        f.write(ol + '\n')

print(f"Wrote {len(output_lines)} solutions to {output_path}")

# Verify all answers match gold
all_ok = True
for i, ol in enumerate(output_lines):
    data = json.loads(ol)
    gold = data['gold']
    sol = data['cot_solution']
    if f"**Answer:** {gold}" not in sol:
        print(f"WARNING Q{i}: gold={gold} not found in solution!")
        all_ok = False

if all_ok:
    print("All 52 solutions verified: gold answers match.")
