import json

input_path = "/Users/apple/jee-finetune/data/batches/batch_00.jsonl"
output_path = "/Users/apple/jee-finetune/data/batches/batch_00_solutions.jsonl"

# Read all questions
questions = []
with open(input_path, 'r') as f:
    for line in f:
        line = line.strip()
        if line:
            questions.append(json.loads(line))

print(f"Read {len(questions)} questions")

# Solutions dictionary keyed by (description, index)
solutions = {}

# ============================================================
# QUESTION 1: Planck's constant from photoelectric effect
# ============================================================
solutions[("JEE Adv 2016 Paper 1", 1)] = r"""We use the photoelectric equation: $eV_0 = \frac{hc}{\lambda} - \phi$, where $\phi$ is the work function.

Using the data points $\lambda_1 = 0.3\,\mu\text{m}$, $V_{0,1} = 2.0\,\text{V}$ and $\lambda_2 = 0.4\,\mu\text{m}$, $V_{0,2} = 1.0\,\text{V}$:

$$eV_{0,1} = \frac{hc}{\lambda_1} - \phi \quad \text{and} \quad eV_{0,2} = \frac{hc}{\lambda_2} - \phi$$

Subtracting: $e(V_{0,1} - V_{0,2}) = hc\left(\frac{1}{\lambda_1} - \frac{1}{\lambda_2}\right)$

$$h = \frac{e(V_{0,1} - V_{0,2})}{c\left(\frac{1}{\lambda_1} - \frac{1}{\lambda_2}\right)}$$

Computing the denominator:
$$\frac{1}{\lambda_1} - \frac{1}{\lambda_2} = \frac{1}{0.3 \times 10^{-6}} - \frac{1}{0.4 \times 10^{-6}} = \frac{10^6}{0.3} - \frac{10^6}{0.4} = 10^6\left(\frac{10}{3} - \frac{10}{4}\right) = 10^6 \times \frac{10}{12} = \frac{10^7}{12}$$

Numerator: $e(V_{0,1} - V_{0,2}) = 1.6 \times 10^{-19} \times 1.0 = 1.6 \times 10^{-19}\,\text{J}$

$$h = \frac{1.6 \times 10^{-19}}{3 \times 10^8 \times \frac{10^7}{12}} = \frac{1.6 \times 10^{-19} \times 12}{3 \times 10^{15}} = \frac{19.2 \times 10^{-19}}{3 \times 10^{15}} = 6.4 \times 10^{-34}\,\text{J s}$$

**Answer:** B"""

# ============================================================
# QUESTION 2: Stick on wall
# ============================================================
solutions[("JEE Adv 2016 Paper 1", 2)] = r"""Let the stick of mass $m = 1.6\,\text{kg}$ and length $l$ make angle $30°$ with the vertical wall. The wall reaction $N_w$ is perpendicular to the stick, and $N_w = N_f$ (reaction of floor).

Setting up coordinates with the bottom of the stick at origin on the floor. The stick makes $30°$ with the wall (i.e., $60°$ with horizontal). The contact point with the wall is at height $h$.

The distance along the stick to the wall contact: since the wall is vertical at height $h$, the stick touches at distance $d$ from the bottom where $d\cos 60° = $ horizontal distance from bottom to wall and $d\sin 60° = h$. Actually, the wall is at height $h$, so $d \sin 60° = h$, giving $d = h/\sin 60° = 2h/\sqrt{3}$.

The stick makes angle $30°$ with the wall, so $60°$ with the floor.

Forces on stick: weight $mg$ at center ($l/2$ from bottom), normal from wall $N_w$ (perpendicular to stick at distance $d$ from bottom), normal from floor $N_f$ (vertical, at bottom), friction $f$ (horizontal, at bottom).

Taking torques about the bottom point:
- $mg$ acts at $l/2$ from bottom; moment arm = $(l/2)\cos 60° = l/4$
- $N_w$ acts at $d = 2h/\sqrt{3}$ from bottom, perpendicular to stick

$$N_w \cdot d = mg \cdot \frac{l}{2}\cos 60°$$
$$N_w \cdot \frac{2h}{\sqrt{3}} = mg \cdot \frac{l}{4}$$

Force balance:
- Horizontal: $f = N_w \sin 60° = \frac{\sqrt{3}}{2}N_w$
- Vertical: $N_f = mg - N_w \cos 60° = mg - \frac{N_w}{2}$

Given $N_w = N_f$: $N_w = mg - \frac{N_w}{2}$, so $\frac{3N_w}{2} = mg$, giving $N_w = \frac{2mg}{3}$.

From the torque equation:
$$\frac{2mg}{3} \cdot \frac{2h}{\sqrt{3}} = mg \cdot \frac{l}{4}$$
$$\frac{4h}{3\sqrt{3}} = \frac{l}{4}$$
$$\frac{h}{l} = \frac{3\sqrt{3}}{16}$$

Friction: $f = \frac{\sqrt{3}}{2} \cdot \frac{2mg}{3} = \frac{\sqrt{3}mg}{3} = \frac{\sqrt{3} \times 16}{3} = \frac{16\sqrt{3}}{3}\,\text{N}$

**Answer:** D"""

# ============================================================
# QUESTION 3: Rydberg states
# ============================================================
solutions[("JEE Adv 2016 Paper 1", 6)] = r"""For hydrogen-like atoms with quantum number $n$:

**Radii:** $r_n = \frac{n^2 a_0}{Z}$

Relative change in radii of consecutive orbitals:
$$\frac{\Delta r}{r_n} = \frac{r_{n+1} - r_n}{r_n} = \frac{(n+1)^2 - n^2}{n^2} = \frac{2n+1}{n^2} \approx \frac{2}{n} \text{ for } n \gg 1$$

This does not depend on $Z$ (Statement A is TRUE), and varies as $1/n$ (not exactly $1/n$ but approximately $2/n$, so Statement B is TRUE).

**Energy:** $E_n = -\frac{13.6 Z^2}{n^2}\,\text{eV}$

$$\frac{\Delta E}{E_n} = \frac{E_{n+1} - E_n}{E_n} = \frac{\frac{1}{n^2} - \frac{1}{(n+1)^2}}{\frac{1}{n^2}} = 1 - \frac{n^2}{(n+1)^2} = \frac{2n+1}{(n+1)^2} \approx \frac{2}{n}$$

This varies as $1/n$, not $1/n^3$ (Statement C is FALSE).

**Angular momentum:** $L_n = n\hbar$

$$\frac{\Delta L}{L_n} = \frac{(n+1)\hbar - n\hbar}{n\hbar} = \frac{1}{n}$$

Statement D is TRUE.

**Answer:** ABD"""

# ============================================================
# QUESTION 4: Incandescent bulb filament
# ============================================================
solutions[("JEE Adv 2016 Paper 1", 8)] = r"""As tungsten evaporates non-uniformly, some sections become thinner, increasing their resistance. At constant voltage, current through the filament decreases with time as total resistance increases.

(A) FALSE: Thinner sections have higher resistance, dissipate more power per unit length, and become hotter. The temperature distribution is non-uniform.

(B) FALSE: Resistance of small sections increases with time as the filament becomes thinner (and also hotter at those points). The cross-sectional area decreases, so $R = \rho l/A$ increases.

(C) TRUE: Thinner sections get hotter. By Wien's law, the peak frequency of blackbody radiation shifts higher with temperature. The filament emits more light at higher frequencies before breaking.

(D) TRUE: Total resistance increases over time. At constant voltage, $P = V^2/R$ decreases. The filament consumes less electrical power towards end of life.

**Answer:** CD"""

# ============================================================
# QUESTION 5: Plano-convex lens
# ============================================================
solutions[("JEE Adv 2016 Paper 1", 9)] = r"""The lens has a flat surface and a curved (convex) surface with radius $R$.

**From reflection at convex surface:** The convex surface acts as a convex mirror with focal length $f_m = R/2$.

Using mirror formula: $\frac{1}{v} + \frac{1}{u} = \frac{1}{f_m}$

Object is at $u = -30\,\text{cm}$ (in front of convex surface). The faint image is at $10\,\text{cm}$ away. For a convex mirror, the image is virtual and behind the mirror, so $v = +10\,\text{cm}$.

$$\frac{1}{10} + \frac{1}{-30} = \frac{1}{f_m} = \frac{2}{30} = \frac{1}{15}$$

So $f_m = 15\,\text{cm}$, giving $R = 30\,\text{cm}$.

The faint image from the convex mirror is virtual and erect (Statement C is FALSE — it's virtual, not real).

**From refraction (lens):** The image is double the size. For a plano-convex lens with curved surface facing the object:

Using the lens-maker's equation: $\frac{1}{f} = (n-1)\left(\frac{1}{R_1} - \frac{1}{R_2}\right)$

For plano-convex lens: $R_1 = R = 30\,\text{cm}$ (convex, facing object), $R_2 = \infty$ (flat).

$$\frac{1}{f} = (n-1) \cdot \frac{1}{30}$$

The image is double size with $u = -30\,\text{cm}$. If real image: $m = -2$, so $v = 60\,\text{cm}$.

$$\frac{1}{60} - \frac{1}{-30} = \frac{1}{f} \implies \frac{1}{60} + \frac{1}{30} = \frac{3}{60} = \frac{1}{20}$$

So $f = 20\,\text{cm}$ (Statement D is TRUE).

$(n-1)/30 = 1/20 \implies n-1 = 3/2 \implies n = 2.5$ (Statement A is TRUE).

Statement B: $R = 30\,\text{cm} \neq 45\,\text{cm}$ (FALSE).

**Answer:** AD"""

# ============================================================
# QUESTION 6: Dimensional analysis for length scale
# ============================================================
solutions[("JEE Adv 2016 Paper 1", 10)] = r"""We need dimensions of each quantity:
- $[\varepsilon] = M^{-1}L^{-3}T^4A^2$ (permittivity)
- $[k_B] = ML^2T^{-2}K^{-1}$ (Boltzmann constant)
- $[T] = K$ (temperature)
- $[n] = L^{-3}$ (number density)
- $[q] = AT$ (charge)

So $[q^2] = A^2T^2$ and $[\varepsilon k_B T] = M^{-1}L^{-3}T^4A^2 \cdot ML^2T^{-2}K^{-1} \cdot K = L^{-1}T^2A^2$.

**Option B:** $\frac{\varepsilon k_B T}{n q^2}$ has dimensions $\frac{L^{-1}T^2A^2}{L^{-3} \cdot A^2T^2} = L^2$. So $l = \sqrt{\frac{\varepsilon k_B T}{nq^2}}$ has dimension $L$. **CORRECT.**

**Option A:** $\frac{nq^2}{\varepsilon k_B T} = L^{-2}$. Square root gives $L^{-1}$. **INCORRECT.**

**Option C:** $\frac{q^2}{\varepsilon n^{2/3} k_B T}$ has dimensions $\frac{A^2T^2}{L^{-1}T^2A^2 \cdot L^{-2}} = \frac{1}{L^{-3}} = L^3$. Wait, let me redo: $[\varepsilon n^{2/3} k_B T] = L^{-1}T^2A^2 \cdot L^{-2} = L^{-3}T^2A^2$. Then $\frac{q^2}{\varepsilon n^{2/3} k_B T} = \frac{A^2T^2}{L^{-3}T^2A^2} = L^3$. Square root gives $L^{3/2}$. **INCORRECT.**

**Option D:** $\frac{q^2}{\varepsilon n^{1/3} k_B T}$: $[\varepsilon n^{1/3} k_B T] = L^{-1}T^2A^2 \cdot L^{-1} = L^{-2}T^2A^2$. Then $\frac{A^2T^2}{L^{-2}T^2A^2} = L^2$. Square root gives $L$. **CORRECT.**

**Answer:** BD"""

# ============================================================
# QUESTION 7: Position vector, velocity, angular momentum, force, torque
# ============================================================
solutions[("JEE Adv 2016 Paper 1", 12)] = r"""Given $\vec{r}(t) = \alpha t^3 \hat{i} + \beta t^2 \hat{j}$ with $\alpha = 10/3\,\text{m/s}^3$, $\beta = 5\,\text{m/s}^2$, $m = 0.1\,\text{kg}$.

**Velocity:** $\vec{v} = \frac{d\vec{r}}{dt} = 3\alpha t^2 \hat{i} + 2\beta t \hat{j}$

At $t = 1$: $\vec{v} = 3 \times \frac{10}{3} \times 1 \hat{i} + 2 \times 5 \times 1 \hat{j} = 10\hat{i} + 10\hat{j}\,\text{m/s}$ (Statement A is TRUE)

**Position at $t=1$:** $\vec{r} = \frac{10}{3}\hat{i} + 5\hat{j}$

**Angular momentum:** $\vec{L} = m(\vec{r} \times \vec{v}) = 0.1\left(\frac{10}{3}\hat{i} + 5\hat{j}\right) \times (10\hat{i} + 10\hat{j})$

$= 0.1\left(\frac{10}{3} \times 10 - 5 \times 10\right)\hat{k} = 0.1\left(\frac{100}{3} - 50\right)\hat{k} = 0.1 \times \left(-\frac{50}{3}\right)\hat{k} = -\frac{5}{3}\hat{k}\,\text{N m s}$

(Statement B is TRUE)

**Acceleration:** $\vec{a} = 6\alpha t \hat{i} + 2\beta \hat{j} = 20t\hat{i} + 10\hat{j}$

At $t=1$: $\vec{a} = 20\hat{i} + 10\hat{j}$

**Force:** $\vec{F} = m\vec{a} = 0.1(20\hat{i} + 10\hat{j}) = 2\hat{i} + 1\hat{j}\,\text{N}$ (Statement C is FALSE — it says $\hat{i} + 2\hat{j}$)

**Torque:** $\vec{\tau} = \vec{r} \times \vec{F} = \left(\frac{10}{3}\hat{i} + 5\hat{j}\right) \times (2\hat{i} + 1\hat{j})$

$= \left(\frac{10}{3} \times 1 - 5 \times 2\right)\hat{k} = \left(\frac{10}{3} - 10\right)\hat{k} = -\frac{20}{3}\hat{k}\,\text{N m}$ (Statement D is TRUE)

**Answer:** ABD"""

# ============================================================
# QUESTION 8: Stefan's law sensor reading
# ============================================================
solutions[("JEE Adv 2016 Paper 1", 14)] = r"""By Stefan-Boltzmann law, $P \propto T^4$ (in Kelvin).

At $T_1 = 487 + 273 = 760\,\text{K}$: sensor reads $\log_2(P_1/P_0) = 1$, so $P_1 = 2P_0$.

At $T_2 = 2767 + 273 = 3040\,\text{K}$: $\frac{T_2}{T_1} = \frac{3040}{760} = 4$

$$\frac{P_2}{P_1} = \left(\frac{T_2}{T_1}\right)^4 = 4^4 = 256$$

$$P_2 = 256 P_1 = 256 \times 2P_0 = 512 P_0$$

$$\log_2(P_2/P_0) = \log_2(512) = 9$$

**Answer:** 9"""

# ============================================================
# QUESTION 9: Beta decay kinetic energy
# ============================================================
solutions[("JEE Adv 2016 Paper 1", 15)] = r"""For $\beta^-$-decay: ${}^{12}_5\text{B} \to {}^{12}_6\text{C}^* + e^- + \bar{\nu}_e$

The Q-value for decay to the excited state:
$$Q = [m({}^{12}_5\text{B}) - m({}^{12}_6\text{C})]c^2 - E^*$$

where $E^* = 4.041\,\text{MeV}$ is the excitation energy. Note that atomic masses include electron masses, and the $\beta^-$ decay mass difference using atomic masses automatically accounts for the emitted electron.

$$Q = (12.014 - 12.000) \times 931.5 - 4.041$$
$$= 0.014 \times 931.5 - 4.041$$
$$= 13.041 - 4.041 = 9.0\,\text{MeV}$$

The maximum kinetic energy of the $\beta$-particle equals the Q-value (when the neutrino gets negligible energy and nuclear recoil is neglected).

$$K_{\max} = 9\,\text{MeV}$$

**Answer:** 9"""

# ============================================================
# QUESTION 10: Hydrogen emission spectrum lines
# ============================================================
solutions[("JEE Adv 2016 Paper 1", 16)] = r"""Energy of incident photon:
$$E = \frac{hc}{\lambda} = \frac{1.237 \times 10^{-6}}{970 \times 10^{-10}} = \frac{1.237 \times 10^{-6}}{9.7 \times 10^{-8}} = 12.75\,\text{eV}$$

The ground state energy is $E_1 = -13.6\,\text{eV}$.

The electron is excited to level $n$ where:
$$-13.6 + 12.75 = -0.85\,\text{eV} = \frac{-13.6}{n^2}$$
$$n^2 = \frac{13.6}{0.85} = 16 \implies n = 4$$

The number of spectral lines from level $n=4$:
$$\text{Lines} = \frac{n(n-1)}{2} = \frac{4 \times 3}{2} = 6$$

**Answer:** 6"""

# ============================================================
# QUESTION 11: Terminal velocity ratio
# ============================================================
solutions[("JEE Adv 2016 Paper 1", 17)] = r"""Terminal velocity: $v_t = \frac{2r^2(\rho_s - \rho_l)g}{9\eta}$

**Sphere P:** $r_P = 0.5\,\text{cm}$, $\rho_s = 8$, $\rho_l = 0.8$, $\eta_P = 3$

$$v_P = \frac{2(0.5)^2(8 - 0.8)g}{9 \times 3} = \frac{2 \times 0.25 \times 7.2 \times g}{27} = \frac{3.6g}{27}$$

**Sphere Q:** $r_Q = 0.25\,\text{cm}$, $\rho_s = 8$, $\rho_l = 1.6$, $\eta_Q = 2$

$$v_Q = \frac{2(0.25)^2(8 - 1.6)g}{9 \times 2} = \frac{2 \times 0.0625 \times 6.4 \times g}{18} = \frac{0.8g}{18}$$

$$\frac{v_P}{v_Q} = \frac{3.6g/27}{0.8g/18} = \frac{3.6}{27} \times \frac{18}{0.8} = \frac{3.6 \times 18}{27 \times 0.8} = \frac{64.8}{21.6} = 3$$

**Answer:** 3"""

# ============================================================
# QUESTION 12: Inductors and resistor in parallel
# ============================================================
solutions[("JEE Adv 2016 Paper 1", 18)] = r"""At $t = 0$ (switch on): inductors act as open circuits (oppose sudden change in current). Only the resistor $R = 12\,\Omega$ draws current.

$$I_{\min} = \frac{V}{R} = \frac{5}{12}\,\text{A}$$

At $t \to \infty$ (steady state): inductors act as pure resistors. All three are in parallel:

$L_1$: internal resistance $r_1 = 3\,\Omega$
$L_2$: internal resistance $r_2 = 4\,\Omega$
$R = 12\,\Omega$

$$\frac{1}{R_{eq}} = \frac{1}{3} + \frac{1}{4} + \frac{1}{12} = \frac{4 + 3 + 1}{12} = \frac{8}{12} = \frac{2}{3}$$

$$R_{eq} = \frac{3}{2}\,\Omega$$

$$I_{\max} = \frac{V}{R_{eq}} = \frac{5}{3/2} = \frac{10}{3}\,\text{A}$$

$$\frac{I_{\max}}{I_{\min}} = \frac{10/3}{5/12} = \frac{10}{3} \times \frac{12}{5} = 8$$

**Answer:** 8"""

# ============================================================
# QUESTION 13: Entropy of surroundings
# ============================================================
solutions[("JEE Adv 2016 Paper 1", 20)] = r"""For an isothermal expansion against constant external pressure:

Work done by gas: $W = P_{\text{ext}} \Delta V = 3.0\,\text{atm} \times (2.0 - 1.0)\,\text{L} = 3.0\,\text{L atm}$

Converting: $W = 3.0 \times 101.3 = 303.9\,\text{J}$

The heat absorbed by the surroundings equals the negative of the heat absorbed by the system. For an isothermal process of an ideal gas, $\Delta U = 0$, so $q_{\text{sys}} = W = 303.9\,\text{J}$.

Heat absorbed by surroundings: $q_{\text{surr}} = -q_{\text{sys}} = -303.9\,\text{J}$

$$\Delta S_{\text{surr}} = \frac{q_{\text{surr}}}{T} = \frac{-303.9}{300} = -1.013\,\text{J K}^{-1}$$

**Answer:** C"""

# ============================================================
# QUESTION 14: Atomic radii Group 13
# ============================================================
solutions[("JEE Adv 2016 Paper 1", 21)] = r"""In Group 13, going down the group, atomic radii generally increase. However, Ga has an anomalously small radius due to the poor shielding of the 3d electrons (d-block contraction).

The atomic radii are:
- Al: 143 pm
- Ga: 135 pm (smaller than Al due to d-block contraction)
- In: 167 pm
- Tl: 170 pm

Therefore the increasing order is: $\text{Ga} < \text{Al} < \text{In} < \text{Tl}$

**Answer:** B"""

# ============================================================
# QUESTION 15: Paramagnetic compounds
# ============================================================
solutions[("JEE Adv 2016 Paper 1", 22)] = r"""Let us check each compound:

1. **$[\text{Ni(CO)}_4]$**: Ni is in 0 oxidation state ($\text{Ni}^0$, $3d^{10}$). CO is a strong field ligand causing $sp^3$ hybridization. All electrons are paired. **Diamagnetic.**

2. **$[\text{NiCl}_4]^{2-}$**: Ni$^{2+}$ has $3d^8$ configuration. Cl$^-$ is a weak field ligand, so tetrahedral geometry with $sp^3$ hybridization. Has 2 unpaired electrons. **Paramagnetic.**

3. **$[\text{Co(NH}_3)_4\text{Cl}_2]\text{Cl}$**: Co$^{3+}$ has $3d^6$. With mixed ligands (NH$_3$ is moderate-strong field), in octahedral field it is typically low spin with all electrons paired. **Diamagnetic.**

4. **$\text{Na}_3[\text{CoF}_6]$**: Co$^{3+}$ has $3d^6$. F$^-$ is a weak field ligand, so high spin octahedral with 4 unpaired electrons. **Paramagnetic.**

5. **$\text{Na}_2\text{O}_2$**: Contains $\text{O}_2^{2-}$ (peroxide ion) with bond order 1, all electrons paired. **Diamagnetic.**

6. **$\text{CsO}_2$**: Contains $\text{O}_2^-$ (superoxide ion) with one unpaired electron. **Paramagnetic.**

Number of paramagnetic compounds = 3 ($[\text{NiCl}_4]^{2-}$, $\text{Na}_3[\text{CoF}_6]$, $\text{CsO}_2$).

**Answer:** B"""

# ============================================================
# QUESTION 16: Hydrogenation of natural rubber
# ============================================================
solutions[("JEE Adv 2016 Paper 1", 23)] = r"""Natural rubber is cis-1,4-polyisoprene, which is a polymer of isoprene (2-methyl-1,3-butadiene, $\text{CH}_2=\text{C(CH}_3)-\text{CH}=\text{CH}_2$).

The repeating unit is: $-\text{CH}_2-\text{C(CH}_3)=\text{CH}-\text{CH}_2-$

On complete hydrogenation, all C=C double bonds are reduced to C-C single bonds:

$-\text{CH}_2-\text{CH(CH}_3)-\text{CH}_2-\text{CH}_2-$

This is equivalent to an alternating copolymer of ethylene ($-\text{CH}_2-\text{CH}_2-$) and propylene ($-\text{CH}_2-\text{CH(CH}_3)-$) units.

Therefore, complete hydrogenation of natural rubber produces an ethylene-propylene copolymer.

**Answer:** A"""

# ============================================================
# QUESTION 17: Arrhenius equation
# ============================================================
solutions[("JEE Adv 2016 Paper 1", 24)] = r"""The Arrhenius equation is $k = Ae^{-E_a/RT}$.

**(A)** A high activation energy $E_a$ means $e^{-E_a/RT}$ is smaller, so $k$ is smaller. High $E_a$ implies a slow reaction. **FALSE.**

**(B)** As temperature $T$ increases, $e^{-E_a/RT}$ increases because more molecules have energy exceeding $E_a$. The rate constant increases due to greater number of effective collisions. **TRUE.**

**(C)** Taking the derivative: $\frac{d(\ln k)}{dT} = \frac{E_a}{RT^2}$. Higher $E_a$ means $\ln k$ changes more rapidly with temperature, so the temperature dependence is stronger. **TRUE.**

**(D)** The pre-exponential factor $A$ represents the frequency of collisions with proper orientation, irrespective of whether their energy exceeds $E_a$. It is indeed a measure of collision rate regardless of energy. **TRUE.**

**Answer:** BCD"""

# ============================================================
# QUESTION 18: Nuclear stability, N/P < 1
# ============================================================
solutions[("JEE Adv 2016 Paper 1", 25)] = r"""For an unstable nucleus with $N/P < 1$, there are too many protons relative to neutrons. The nucleus needs to decrease its proton number or increase its neutron number to become stable.

**(A) $\beta^-$-decay:** A neutron converts to a proton ($n \to p + e^- + \bar{\nu}$). This increases the proton number and decreases neutrons, making $N/P$ even smaller. **Not favorable.** FALSE.

**(B) K-electron capture:** A proton captures an inner orbital electron ($p + e^- \to n + \nu$). This decreases protons and increases neutrons, increasing $N/P$. **TRUE.**

**(C) Neutron emission:** This would decrease $N$ further, making $N/P$ even smaller. **Not favorable.** FALSE.

**(D) $\beta^+$-decay (positron emission):** A proton converts to a neutron ($p \to n + e^+ + \nu$). This decreases protons and increases neutrons, increasing $N/P$. **TRUE.**

**Answer:** BD"""

# ============================================================
# QUESTION 19: Borax structure
# ============================================================
solutions[("JEE Adv 2016 Paper 1", 26)] = r"""Borax has the formula $\text{Na}_2[\text{B}_4\text{O}_5(\text{OH})_4] \cdot 8\text{H}_2\text{O}$.

The tetranuclear unit $[\text{B}_4\text{O}_5(\text{OH})_4]^{2-}$ contains 4 boron atoms.

**(A)** The unit is indeed tetranuclear with the formula $[\text{B}_4\text{O}_5(\text{OH})_4]^{2-}$. **TRUE.**

**(B)** Two of the boron atoms are $sp^2$ hybridized (trigonal planar) and two are $sp^3$ hybridized (tetrahedral). Since the $sp^3$ borons are out of the plane of the $sp^2$ borons, all boron atoms are NOT in the same plane. **FALSE.**

**(C)** There are 2 boron atoms with $sp^2$ hybridization and 2 with $sp^3$ hybridization, so equal numbers. **TRUE.**

**(D)** Each boron atom is bonded to one terminal $-\text{OH}$ group, giving one terminal hydroxide per boron atom. There are 4 OH groups for 4 boron atoms. **TRUE.**

**Answer:** ACD"""

# ============================================================
# QUESTION 20: Lone pairs on central atom
# ============================================================
solutions[("JEE Adv 2016 Paper 1", 27)] = r"""Count the lone pairs on the central atom using VSEPR theory:

**(A) $\text{BrF}_5$:** Br has 7 valence electrons. With 5 bonds to F, there is $\frac{7-5}{2} = 1$ lone pair. Structure is square pyramidal. **ONE lone pair.**

**(B) $\text{ClF}_3$:** Cl has 7 valence electrons. With 3 bonds to F, there are $\frac{7-3}{2} = 2$ lone pairs. Structure is T-shaped. **TWO lone pairs. TRUE.**

**(C) $\text{XeF}_4$:** Xe has 8 valence electrons (considering expanded octet). With 4 bonds to F, there are $\frac{8-4}{2} = 2$ lone pairs. Structure is square planar. Wait: Xe has 8 valence electrons, forms 4 bonds using 4 electrons, leaving 4 electrons = 2 lone pairs. Also, total electron pairs around Xe = 4 bond pairs + 2 lone pairs = 6 (octahedral arrangement). **TWO lone pairs. TRUE.**

**(D) $\text{SF}_4$:** S has 6 valence electrons. With 4 bonds to F, there is $\frac{6-4}{2} = 1$ lone pair. Structure is see-saw. **ONE lone pair.**

**Answer:** BC"""

# ============================================================
# QUESTION 21: Selective precipitation of S2-
# ============================================================
solutions[("JEE Adv 2016 Paper 1", 28)] = r"""We need a reagent that precipitates $\text{S}^{2-}$ but NOT $\text{SO}_4^{2-}$.

**(A) $\text{CuCl}_2$:** $\text{CuS}$ is highly insoluble ($K_{sp}$ extremely low), while $\text{CuSO}_4$ is soluble. So $\text{Cu}^{2+}$ will selectively precipitate $\text{S}^{2-}$ as $\text{CuS}$. **TRUE.**

**(B) $\text{BaCl}_2$:** $\text{BaSO}_4$ is insoluble ($K_{sp}$ very low), and $\text{BaS}$ is soluble. So $\text{Ba}^{2+}$ would precipitate $\text{SO}_4^{2-}$, not selectively $\text{S}^{2-}$. **FALSE.**

**(C) $\text{Pb(OOCCH}_3)_2$:** Both $\text{PbS}$ and $\text{PbSO}_4$ are insoluble. This would precipitate both ions. **Not selective.** FALSE.

**(D) $\text{Na}_2[\text{Fe(CN)}_5\text{NO}]$:** Sodium nitroprusside gives a purple/violet coloration with $\text{S}^{2-}$ but does not precipitate it. It's a detection reagent, not a precipitating agent. **FALSE.**

**Answer:** A"""

# ============================================================
# QUESTION 22: Molecular weight ratio
# ============================================================
solutions[("JEE Adv 2016 Paper 1", 32)] = r"""Let the molecular weight of solute be $M_A$ and solvent be $M_B$.

Mole fraction of solute: $x_A = 0.1$, so $x_B = 0.9$.

Consider 1 mole of solution: 0.1 mol solute + 0.9 mol solvent.

Mass of solution: $0.1M_A + 0.9M_B$ grams.

**Molality:** $m = \frac{0.1}{0.9M_B/1000} = \frac{0.1 \times 1000}{0.9M_B} = \frac{1000}{9M_B}$

**Molarity:** Volume of solution $= \frac{\text{mass}}{\text{density}} = \frac{0.1M_A + 0.9M_B}{2.0}\,\text{cm}^3 = \frac{0.1M_A + 0.9M_B}{2000}\,\text{L}$

$$M = \frac{0.1}{(0.1M_A + 0.9M_B)/2000} = \frac{200}{0.1M_A + 0.9M_B}$$

Setting molarity = molality:
$$\frac{200}{0.1M_A + 0.9M_B} = \frac{1000}{9M_B}$$

$$200 \times 9M_B = 1000(0.1M_A + 0.9M_B)$$

$$1800M_B = 100M_A + 900M_B$$

$$900M_B = 100M_A$$

$$\frac{M_A}{M_B} = 9$$

**Answer:** 9"""

# ============================================================
# QUESTION 23: Diffusion coefficient
# ============================================================
solutions[("JEE Adv 2016 Paper 1", 33)] = r"""The diffusion coefficient $D \propto \lambda \bar{v}$, where $\lambda$ is the mean free path and $\bar{v}$ is the mean speed.

For an ideal gas:
- Mean free path: $\lambda = \frac{k_BT}{\sqrt{2}\pi d^2 P} \propto \frac{T}{P}$
- Mean speed: $\bar{v} = \sqrt{\frac{8k_BT}{\pi m}} \propto \sqrt{T}$

Therefore: $D \propto \lambda \bar{v} \propto \frac{T}{P} \cdot \sqrt{T} = \frac{T^{3/2}}{P}$

When $T \to 4T$ and $P \to 2P$:

$$\frac{D_2}{D_1} = \frac{(4T)^{3/2}/2P}{T^{3/2}/P} = \frac{4^{3/2}}{2} = \frac{8}{2} = 4$$

So $x = 4$.

**Answer:** 4"""

# ============================================================
# QUESTION 24: Permanganate oxidizing thiosulphate
# ============================================================
solutions[("JEE Adv 2016 Paper 1", 34)] = r"""In neutral or faintly alkaline solution, permanganate ($\text{MnO}_4^-$) is reduced to $\text{MnO}_2$ (Mn goes from +7 to +4, gaining 3 electrons).

Thiosulphate ($\text{S}_2\text{O}_3^{2-}$) is oxidized to sulphate ($\text{SO}_4^{2-}$) in alkaline/neutral medium. The average oxidation state of S in $\text{S}_2\text{O}_3^{2-}$ is +2, and in $\text{SO}_4^{2-}$ it is +6. Each S atom loses 4 electrons, so each $\text{S}_2\text{O}_3^{2-}$ loses 8 electrons.

Balancing electrons: 8 moles of $\text{MnO}_4^-$ gain $8 \times 3 = 24$ electrons.

Each $\text{S}_2\text{O}_3^{2-}$ loses 8 electrons, so moles of $\text{S}_2\text{O}_3^{2-}$ needed $= 24/8 = 3$.

Each $\text{S}_2\text{O}_3^{2-}$ produces 2 $\text{SO}_4^{2-}$, so total $\text{SO}_4^{2-}$ produced $= 3 \times 2 = 6$ moles.

$X = 6$.

**Answer:** 6"""

# ============================================================
# QUESTION 25: Quadratic roots, alpha1 + beta2
# ============================================================
solutions[("JEE Adv 2016 Paper 1", 37)] = r"""Given $-\frac{\pi}{6} < \theta < -\frac{\pi}{12}$, so $\theta$ is in the fourth quadrant (small negative angle).

**Equation 1:** $x^2 - 2x\sec\theta + 1 = 0$

Roots: $x = \frac{2\sec\theta \pm \sqrt{4\sec^2\theta - 4}}{2} = \sec\theta \pm |\tan\theta|$

Since $\theta$ is negative and in $(-\pi/6, -\pi/12)$: $\cos\theta > 0$, so $\sec\theta > 0$; $\tan\theta < 0$, so $|\tan\theta| = -\tan\theta$.

$\alpha_1 = \sec\theta + (-\tan\theta) = \sec\theta - \tan\theta$ (larger root since $-\tan\theta > 0$)

**Equation 2:** $x^2 + 2x\tan\theta - 1 = 0$

Roots: $x = \frac{-2\tan\theta \pm \sqrt{4\tan^2\theta + 4}}{2} = -\tan\theta \pm \sec\theta$

Since $\sec\theta > 0$, $-\tan\theta > 0$:
$\alpha_2 = -\tan\theta + \sec\theta$ and $\beta_2 = -\tan\theta - \sec\theta$

Wait, we need $\alpha_2 > \beta_2$, so $\alpha_2 = -\tan\theta + |\sec\theta|$. Since $\cos\theta > 0$, $\sec\theta > 0$, so:

$\alpha_2 = -\tan\theta + \sec\theta$, $\beta_2 = -\tan\theta - \sec\theta$

$$\alpha_1 + \beta_2 = (\sec\theta - \tan\theta) + (-\tan\theta - \sec\theta) = -2\tan\theta$$

**Answer:** C"""

# ============================================================
# QUESTION 26: Debate club team selection
# ============================================================
solutions[("JEE Adv 2016 Paper 1", 38)] = r"""The team has 4 members with at most 1 boy, so either 0 boys or 1 boy. A captain must be chosen from the team.

**Case 1: 0 boys (4 girls from 6)**
Ways to select 4 girls: $\binom{6}{4} = 15$
Ways to select captain from 4: $4$
Total: $15 \times 4 = 60$

**Case 2: 1 boy and 3 girls**
Ways to select 1 boy from 4: $\binom{4}{1} = 4$
Ways to select 3 girls from 6: $\binom{6}{3} = 20$
Ways to select captain from 4: $4$
Total: $4 \times 20 \times 4 = 320$

**Grand total:** $60 + 320 = 380$

**Answer:** A"""

# ============================================================
# QUESTION 27: Trigonometric equation sum of solutions
# ============================================================
solutions[("JEE Adv 2016 Paper 1", 39)] = r"""The equation is $\sqrt{3}\sec x + \csc x + 2(\tan x - \cot x) = 0$.

Multiply through by $\sin x \cos x$:
$$\sqrt{3}\sin x + \cos x + 2(\sin^2 x - \cos^2 x) = 0$$
$$\sqrt{3}\sin x + \cos x - 2\cos 2x = 0$$

Note $\sqrt{3}\sin x + \cos x = 2\sin\left(x + \frac{\pi}{6}\right)$.

Also, $\cos 2x = 1 - 2\sin^2 x$. Alternatively, use $\cos 2x = 2\cos^2 x - 1$.

So: $2\sin(x + \pi/6) - 2\cos 2x = 0$

$\sin(x + \pi/6) = \cos 2x = \sin(\pi/2 - 2x)$

**Case 1:** $x + \pi/6 = \pi/2 - 2x + 2k\pi \implies 3x = \pi/3 + 2k\pi \implies x = \pi/9 + 2k\pi/3$

In $(-\pi, \pi)$: $x = \pi/9, \pi/9 + 2\pi/3 = 7\pi/9, \pi/9 - 2\pi/3 = -5\pi/9$

**Case 2:** $x + \pi/6 = \pi - (\pi/2 - 2x) + 2k\pi \implies x + \pi/6 = \pi/2 + 2x + 2k\pi \implies -x = \pi/3 + 2k\pi \implies x = -\pi/3 - 2k\pi$

In $(-\pi, \pi)$: $x = -\pi/3$

Check validity (excluding $x = 0, \pm\pi/2$): All solutions $\pi/9, 7\pi/9, -5\pi/9, -\pi/3$ are valid.

Sum: $\pi/9 + 7\pi/9 - 5\pi/9 - \pi/3 = \pi/9 + 7\pi/9 - 5\pi/9 - 3\pi/9 = 0$

**Answer:** C"""

# ============================================================
# QUESTION 28: Probability - computer factory
# ============================================================
solutions[("JEE Adv 2016 Paper 1", 40)] = r"""Let $P(D|T_1) = p_1$ and $P(D|T_2) = p_2$. Given that $p_1 = 10p_2$.

Total defective probability: $P(D) = 0.2p_1 + 0.8p_2 = 0.07$

Substituting $p_1 = 10p_2$: $0.2(10p_2) + 0.8p_2 = 0.07$

$2p_2 + 0.8p_2 = 0.07 \implies 2.8p_2 = 0.07 \implies p_2 = 0.025$

So $p_1 = 0.25$.

We need $P(T_2 | D^c)$:

$$P(T_2|D^c) = \frac{P(D^c|T_2) \cdot P(T_2)}{P(D^c)} = \frac{(1-0.025)(0.8)}{1-0.07} = \frac{0.975 \times 0.8}{0.93} = \frac{0.78}{0.93} = \frac{78}{93}$$

**Answer:** C"""

# ============================================================
# QUESTION 29: Minimum alpha for inequality
# ============================================================
solutions[("JEE Adv 2016 Paper 1", 41)] = r"""We need the least $\alpha$ such that $4\alpha x^2 + \frac{1}{x} \geq 1$ for all $x > 0$.

Let $f(x) = 4\alpha x^2 + \frac{1}{x}$. We need $f(x) \geq 1$ for all $x > 0$.

Apply AM-GM inequality to $4\alpha x^2 + \frac{1}{x}$. Write $\frac{1}{x} = \frac{1}{2x} + \frac{1}{2x}$:

By AM-GM on three terms $4\alpha x^2, \frac{1}{2x}, \frac{1}{2x}$:

$$\frac{4\alpha x^2 + \frac{1}{2x} + \frac{1}{2x}}{3} \geq \left(4\alpha x^2 \cdot \frac{1}{2x} \cdot \frac{1}{2x}\right)^{1/3}$$

$$\frac{f(x)}{3} \geq \left(\frac{4\alpha}{4}\right)^{1/3} = \alpha^{1/3}$$

$$f(x) \geq 3\alpha^{1/3}$$

For equality to hold at the minimum, we need $4\alpha x^2 = \frac{1}{2x}$, i.e., $x^3 = \frac{1}{8\alpha}$.

Setting $3\alpha^{1/3} = 1$: $\alpha^{1/3} = \frac{1}{3}$, so $\alpha = \frac{1}{27}$.

**Answer:** C"""

# ============================================================
# QUESTION 30: Pyramid OPQRS
# ============================================================
solutions[("JEE Adv 2016 Paper 1", 42)] = r"""Set up coordinates: $O = (0,0,0)$, $P = (3,0,0)$, $Q = (3,3,0)$, $R = (0,3,0)$.

Midpoint of $OQ$: $T = (3/2, 3/2, 0)$. $S$ is directly above $T$ with $TS = 3$: $S = (3/2, 3/2, 3)$.

**(A)** $\vec{OQ} = (3,3,0)$, $\vec{OS} = (3/2, 3/2, 3)$.
$\cos\theta = \frac{\vec{OQ} \cdot \vec{OS}}{|\vec{OQ}||\vec{OS}|} = \frac{9/2 + 9/2}{3\sqrt{2} \cdot \sqrt{9/4+9/4+9}} = \frac{9}{3\sqrt{2} \cdot \sqrt{27/2}} = \frac{9}{3\sqrt{2} \cdot 3\sqrt{3}/\sqrt{2}} = \frac{9}{9\sqrt{3}/\sqrt{2} \cdot \sqrt{2}} = \frac{9}{9} $

Wait, let me recompute: $|\vec{OS}| = \sqrt{9/4 + 9/4 + 9} = \sqrt{9/2 + 9} = \sqrt{27/2} = \frac{3\sqrt{3}}{\sqrt{2}}$

$\cos\theta = \frac{9}{3\sqrt{2} \cdot \frac{3\sqrt{3}}{\sqrt{2}}} = \frac{9}{3\sqrt{2} \cdot \frac{3\sqrt{3}}{\sqrt{2}}} = \frac{9}{9\sqrt{3}} \cdot \frac{\sqrt{2}}{\sqrt{2}} $

Actually: $\cos\theta = \frac{9}{3\sqrt{2} \cdot \frac{3\sqrt{6}}{2}}$. Let me be more careful.

$|\vec{OS}| = \sqrt{(3/2)^2 + (3/2)^2 + 3^2} = \sqrt{9/4 + 9/4 + 9} = \sqrt{27/2} = 3\sqrt{3/2}$

$\cos\theta = \frac{9}{3\sqrt{2} \cdot 3\sqrt{3/2}} = \frac{9}{9\sqrt{2}\sqrt{3/2}} = \frac{1}{\sqrt{3}} $

So $\theta = \arccos(1/\sqrt{3}) \neq \pi/3$. **(A) FALSE.**

**(B)** Plane through $O$, $Q$, $S$: $\vec{OQ} = (3,3,0)$, $\vec{OS} = (3/2,3/2,3)$.
Normal: $\vec{OQ} \times \vec{OS} = \begin{vmatrix} \hat{i} & \hat{j} & \hat{k} \\ 3 & 3 & 0 \\ 3/2 & 3/2 & 3 \end{vmatrix} = (9-0)\hat{i} - (9-0)\hat{j} + (9/2-9/2)\hat{k} = 9\hat{i} - 9\hat{j}$

Normal direction: $(1,-1,0)$. Plane through origin: $x - y = 0$. **(B) TRUE.**

**(C)** Distance from $P = (3,0,0)$ to plane $x - y = 0$: $\frac{|3-0|}{\sqrt{2}} = \frac{3}{\sqrt{2}}$. **(C) TRUE.**

**(D)** Line $RS$: $R = (0,3,0)$, $S = (3/2,3/2,3)$. Direction: $(3/2,-3/2,3)$.
Distance from $O$ to line $RS$: $\frac{|\vec{OR} \times \vec{d}|}{|\vec{d}|}$ where $\vec{d} = (3/2,-3/2,3)$.

$\vec{OR} \times \vec{d} = (0,3,0) \times (3/2,-3/2,3) = (9-0)\hat{i} - (0-0)\hat{j} + (0-9/2)\hat{k} = (9, 0, -9/2)$

$|\vec{OR} \times \vec{d}| = \sqrt{81 + 0 + 81/4} = \sqrt{405/4} = \frac{9\sqrt{5}}{2}$

$|\vec{d}| = \sqrt{9/4 + 9/4 + 9} = \sqrt{27/2} = \frac{3\sqrt{6}}{2}$

Distance $= \frac{9\sqrt{5}/2}{3\sqrt{6}/2} = \frac{9\sqrt{5}}{3\sqrt{6}} = \frac{3\sqrt{5}}{\sqrt{6}} = 3\sqrt{5/6} = \sqrt{45/6} = \sqrt{15/2}$

**(D) TRUE.**

**Answer:** BCD"""

# ============================================================
# QUESTION 31: Differential equation f'(x) = 2 - f(x)/x
# ============================================================
solutions[("JEE Adv 2016 Paper 1", 43)] = r"""The ODE $f'(x) = 2 - \frac{f(x)}{x}$ can be rewritten as $f'(x) + \frac{f(x)}{x} = 2$, a first-order linear ODE.

Integrating factor: $\mu = e^{\int dx/x} = x$.

$$\frac{d}{dx}(xf(x)) = 2x$$

$$xf(x) = x^2 + C \implies f(x) = x + \frac{C}{x}$$

Since $f(1) \neq 1$, we have $C \neq 0$.

**(A)** $f'(x) = 1 - C/x^2$. $f'(1/x) = 1 - Cx^2$. $\lim_{x \to 0^+} f'(1/x) = 1 - 0 = 1$. **TRUE.**

**(B)** $xf(1/x) = x(1/x + Cx) = 1 + Cx^2$. $\lim_{x \to 0^+} xf(1/x) = 1 \neq 2$. **FALSE.**

**(C)** $x^2 f'(x) = x^2 - C$. $\lim_{x \to 0^+} x^2 f'(x) = -C \neq 0$ (since $C \neq 0$). **FALSE.**

**(D)** $f(x) = x + C/x$. For $C > 0$ and small $x > 0$, $f(x) \to +\infty$. For $C < 0$ and small $x$, $f(x) \to -\infty$. So $|f(x)|$ is unbounded on $(0,2)$. **FALSE.**

**Answer:** A"""

# ============================================================
# QUESTION 32: Matrix P, Q with PQ = kI
# ============================================================
solutions[("JEE Adv 2016 Paper 1", 44)] = r"""Since $PQ = kI$, we have $Q = kP^{-1}$, so $\det(Q) = k^3/\det(P)$.

Also, $Q = \frac{k}{\det(P)} \text{adj}(P)$, so $q_{ij} = \frac{k}{\det(P)} C_{ij}$ where $C_{ij}$ is the cofactor of $P_{ji}$ (cofactor of $P^T$... actually the adjugate).

$q_{23} = \frac{k}{\det(P)} \cdot$ cofactor of $P_{32}$ in $P^T$, which equals the cofactor of element $(3,2)$ in $P$.

The $(3,2)$ cofactor of $P$ is $(-1)^{3+2} \begin{vmatrix} 3 & -2 \\ 2 & \alpha \end{vmatrix} = -(3\alpha + 4)$.

So $q_{23} = \frac{k}{\det(P)} \cdot (-(3\alpha+4))$.

Given $q_{23} = -k/8$:
$$\frac{-(3\alpha+4)}{\det(P)} = -\frac{1}{8} \implies \det(P) = 8(3\alpha+4)$$

Computing $\det(P)$: expanding along first row:
$$\det(P) = 3(0+5\alpha) + 1(0-3\alpha) + (-2)(-10-0) = 15\alpha - 3\alpha + 20 = 12\alpha + 20$$

So $12\alpha + 20 = 24\alpha + 32 \implies -12\alpha = 12 \implies \alpha = -1$.

$\det(P) = 12(-1) + 20 = 8$, and $k = \det(P)/(3\alpha+4)$... wait, let me use $\det(Q) = k^3/\det(P) = k^3/8$.

Given $\det(Q) = k^2/2$: $k^3/8 = k^2/2 \implies k = 4$.

Check **(A)**: $\alpha = -1 \neq 0$ and $k = 4 \neq 8$. FALSE.

Check **(B)**: $4(-1) - 4 + 8 = -4 - 4 + 8 = 0$. **TRUE.**

Check **(C)**: $\det(P \cdot \text{adj}(Q)) = \det(P) \cdot \det(\text{adj}(Q)) = \det(P) \cdot [\det(Q)]^2 = 8 \cdot (k^2/2)^2 = 8 \cdot (16/2)^2 = 8 \cdot 64 = 512 = 2^9$. **TRUE.**

Check **(D)**: $\det(Q \cdot \text{adj}(P)) = \det(Q) \cdot [\det(P)]^2 = (k^2/2) \cdot 64 = 8 \cdot 64 = 512 = 2^9 \neq 2^{13}$. **FALSE.**

**Answer:** BC"""

# ============================================================
# QUESTION 33: Triangle XYZ, incircle
# ============================================================
solutions[("JEE Adv 2016 Paper 1", 45)] = r"""Given $\frac{s-x}{4} = \frac{s-y}{3} = \frac{s-z}{2} = k$ (say).

So $s-x = 4k$, $s-y = 3k$, $s-z = 2k$.

Adding: $3s - (x+y+z) = 9k \implies 3s - 2s = 9k \implies s = 9k$.

Therefore: $x = s - 4k = 5k$, $y = s - 3k = 6k$, $z = s - 2k = 7k$.

Area of incircle $= \pi r^2 = \frac{8\pi}{3}$, so $r^2 = 8/3$, $r = \sqrt{8/3} = 2\sqrt{2/3}$.

By Heron's formula: $\Delta = \sqrt{s(s-x)(s-y)(s-z)} = \sqrt{9k \cdot 4k \cdot 3k \cdot 2k} = \sqrt{216k^4} = 6k^2\sqrt{6}$

Also $\Delta = rs$: $6k^2\sqrt{6} = 2\sqrt{2/3} \cdot 9k \implies k = \frac{18\sqrt{2/3}}{6\sqrt{6}} = \frac{3\sqrt{2/3}}{\sqrt{6}} = \frac{3\sqrt{2}}{\sqrt{3}\sqrt{6}} = \frac{3\sqrt{2}}{3\sqrt{2}} = 1$

So $k = 1$, $s = 9$, $x = 5$, $y = 6$, $z = 7$.

**(A)** $\Delta = 6\sqrt{6}$. **TRUE.**

**(B)** Circumradius: $R = \frac{xyz}{4\Delta} = \frac{5 \cdot 6 \cdot 7}{4 \cdot 6\sqrt{6}} = \frac{210}{24\sqrt{6}} = \frac{35}{4\sqrt{6}} = \frac{35\sqrt{6}}{24}$. The given value is $\frac{35}{6}\sqrt{6} = \frac{35\sqrt{6}}{6}$, which doesn't match. **FALSE.**

**(C)** $\sin\frac{X}{2}\sin\frac{Y}{2}\sin\frac{Z}{2} = \frac{r}{4R} = \frac{2\sqrt{2/3}}{4 \cdot \frac{35\sqrt{6}}{24}} = \frac{2\sqrt{2/3} \cdot 24}{4 \cdot 35\sqrt{6}} = \frac{48\sqrt{2/3}}{140\sqrt{6}}$

$= \frac{48}{140} \cdot \frac{\sqrt{2}}{\sqrt{3}\sqrt{6}} = \frac{48}{140} \cdot \frac{\sqrt{2}}{3\sqrt{2}} = \frac{48}{420} = \frac{4}{35}$. **TRUE.**

**(D)** $\frac{X+Y}{2} = \frac{\pi - Z}{2}$, so $\sin^2\frac{X+Y}{2} = \cos^2\frac{Z}{2}$.

$\cos^2\frac{Z}{2} = \frac{s(s-z)}{\text{...}}$. Using the formula: $\cos\frac{Z}{2} = \sqrt{\frac{s(s-z)}{xy}} = \sqrt{\frac{9 \cdot 2}{30}} = \sqrt{\frac{18}{30}} = \sqrt{\frac{3}{5}}$.

So $\sin^2\frac{X+Y}{2} = \frac{3}{5}$. **TRUE.**

**Answer:** ACD"""

# ============================================================
# QUESTION 34: Differential equation solution curve
# ============================================================
solutions[("JEE Adv 2016 Paper 1", 46)] = r"""The DE: $(x^2 + xy + 4x + 2y + 4)\frac{dy}{dx} - y^2 = 0$

Factor the expression: $x^2 + xy + 4x + 2y + 4 = x^2 + 4x + 4 + xy + 2y = (x+2)^2 + y(x+2) = (x+2)(x+2+y)$

So: $(x+2)(x+y+2)\frac{dy}{dx} = y^2$

Let $v = \frac{y}{x+2}$, so $y = v(x+2)$ and $\frac{dy}{dx} = v + (x+2)v'$.

$(x+2)^2(1+v)\left(v + (x+2)v'\right) = v^2(x+2)^2$

$(1+v)(v + (x+2)v') = v^2$

$v(1+v) + (x+2)(1+v)v' = v^2$

$v + v^2 + (x+2)(1+v)v' = v^2$

$(x+2)(1+v)v' = -v$

$\frac{(1+v)}{v}dv = \frac{-dx}{x+2}$

$\left(\frac{1}{v} + 1\right)dv = \frac{-dx}{x+2}$

$\ln|v| + v = -\ln|x+2| + C$

$\ln|v(x+2)| + v = C$

$\ln|y| + \frac{y}{x+2} = C$

Using $(1,3)$: $\ln 3 + 1 = C$.

So: $\ln y + \frac{y}{x+2} = 1 + \ln 3$

**(A)** At $y = x+2$: $\ln(x+2) + 1 = 1 + \ln 3 \implies \ln(x+2) = \ln 3 \implies x = 1$, giving $y = 3$. Exactly one intersection. **TRUE.**

**(B)** From above, exactly one point. **FALSE.**

**(C)** At $y = (x+2)^2$: $\ln(x+2)^2 + (x+2) = 1 + \ln 3$. For $x = 0$: $\ln 4 + 2 = 2\ln 2 + 2 \approx 3.386$ vs $1 + \ln 3 \approx 2.099$. For small $x > 0$, LHS grows, while RHS is fixed. At $x = -1$: $\ln 1 + 1 = 1$ vs $2.099$. Need to check if there's a solution. LHS at $x = -1$ is 1, at $x = 0$ is 3.386. The target is 2.099, so there exists a solution in $(-1, 0)$... but $x > 0$ is required. For $x > 0$, LHS $> 3.386 > 2.099$. Actually we need to check more carefully. Let $g(x) = 2\ln(x+2) + (x+2) - 1 - \ln 3$. At $x \to 0^+$: $g(0) = 2\ln 2 + 2 - 1 - \ln 3 = 1.386 + 1 - 1.099 = 1.287 > 0$. Since $g'(x) = \frac{2}{x+2} + 1 > 0$, $g$ is increasing for $x > 0$, so no solution for $x > 0$. **FALSE** — does not intersect.

**(D)** At $y = (x+3)^2$: $\ln(x+3)^2 + \frac{(x+3)^2}{x+2} = 1 + \ln 3$. At $x = 0$: $2\ln 3 + 9/2 = 2.197 + 4.5 = 6.697 \gg 2.099$. At very small positive $x$, LHS is large. Since LHS is increasing, there's no intersection. **TRUE.**

**Answer:** AD"""

# ============================================================
# QUESTION 35: f, g, h functions
# ============================================================
solutions[("JEE Adv 2016 Paper 1", 47)] = r"""Given $f(x) = x^3 + 3x + 2$, $g(f(x)) = x$, $h(g(g(x))) = x$.

So $g = f^{-1}$ and $h = (g \circ g)^{-1} = f \circ f$ (since if $h(g(g(x))) = x$, then $h = (g \circ g)^{-1} = f \circ f$).

$f'(x) = 3x^2 + 3$.

**(A)** $g'(2) = \frac{1}{f'(g(2))}$. We need $g(2) = f^{-1}(2)$: $f(0) = 2$, so $g(2) = 0$.

$g'(2) = \frac{1}{f'(0)} = \frac{1}{3}$. The answer says $1/15$. **FALSE.**

**(B)** $h(x) = f(f(x))$. $h'(x) = f'(f(x)) \cdot f'(x)$.

$h'(1) = f'(f(1)) \cdot f'(1) = f'(6) \cdot 6 = (3 \cdot 36 + 3) \cdot 6 = 111 \times 6 = 666$. **TRUE.**

**(C)** $h(0) = f(f(0)) = f(2) = 8 + 6 + 2 = 16$. **TRUE.**

**(D)** $h(g(3)) = f(f(g(3))) = f(3) = 27 + 9 + 2 = 38 \neq 36$. **FALSE.**

**Answer:** BC"""

# ============================================================
# QUESTION 36: Circles and parabola
# ============================================================
solutions[("JEE Adv 2016 Paper 1", 48)] = r"""Circle $C_1: x^2 + y^2 = 3$. Parabola: $x^2 = 2y$.

Intersection: $2y + y^2 = 3 \implies y^2 + 2y - 3 = 0 \implies (y+3)(y-1) = 0$. So $y = 1$ (first quadrant), $x = \sqrt{2}$.

Point $P = (\sqrt{2}, 1)$.

Tangent to $C_1$ at $P$: $\sqrt{2}x + y = 3$.

$C_2$ and $C_3$ have centers $Q_2, Q_3$ on the $y$-axis with radius $r = 2\sqrt{3}$.

Let $Q_2 = (0, a)$. Distance from $Q_2$ to tangent line $\sqrt{2}x + y - 3 = 0$ equals $r$:
$$\frac{|a - 3|}{\sqrt{3}} = 2\sqrt{3} \implies |a - 3| = 6$$

$a = 9$ or $a = -3$. So $Q_2 = (0, 9)$, $Q_3 = (0, -3)$.

**(A)** $Q_2Q_3 = |9 - (-3)| = 12$. **TRUE.**

**(B)** $R_2$ and $R_3$ are points of tangency on the tangent line.

$R_2$: Foot of perpendicular from $Q_2 = (0,9)$ to line $\sqrt{2}x + y = 3$.

$R_2 = Q_2 - \frac{(\sqrt{2}(0) + 9 - 3)}{3}(\sqrt{2}, 1) = (0,9) - 2(\sqrt{2}, 1) = (-2\sqrt{2}, 7)$

$R_3$: Foot of perpendicular from $Q_3 = (0,-3)$ to line.

$R_3 = (0,-3) - \frac{(-3-3)}{3}(\sqrt{2}, 1) = (0,-3) + 2(\sqrt{2}, 1) = (2\sqrt{2}, -1)$

$R_2R_3 = \sqrt{(4\sqrt{2})^2 + 8^2} = \sqrt{32 + 64} = \sqrt{96} = 4\sqrt{6}$. **TRUE.**

**(C)** Area of $\triangle OR_2R_3$: $O = (0,0)$, $R_2 = (-2\sqrt{2}, 7)$, $R_3 = (2\sqrt{2}, -1)$.

Area $= \frac{1}{2}|x_{R_2}y_{R_3} - x_{R_3}y_{R_2}| = \frac{1}{2}|(-2\sqrt{2})(-1) - (2\sqrt{2})(7)| = \frac{1}{2}|2\sqrt{2} - 14\sqrt{2}| = \frac{1}{2} \cdot 12\sqrt{2} = 6\sqrt{2}$. **TRUE.**

**(D)** Area of $\triangle PQ_2Q_3$: $P = (\sqrt{2}, 1)$, $Q_2 = (0, 9)$, $Q_3 = (0, -3)$.

Area $= \frac{1}{2} \cdot |Q_2Q_3| \cdot |\text{horizontal distance of } P| = \frac{1}{2} \cdot 12 \cdot \sqrt{2} = 6\sqrt{2}$.

The given value is $4\sqrt{2}$. **FALSE.**

**Answer:** ABC"""

# ============================================================
# QUESTION 37: Locus of point E on circle
# ============================================================
solutions[("JEE Adv 2016 Paper 1", 49)] = r"""Circle $x^2 + y^2 = 1$, $S = (1,0)$, $R = (-1,0)$. Let $P = (\cos\theta, \sin\theta)$.

Tangent at $S$: $x = 1$.

Tangent at $P$: $x\cos\theta + y\sin\theta = 1$.

Point $Q$ is intersection of these tangents. From $x = 1$: $\cos\theta + y\sin\theta = 1 \implies y = \frac{1-\cos\theta}{\sin\theta} = \tan(\theta/2)$.

So $Q = (1, \tan(\theta/2))$.

Normal at $P$: passes through origin and $P$, so the line is $y = x\tan\theta$.

Line through $Q$ parallel to $RS$ (which is the $x$-axis): $y = \tan(\theta/2)$.

Point $E$: intersection of normal $y = x\tan\theta$ and line $y = \tan(\theta/2)$.

$\tan(\theta/2) = x\tan\theta \implies x = \frac{\tan(\theta/2)}{\tan\theta} = \frac{\tan(\theta/2)}{\frac{2\tan(\theta/2)}{1-\tan^2(\theta/2)}} = \frac{1-\tan^2(\theta/2)}{2}$

Let $t = \tan(\theta/2)$: $x = \frac{1-t^2}{2}$, $y = t$.

So $t^2 = 1 - 2x$, i.e., $y^2 = 1 - 2x$, or $x = \frac{1-y^2}{2}$.

Check **(A)**: $(1/3, 1/\sqrt{3})$: $x = \frac{1-1/3}{2} = 1/3$. YES. **TRUE.**

Check **(B)**: $(1/4, 1/2)$: $x = \frac{1-1/4}{2} = 3/8 \neq 1/4$. **FALSE.**

Check **(C)**: $(1/3, -1/\sqrt{3})$: $x = \frac{1-1/3}{2} = 1/3$. YES. **TRUE.**

Check **(D)**: $(1/4, -1/2)$: $x = 3/8 \neq 1/4$. **FALSE.**

**Answer:** AC"""

# ============================================================
# QUESTION 38: Determinant = 10
# ============================================================
solutions[("JEE Adv 2016 Paper 1", 50)] = r"""$$\begin{vmatrix} x & x^2 & 1+x^3 \\ 2x & 4x^2 & 1+8x^3 \\ 3x & 9x^2 & 1+27x^3 \end{vmatrix} = 10$$

Factor $x$ from column 1 and $x^2$ from column 2 (if $x \neq 0$):

$$x \cdot x^2 \begin{vmatrix} 1 & 1 & 1+x^3 \\ 2 & 4 & 1+8x^3 \\ 3 & 9 & 1+27x^3 \end{vmatrix} = 10$$

Split column 3: the determinant becomes $D_1 + D_2$ where:

$$x^3 \begin{vmatrix} 1 & 1 & 1 \\ 2 & 4 & 1 \\ 3 & 9 & 1 \end{vmatrix} + x^3 \begin{vmatrix} 1 & 1 & x^3 \\ 2 & 4 & 8x^3 \\ 3 & 9 & 27x^3 \end{vmatrix}$$

For the first determinant: $R_2 \to R_2 - 2R_1$, $R_3 \to R_3 - 3R_1$:
$$\begin{vmatrix} 1 & 1 & 1 \\ 0 & 2 & -1 \\ 0 & 6 & -2 \end{vmatrix} = 1(-4+6) = 2$$

For the second determinant, factor $x^3$ from column 3:
$$x^6 \begin{vmatrix} 1 & 1 & 1 \\ 2 & 4 & 8 \\ 3 & 9 & 27 \end{vmatrix}$$

This is a Vandermonde-like determinant with rows $(1, 1, 1), (2, 4, 8), (3, 9, 27)$ = rows of $(a^0, a^1, a^2)$... actually it's $(a, a^2, a^3)$ for $a = 1, 2, 3$.

$$= \begin{vmatrix} 1 & 1 & 1 \\ 2 & 4 & 8 \\ 3 & 9 & 27 \end{vmatrix} = 1(108-72) - 1(54-24) + 1(18-12) = 36 - 30 + 6 = 12$$

So the equation becomes: $x^3 \cdot 2 + x^3 \cdot x^6 \cdot 12 = 10$

Wait, let me redo. The full expression is: $x^3(2 + 12x^6) = 10$, but we also need to account for $x = 0$ case.

Actually: $2x^3 + 12x^9 = 10 \implies 6x^9 + x^3 - 5 = 0$.

Let $u = x^3$: $6u^3 + u - 5 = 0$.

Testing $u = \frac{5}{6}$: no. $u = 1$: $6 + 1 - 5 = 2 \neq 0$. Hmm, let me recheck.

$2x^3 + 12x^9 = 10 \implies 12x^9 + 2x^3 - 10 = 0 \implies 6x^9 + x^3 - 5 = 0$.

Let $t = x^3$: $6t^3 + t - 5 = 0$. $t = \frac{5}{6}$: $6 \cdot 125/216 + 5/6 - 5 = 125/36 + 5/6 - 5 = 125/36 + 30/36 - 180/36 = -25/36 \neq 0$.

$t = 1$: $6 + 1 - 5 = 2 \neq 0$. Hmm. Let me recompute the determinant more carefully.

Actually I may have an error with the factoring. Let me redo from scratch.

Let the determinant be $D$. $R_2 \to R_2 - 2R_1$, $R_3 \to R_3 - 3R_1$:

$$D = \begin{vmatrix} x & x^2 & 1+x^3 \\ 0 & 2x^2 & -1+6x^3 \\ 0 & 6x^2 & -2+24x^3 \end{vmatrix} = x \cdot (2x^2(-2+24x^3) - 6x^2(-1+6x^3))$$

Hmm wait, expanding along column 1:

$= x[(2x^2)(-2+24x^3) - (6x^2)(-1+6x^3)]$
$= x[(-4x^2 + 48x^5) - (-6x^2 + 36x^5)]$
$= x[-4x^2 + 48x^5 + 6x^2 - 36x^5]$
$= x[2x^2 + 12x^5]$
$= 2x^3 + 12x^6$

So $2x^3 + 12x^6 = 10 \implies 6x^6 + x^3 - 5 = 0$.

Let $t = x^3$: $6t^2 + t - 5 = 0 \implies t = \frac{-1 \pm \sqrt{1+120}}{12} = \frac{-1 \pm 11}{12}$.

$t = \frac{10}{12} = \frac{5}{6}$ or $t = -1$.

$x^3 = 5/6 \implies x = (5/6)^{1/3}$ (one real solution).
$x^3 = -1 \implies x = -1$ (one real solution).

Total: **2** distinct real values.

**Answer:** 2"""

# ============================================================
# QUESTION 39: Coefficient of x^2, smallest m
# ============================================================
solutions[("JEE Adv 2016 Paper 1", 51)] = r"""The coefficient of $x^2$ in $(1+x)^k$ is $\binom{k}{2}$.

Sum of coefficients of $x^2$ from $(1+x)^2 + (1+x)^3 + \cdots + (1+x)^{49}$:
$$\sum_{k=2}^{49} \binom{k}{2} = \binom{3}{3} + \binom{4}{3} + \cdots + \binom{49}{3}$$

Wait, using the hockey stick identity: $\sum_{k=2}^{49} \binom{k}{2} = \binom{50}{3}$ (by hockey stick: $\sum_{k=r}^{n} \binom{k}{r} = \binom{n+1}{r+1}$).

So $\sum_{k=2}^{49} \binom{k}{2} = \binom{50}{3}$.

The coefficient of $x^2$ in $(1+mx)^{50}$ is $\binom{50}{2}m^2$.

Total coefficient of $x^2$: $\binom{50}{3} + \binom{50}{2}m^2$.

This equals $(3n+1)\binom{51}{3}$:

$$\binom{50}{3} + \binom{50}{2}m^2 = (3n+1)\binom{51}{3}$$

$\binom{50}{3} = \frac{50 \cdot 49 \cdot 48}{6} = 19600$

$\binom{50}{2} = \frac{50 \cdot 49}{2} = 1225$

$\binom{51}{3} = \frac{51 \cdot 50 \cdot 49}{6} = 20825$

$$19600 + 1225m^2 = (3n+1) \times 20825$$

$$1225m^2 = 20825(3n+1) - 19600$$

Note: $20825 = 17 \times 1225$ and $19600 = 16 \times 1225$.

$$1225m^2 = 1225 \times 17(3n+1) - 1225 \times 16$$

$$m^2 = 17(3n+1) - 16 = 51n + 17 - 16 = 51n + 1$$

For smallest positive integer $m$: try $n$ values.
- $n = 1$: $m^2 = 52$. Not a perfect square.
- $n = 2$: $m^2 = 103$. Not a perfect square.
- $n = 3$: $m^2 = 154$. Not.
- $n = 4$: $m^2 = 205$. Not.
- $n = 5$: $m^2 = 256 = 16^2$. Yes! $m = 16$.

So $n = 5$.

**Answer:** 5"""

# ============================================================
# QUESTION 40: Integral equation
# ============================================================
solutions[("JEE Adv 2016 Paper 1", 52)] = r"""We need the number of solutions to $\int_0^x \frac{t^2}{1+t^4}dt = 2x - 1$ in $[0,1]$.

Let $f(x) = \int_0^x \frac{t^2}{1+t^4}dt$ and $g(x) = 2x - 1$.

At $x = 0$: $f(0) = 0$, $g(0) = -1$. So $f(0) > g(0)$.

At $x = 1$: $f(1) = \int_0^1 \frac{t^2}{1+t^4}dt$. Since $\frac{t^2}{1+t^4} \leq \frac{t^2}{1} = t^2$ for $t \in [0,1]$, we get $f(1) \leq 1/3$. Also $g(1) = 1$.

So $f(1) < g(1)$.

Since $f$ is continuous and starts above $g$ at $x=0$ and ends below $g$ at $x=1$, by IVT there is at least one crossing.

$f'(x) = \frac{x^2}{1+x^4}$ and $g'(x) = 2$.

For $x \in [0,1]$: $f'(x) = \frac{x^2}{1+x^4} \leq \frac{1}{2}$ (maximum at $x=1$ gives $1/2$). So $f'(x) \leq 1/2 < 2 = g'(x)$.

Since $g'(x) > f'(x)$ for all $x \in [0,1]$, the function $h(x) = f(x) - g(x)$ has $h'(x) = f'(x) - 2 < 0$, so $h$ is strictly decreasing. Therefore there is exactly **1** solution.

**Answer:** 1"""

# ============================================================
# QUESTION 41: Limit, find 6(alpha+beta)
# ============================================================
solutions[("JEE Adv 2016 Paper 1", 53)] = r"""We need $\lim_{x \to 0} \frac{x^2 \sin(\beta x)}{\alpha x - \sin x} = 1$.

Using Taylor expansions: $\sin(\beta x) = \beta x - \frac{(\beta x)^3}{6} + \cdots$ and $\sin x = x - \frac{x^3}{6} + \cdots$

Numerator: $x^2(\beta x - \frac{\beta^3 x^3}{6} + \cdots) = \beta x^3 - \frac{\beta^3 x^5}{6} + \cdots$

Denominator: $\alpha x - x + \frac{x^3}{6} - \cdots = (\alpha - 1)x + \frac{x^3}{6} + \cdots$

For the limit to be finite and equal to 1, the leading powers must match.

If $\alpha \neq 1$: denominator $\sim (\alpha-1)x$, numerator $\sim \beta x^3$. Ratio $\sim \frac{\beta x^2}{\alpha-1} \to 0 \neq 1$.

So we need $\alpha = 1$. Then denominator $= \frac{x^3}{6} - \frac{x^5}{120} + \cdots$

$$\lim_{x \to 0} \frac{\beta x^3}{x^3/6} = 6\beta = 1 \implies \beta = \frac{1}{6}$$

$$6(\alpha + \beta) = 6\left(1 + \frac{1}{6}\right) = 6 \cdot \frac{7}{6} = 7$$

**Answer:** 7"""

# ============================================================
# QUESTION 42: Matrix P^2 = -I
# ============================================================
solutions[("JEE Adv 2016 Paper 1", 54)] = r"""$z = \frac{-1+\sqrt{3}i}{2} = e^{i2\pi/3} = \omega$ (a primitive cube root of unity).

$P = \begin{pmatrix} (-z)^r & z^{2s} \\ z^{2s} & z^r \end{pmatrix}$

$(-z)^r = (-1)^r z^r = (-1)^r \omega^r$

Note: $\omega^3 = 1$, so $\omega^r$ depends on $r \mod 3$.

$P^2 = -I$ requires $P^2 + I = 0$.

$P^2 = \begin{pmatrix} (-z)^{2r} + z^{4s} & (-z)^r z^{2s} + z^{2s}z^r \\ z^{2s}(-z)^r + z^r z^{2s} & z^{4s} + z^{2r} \end{pmatrix}$

Off-diagonal: $z^{2s}[(-z)^r + z^r] = z^{2s} z^r[(-1)^r + 1]$

For off-diagonal to be 0: either $(-1)^r + 1 = 0$ (i.e., $r$ is odd) or $z^{2s}z^r = 0$ (impossible since $|z| = 1$).

So $r$ must be odd: $r = 1$ or $r = 3$.

Diagonal entries of $P^2$:
$(1,1)$: $(-z)^{2r} + z^{4s} = z^{2r} + z^{4s}$ (since $(-1)^{2r} = 1$)
$(2,2)$: $z^{4s} + z^{2r}$

Both diagonal entries equal $z^{2r} + z^{4s}$, and must equal $-1$.

$\omega^{2r} + \omega^{4s} = -1$

For $r = 1$: $\omega^2 + \omega^{4s} = -1$. Since $1 + \omega + \omega^2 = 0$, we have $\omega + \omega^2 = -1$.

$\omega^{4s}$: for $s = 1$: $\omega^4 = \omega$. So $\omega^2 + \omega = -1$. YES.
$s = 2$: $\omega^8 = \omega^2$. So $\omega^2 + \omega^2 = 2\omega^2 \neq -1$.
$s = 3$: $\omega^{12} = 1$. So $\omega^2 + 1 \neq -1$ (since $\omega^2 + 1 = -\omega$).

For $r = 3$: $\omega^6 + \omega^{4s} = 1 + \omega^{4s} = -1 \implies \omega^{4s} = -2$. But $|\omega^{4s}| = 1 \neq 2$. Impossible.

So only $(r, s) = (1, 1)$ works. Total: **1** ordered pair.

**Answer:** 1"""

# ============================================================
# QUESTION 43: Nuclear radius from binding energies
# ============================================================
solutions[("JEE Adv 2016 Paper 2", 1)] = r"""The difference in binding energies of ${}^{15}_7\text{N}$ and ${}^{15}_8\text{O}$ is due to the electrostatic energy difference.

Binding energy of ${}^{15}_7\text{N}$: $BE_N = [7(1.007825) + 8(1.008665) - 15.000109] \times 931.5\,\text{MeV}$
$= [7.054775 + 8.069320 - 15.000109] \times 931.5 = 0.123986 \times 931.5 = 115.493\,\text{MeV}$

Binding energy of ${}^{15}_8\text{O}$: $BE_O = [8(1.007825) + 7(1.008665) - 15.003065] \times 931.5$
$= [8.062600 + 7.060655 - 15.003065] \times 931.5 = 0.120190 \times 931.5 = 111.957\,\text{MeV}$

Difference: $BE_N - BE_O = 115.493 - 111.957 = 3.536\,\text{MeV}$

Electrostatic energy difference:
$$\Delta E = \frac{3}{5}\frac{e^2}{4\pi\varepsilon_0 R}[Z_O(Z_O-1) - Z_N(Z_N-1)]$$

$= \frac{3}{5} \cdot \frac{1.44}{R} \cdot [8 \times 7 - 7 \times 6] = \frac{3}{5} \cdot \frac{1.44}{R} \cdot [56 - 42] = \frac{3}{5} \cdot \frac{1.44 \times 14}{R}$

Setting equal to $3.536\,\text{MeV}$:

$$R = \frac{3 \times 1.44 \times 14}{5 \times 3.536} = \frac{60.48}{17.68} = 3.42\,\text{fm}$$

**Answer:** C"""

# ============================================================
# QUESTION 44: Radioactive decay - safe lab
# ============================================================
solutions[("JEE Adv 2016 Paper 2", 2)] = r"""The radiation level needs to decrease by a factor of 64 to reach the permissible level.

$64 = 2^6$, so the material needs to undergo 6 half-lives.

Time = $6 \times 18 = 108$ days.

**Answer:** C"""

# ============================================================
# QUESTION 45: Adiabatic and two-step process
# ============================================================
solutions[("JEE Adv 2016 Paper 2", 3)] = r"""**Adiabatic process:** $P^3V^5 = \text{const}$, so $PV^{5/3} = \text{const}$, meaning $\gamma = 5/3$ (monatomic gas).

For monatomic gas: $C_v = \frac{3}{2}R$, $C_p = \frac{5}{2}R$.

**Two-step process:**

**Step 1: Isobaric expansion** from $(P_i, V_i)$ to $(P_i, V_f)$:
$W_1 = P_i(V_f - V_i) = 10^5(8 \times 10^{-3} - 10^{-3}) = 10^5 \times 7 \times 10^{-3} = 700\,\text{J}$

**Step 2: Isochoric process** from $(P_i, V_f)$ to $(P_f, V_f)$:
$W_2 = 0$

For the adiabatic process ($Q = 0$): $\Delta U = -W_{\text{adiabatic}}$. But since initial and final states are the same in both processes, $\Delta U$ is the same.

$\Delta U$ from state $(P_i, V_i)$ to $(P_f, V_f)$:

Using ideal gas: $\Delta U = nC_v \Delta T = \frac{C_v}{R}(P_fV_f - P_iV_i) = \frac{3/2}{1}(P_fV_f - P_iV_i)$

$P_iV_i = 10^5 \times 10^{-3} = 100\,\text{J}$
$P_fV_f = \frac{10^5}{32} \times 8 \times 10^{-3} = \frac{800}{32} = 25\,\text{J}$

$\Delta U = \frac{3}{2}(25 - 100) = \frac{3}{2}(-75) = -112.5\,\text{J}$

**Heat in two-step process:**
$Q = \Delta U + W = -112.5 + 700 = 587.5 \approx 588\,\text{J}$

**Answer:** C"""

# ============================================================
# QUESTION 46: Thermal expansion of wire PQ
# ============================================================
solutions[("JEE Adv 2016 Paper 2", 4)] = r"""Two wires in series: PQ (thermal conductivity $2K$, length 1 m) and RS (thermal conductivity $K$, length 1 m).

End P at $10°\text{C}$, end S at $400°\text{C}$.

In steady state, heat flow rate is the same through both wires. Let $T_j$ be the junction temperature.

$$\frac{2K \cdot A(T_j - 10)}{1} = \frac{K \cdot A(400 - T_j)}{1}$$

$$2(T_j - 10) = 400 - T_j \implies 2T_j - 20 = 400 - T_j \implies 3T_j = 420 \implies T_j = 140°\text{C}$$

The average temperature of wire PQ is $\frac{10 + 140}{2} = 75°\text{C}$.

The temperature rise of PQ from its initial temperature ($10°\text{C}$): $\Delta T = 75 - 10 = 65°\text{C}$.

Change in length of PQ:
$$\Delta l = l \cdot \alpha \cdot \Delta T = 1 \times 1.2 \times 10^{-5} \times 65 = 78 \times 10^{-5}\,\text{m} = 0.78\,\text{mm}$$

**Answer:** A"""

# ============================================================
# QUESTION 47: Error analysis, g measurement
# ============================================================
solutions[("JEE Adv 2016 Paper 2", 9)] = r"""$T = 2\pi\sqrt{\frac{7(R-r)}{5g}}$

Measurements: $R = 60 \pm 1\,\text{mm}$, $r = 10 \pm 1\,\text{mm}$.

**(A)** Error in $r$: $\frac{\Delta r}{r} = \frac{1}{10} = 10\%$. **TRUE.**

**Time period:** Mean $T = \frac{0.52 + 0.56 + 0.57 + 0.54 + 0.59}{5} = \frac{2.78}{5} = 0.556\,\text{s}$

Mean absolute deviation: $|0.52-0.556| + |0.56-0.556| + |0.57-0.556| + |0.54-0.556| + |0.59-0.556|$
$= 0.036 + 0.004 + 0.014 + 0.016 + 0.034 = 0.104$

$\Delta T = \frac{0.104}{5} = 0.0208\,\text{s}$

But we should round: $\Delta T \approx 0.02\,\text{s}$.

$\frac{\Delta T}{T} = \frac{0.02}{0.556} = 0.036 = 3.6\%$

Rounding appropriately: $\approx 3.57\%$. **(B) TRUE.**

**(C)** 2% would correspond to $\Delta T = 0.01\,\text{s}$, which is just the least count, not the actual error. **FALSE.**

**(D)** From $T^2 = \frac{4\pi^2 \times 7(R-r)}{5g}$: $g = \frac{4\pi^2 \times 7(R-r)}{5T^2}$

$$\frac{\Delta g}{g} = \frac{\Delta(R-r)}{R-r} + 2\frac{\Delta T}{T} = \frac{2}{50} + 2 \times 0.0357 = 0.04 + 0.0714 = 0.1114 \approx 11\%$$

**(D) TRUE.**

**Answer:** ABD"""

# ============================================================
# QUESTION 48: Galvanometers and resistors
# ============================================================
solutions[("JEE Adv 2016 Paper 2", 10)] = r"""Two identical galvanometers (internal resistance $R_C$, full-scale deflection current $I_g$) and two identical resistors with resistance $R$. Given $R_C < R/2$.

**Maximum voltage range:** We want to maximize total resistance in series with the galvanometer being used as a voltmeter.

If we connect one galvanometer in series with both resistors, total resistance = $R_C + 2R$. The other galvanometer connected in parallel to the first: equivalent galvanometer resistance = $R_C/2$, but this doubles the current needed.

Actually, for maximum voltage range with one galvanometer: $V = I_g \times (R_C + R_{\text{series}})$. To maximize, put maximum resistance in series.

**(B)**: Two resistors + one galvanometer in series, second galvanometer in parallel with first. This effectively doubles $I_g$ through the combination, so $V = 2I_g(R_C/2 + 2R) = I_g(R_C + 4R)$. Wait, let me reconsider.

If second galvanometer is in parallel with first: combined resistance = $R_C/2$, combined full-scale current = $2I_g$. Then in series with $2R$: $V_{\max} = 2I_g(R_C/2 + 2R) = I_g(R_C + 4R)$.

**(A)**: All in series: $V = I_g(2R_C + 2R) = I_g \cdot 2(R_C + R)$.

Compare: $R_C + 4R$ vs $2R_C + 2R$: $R_C + 4R - 2R_C - 2R = 2R - R_C > 0$ (since $R_C < R/2 < 2R$).

So **(B)** gives larger voltage range. **TRUE.** **(A) FALSE.**

**Maximum current range:** For an ammeter, we want to maximize the shunt current. The galvanometer should have maximum shunt conductance in parallel.

**(C)**: All components in parallel: equivalent shunt = $R_C \| R_C \| R \| R$. The current through external circuit for full-scale: $I_{\max} = I_g \cdot \frac{R_C}{R_{\text{parallel}}}$ where $R_{\text{parallel}} = \frac{1}{2/R_C + 2/R}$. Full-scale current for the galvanometer gives: total current = $I_g(1 + R_C/R_C + R_C/R + R_C/R) = I_g(2 + 2R_C/R)$.

Actually, let me think more carefully. One galvanometer is the measuring element. The rest are shunts.

For maximum current range using one galvanometer: maximize shunt (parallel resistance should be minimized).

**(C)** All parallel: other galvanometer ($R_C$) and two resistors ($R$ each) all in parallel as shunt.
Shunt resistance: $S = \frac{1}{1/R_C + 1/R + 1/R} = \frac{1}{1/R_C + 2/R}$

$I_{\max} = I_g\left(1 + \frac{R_C}{S}\right) = I_g\left(1 + R_C\left(\frac{1}{R_C} + \frac{2}{R}\right)\right) = I_g\left(2 + \frac{2R_C}{R}\right)$

**(D)** Two galvanometers in series ($2R_C$), this combination in parallel with both resistors.
Here the "ammeter" is the series combination of galvanometers. Full scale deflection current is still $I_g$ (same current through both). Shunt = $R \| R = R/2$.

$I_{\max} = I_g\left(1 + \frac{2R_C}{R/2}\right) = I_g\left(1 + \frac{4R_C}{R}\right)$

Compare (C): $2 + 2R_C/R$ vs (D): $1 + 4R_C/R$.

Difference: $(2 + 2R_C/R) - (1 + 4R_C/R) = 1 - 2R_C/R > 0$ since $R_C < R/2$.

So **(C)** gives larger current range. **TRUE.** **(D) FALSE.**

**Answer:** BC"""

# ============================================================
# QUESTION 49: Block and spring, mass placed softly
# ============================================================
solutions[("JEE Adv 2016 Paper 2", 12)] = r"""Block $M$ on spring, amplitude $A$, equilibrium $x_0$.

**Case (i): Mass $m$ placed at $x_0$ (equilibrium position).**
At $x_0$, the block has maximum velocity $v_0 = A\omega_0 = A\sqrt{k/M}$.

After $m$ is placed (sticks): by conservation of momentum: $(M+m)v_1 = Mv_0 \implies v_1 = \frac{M}{M+m}v_0$.

New angular frequency: $\omega_1 = \sqrt{k/(M+m)}$.

New equilibrium shifts down by $mg/k$, but the velocity at the old equilibrium is $v_1$, and the displacement from new equilibrium is $mg/k$ (small). The new amplitude:

Actually, the new equilibrium is at $x_0' = x_0 + mg/k$. At the moment of placing, position is $x_0$ (displacement $-mg/k$ from new equilibrium) with velocity $v_1$.

$A_1 = \sqrt{(mg/k)^2 + (v_1/\omega_1)^2}$. But this gets complicated. The standard result: since the mass is placed at the equilibrium of the OLD system, the energy is $\frac{1}{2}(M+m)v_1^2$. The new amplitude satisfies:

$\frac{1}{2}k A_1'^2 = \frac{1}{2}(M+m)v_1^2 + \frac{1}{2}k(mg/k)^2$ (accounting for new equilibrium shift).

Hmm, for the purpose of this problem and Statement (A), the problem likely assumes horizontal surface (no gravity effect on spring). Then new equilibrium is still $x_0$.

For horizontal: $A_{\text{new}} = v_1/\omega_1 = \frac{Mv_0}{(M+m)} \cdot \sqrt{\frac{M+m}{k}} = \frac{M}{M+m} \cdot A\sqrt{\frac{k}{M}} \cdot \sqrt{\frac{M+m}{k}} = A\sqrt{\frac{M}{M+m}}$.

So amplitude changes by factor $\sqrt{M/(M+m)}$. **(A) first part TRUE.**

**Case (ii): Mass $m$ placed at $x_0 + A$ (extreme position).**
At the extreme, velocity is zero. Mass $m$ is placed with zero velocity. No momentum exchange needed. The new equilibrium is still $x_0$ (horizontal). The amplitude remains $A$ (particle at rest at distance $A$ from equilibrium). **(A) second part TRUE.**

**(B)** New time period is $T' = 2\pi\sqrt{(M+m)/k}$ in both cases. **TRUE.**

**(C)** Case (i): KE before = $\frac{1}{2}Mv_0^2$. KE after = $\frac{1}{2}(M+m)v_1^2 = \frac{1}{2}\frac{M^2v_0^2}{M+m} < \frac{1}{2}Mv_0^2$. Energy decreases. **TRUE for case (i).**

Case (ii): Initially $E = \frac{1}{2}kA^2$. After placing, still at same position with zero velocity, so $E = \frac{1}{2}kA^2$. Energy unchanged. **FALSE for case (ii).**

So "both cases" is **FALSE**. **(C) FALSE.**

**(D)** Speed at $x_0$: Case (i): $v_1 = \frac{M}{M+m}v_0 < v_0$. **Decreases.**

Case (ii): New amplitude $= A$, new $\omega = \sqrt{k/(M+m)}$. Speed at $x_0 = A\omega_1 = A\sqrt{k/(M+m)} < A\sqrt{k/M} = v_0$. **Decreases.**

**(D) TRUE.**

**Answer:** ABD"""

# ============================================================
# QUESTION 50: Electrochemical cell
# ============================================================
solutions[("JEE Adv 2016 Paper 2", 19)] = r"""The cell is: $\text{Pt}|\text{H}_2(1\,\text{bar})|\text{H}^+(1\,\text{M}) \| \text{M}^{4+}, \text{M}^{2+}|\text{Pt}$

Anode (left): $\text{H}_2 \to 2\text{H}^+ + 2e^-$, $E^\circ_{\text{anode}} = 0\,\text{V}$

Cathode (right): $\text{M}^{4+} + 2e^- \to \text{M}^{2+}$, $E^\circ_{\text{cathode}} = 0.151\,\text{V}$

$E^\circ_{\text{cell}} = 0.151 - 0 = 0.151\,\text{V}$

Nernst equation ($n = 2$):
$$E_{\text{cell}} = E^\circ_{\text{cell}} - \frac{0.059}{2}\log\frac{[\text{M}^{2+}]}{[\text{M}^{4+}]}$$

$$0.092 = 0.151 - \frac{0.059}{2}\log\frac{[\text{M}^{2+}]}{[\text{M}^{4+}]}$$

$$\frac{0.059}{2}\log\frac{[\text{M}^{2+}]}{[\text{M}^{4+}]} = 0.059$$

$$\log\frac{[\text{M}^{2+}]}{[\text{M}^{4+}]} = 2$$

So $x = 2$.

**Answer:** D"""

# ============================================================
# QUESTION 51: Ammonia complexes geometries
# ============================================================
solutions[("JEE Adv 2016 Paper 2", 22)] = r"""**$\text{Ni}^{2+}$** ($3d^8$): With NH$_3$ (moderate-strong field ligand), it forms $[\text{Ni(NH}_3)_6]^{2+}$ with **octahedral** geometry (6 coordinate, $sp^3d^2$ hybridization).

**$\text{Pt}^{2+}$** ($5d^8$): Being a heavy transition metal (second/third row), $\text{Pt}^{2+}$ strongly prefers **square planar** geometry due to large crystal field splitting. Forms $[\text{Pt(NH}_3)_4]^{2+}$.

**$\text{Zn}^{2+}$** ($3d^{10}$): With a completely filled d-orbital, there is no CFSE advantage for any geometry. With NH$_3$, it forms $[\text{Zn(NH}_3)_4]^{2+}$ with **tetrahedral** geometry ($sp^3$).

Order: octahedral, square planar, tetrahedral.

**Answer:** A"""

# ============================================================
# QUESTION 52: Molecular Orbital Theory
# ============================================================
solutions[("JEE Adv 2016 Paper 2", 25)] = r"""**(A) $\text{C}_2^{2-}$:** $\text{C}_2$ has 12 electrons, $\text{C}_2^{2-}$ has 14 electrons.

Electronic configuration (for atoms with $Z \leq 7$, $\pi_{2p}$ is below $\sigma_{2p}$):
$(\sigma_{1s})^2(\sigma^*_{1s})^2(\sigma_{2s})^2(\sigma^*_{2s})^2(\pi_{2p})^4(\sigma_{2p})^2$

All electrons are paired. **Diamagnetic. TRUE.**

**(B) $\text{O}_2^{2+}$:** $\text{O}_2$ has 16 electrons, $\text{O}_2^{2+}$ has 14 electrons.

Bond order of $\text{O}_2 = 2$, bond order of $\text{O}_2^{2+} = 3$ (removed 2 antibonding electrons).

Higher bond order means shorter (not longer) bond length. **FALSE.**

**(C) $\text{N}_2^+$ and $\text{N}_2^-$:**

$\text{N}_2$ has 14 electrons, bond order = 3.

$\text{N}_2^+$ (13 electrons): removes one electron from $\sigma_{2p}$ (or $\pi_{2p}$ — for N, the $\sigma_{2p}$ is above $\pi_{2p}$, so removal from $\sigma_{2p}$). Bond order = 2.5.

$\text{N}_2^-$ (15 electrons): adds one electron to $\pi^*_{2p}$. Bond order = $3 - 0.5 = 2.5$.

Same bond order. **TRUE.**

**(D) $\text{He}_2^+$:** Has 3 electrons: $(\sigma_{1s})^2(\sigma^*_{1s})^1$. Bond order = 0.5.

This is more stable than two isolated He atoms (one He and one He$^+$), so it does NOT have the same energy. **FALSE.**

**Answer:** AC"""

# Now write all solutions to output file
with open(output_path, 'w') as f:
    for q in questions:
        key = (q["description"], q["index"])
        if key in solutions:
            q["cot_solution"] = solutions[key].strip()
        else:
            print(f"WARNING: No solution for {key}")
        f.write(json.dumps(q, ensure_ascii=False) + "\n")

print(f"Wrote {len(questions)} solutions to {output_path}")

# Verify
missing = 0
for q in questions:
    key = (q["description"], q["index"])
    if key not in solutions:
        missing += 1
        print(f"  Missing: {key}")
    else:
        sol = solutions[key]
        gold = q["gold"]
        if f"**Answer:** {gold}" not in sol:
            print(f"  MISMATCH: {key} - gold={gold}, solution ending doesn't match")

if missing == 0:
    print("All questions have solutions!")
