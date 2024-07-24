Depletion approximation
=======================

- Example: :doc:`Traditional GaInP/InGaAs/Ge solar cell <../Examples/example_3J_with_DA_solver>`

Material and device parameters
---------------------------------

The table below lists the device and material parameters required for the depletion approximation solver. It is not
necessary to set all these parameters explicitly, as some can be calculated from other parameters or have default values.
However, there is no reason to assume the default values are reasonable for your material/device!

========================== ============================ ============================= ========== ======== =============================================
Parameter                  Set location                 Solcore label                 Units      Default  Calculable?
========================== ============================ ============================= ========== ======== =============================================
n-type region SRV          ``Junction``                 ``sn`` :sup:`[1]`             m s-1      0        No
p-type region SRV          ``Junction``                 ``sp`` :sup:`[1]`             m s-1      0        No
Permittivity	           ``Junction`` or ``material`` ``permittivity``              F m-1      none     Yes, from ``relative_permittivity`` :sup:`[2]`
Electron diffusion length  p-type ``material``          ``electron_diffusion_length`` m          none     No
Hole diffusion length      or n-type ``material``       ``hole_diffusion_length``     m          none     No
Electron mobility          p-type ``material``          ``electron_mobility``         m2 V-1 s-1 0.94     No :sup:`[3]`
Hole mobility              n-type ``material``          ``hole_mobility``             m2 V-1 s-1 0.05     No :sup:`[3]`
Intrinsic carrier density  ``material``                 ``ni``                        m-3        none     Yes, from ``Nc``, ``Nv`` and ``band_gap`` :sup:`[4]`
Donor (n-type) density     n-type ``material``          ``Nd``                        m-3        1        No
Acceptor (p-type) density  p-type ``material``          ``Na``                        m-3        1        No
Built-in voltage           ``Junction`` (optional)      ``Vbi``                       V          none     Yes, from ``Nd``, ``Na`` and ``ni`` :sup:`[5]`
Shunt resistance           ``Junction`` (optional)      ``R_shunt``                   Ohm m2     1e14     No :sup:`[6]`
========================== ============================ ============================= ========== ======== =============================================

Notes:

1. The n/p labels for the surface recombination velocities ``sn`` and ``sp`` refer to the region, not the carrier type,
   e.g. ``sn`` is the recombination velocity at
   the n-type surface, which can be the front or rear surface depending on the cell configuration.
2. ``relative_permittivity`` is a dimensionless quantity: permittivity = vacuum permittivity * relative permittivity
3. If the material is not in the :doc:`mobility model database <../Systems/Materials>`, which calculates the mobility
   based on the alloy composition (if applicable), temperature, and doping level, the model will default to calculating
   the mobility for GaAs. Thus if you are using a custom  material not included in the mobility database, you should set
   this explicitly, since there is no reason to assume the GaAs values are reasonable for your material.
4. The intrinsic carrier density ``ni`` can be calculated from the conduction and valence band effective density of states
   (``Nc`` and ``Nv`` respectively, units m-3) and ``band_gap`` (SI units used by Solcore: J, NOT eV!).
5. In general, you don't need to set the built-in voltage ``Vbi`` since it is calculated from ``Nd``, ``Na`` and ``ni``,
   all of which are already required.
6. An ideal cell has infinitely high shunt resistance (hence the extremely high default value).


Background
----------

The depletion approximation provides an analytical - or semi-analytical
- solution to the Poisson-drift-diffusion equations described in the
previous section applied to simple PN homojunction solar cells.
Historically, it has been used extensively to model solar cells and it
is still valid, to a large extent, for traditional PN junctions. More
importantly, it requires less input parameters than the PDD solver and
these can be easily related to macroscopic measurable quantities, like
mobility or diffusion lengths. The DA model is based on the assumption
that around the junction between the P and N regions, there are no free
carriers and therefore all the electric field is due to the fixed,
ionized dopants. This “depletion” of free carriers reaches a certain
depth towards the N and P sides; beyond this region, free and fixed
carriers of opposite charges balance and the regions are neutral. Under
these conditions, Poisson’s equation decouples from the drift and
diffusion equations and it can be solved analytically for each region.
For example, for a PN junction with the interface between the two
regions at :math:`z=0`, the solution to Poisson's equation will be:

.. math::

   \phi(z) =
   \left\{
       \begin{array}{ll}
           0  & \mbox{if } z < -w_p \\
           \frac{qN_a}{2\epsilon_s}(z+w_p)^2  & \mbox{if } -w_p < z < 0 \\
           -\frac{qN_d}{2\epsilon_s}(z-w_n)^2 + V_{bi} & \mbox{if } 0 < z < w_n  \\
           V_{bi} & \mbox{if } w_n < z
       \end{array}
   \right.

where :math:`w_n` and :math:`w_p` are the extensions of the depletion
region towards the N and P sides, respectively, and can be found by the
requirement that the electric field :math:`F` and the potential
:math:`\phi` need to be continuous at :math:`z=0`. :math:`V_{bi}` is the
built-in voltage, which can be expressed in terms of the doping
concentration on each side, :math:`N_d` and :math:`N_a`, and the
intrinsic carrier concentration in the material, :math:`n_i^2`:

.. math:: V_{bi} = \frac{k_bT}{q} \ln \left(\frac{N_dN_a}{n_i^2} \right)

Another consequence of the depletion approximation is that the
quasi-Fermi level energies are constant throughout the corresponding
neutral regions and also constant in the depletion region, where their
separation is equal to the external bias :math:`qV`. Based on these
assumptions, the drift-diffusion equations
simplify and an analytical expression can be found for the dependence of
the recombination and generation currents on the applied voltage. A full
derivation of these expressions is included in
Nelson (2003) ([#Nelson2003]_).

Solcore’s implementation of the depletion approximation includes two
modifications to the basic equations. The first one is allowing for an
intrinsic region to be included between the P and N regions to form a
PIN junction. For low injection conditions (low illumination or low
bias) this situation can be treated as described before, simply
considering that the depletion region is now widened by the thickness of
the intrinsic region. Currently, no low doping level is allowed for this
region.

The second modification is related to the generation profile, which in
the equations provided by Nelson is given by the BL law
which has an explicit dependence on :math:`z` and results in analytic
expressions for the current densities. In Solcore, we integrate the
expressions for the drift-diffusion equations under the depletion
approximation numerically or by using the Green's function method to allow
for an arbitrary generation profile calculated with any of the :doc:`optical
solvers <../Optics/optics.rst>`. It should be noted that although the equations
are integrated numerically this will not be a self-consistent solution of the
Poisson-drift-diffusion equations, as is achieved by the PDD solver.

Detailed balance functions
--------------------------

.. automodule:: solcore.analytic_solar_cells.depletion_approximation
    :members:
    :undoc-members:

References
----------

.. [#Nelson2003] Nelson, J.: The Physics of Solar Cells. Imperial College Press, London; River Edge, NJ: Distributed by World Scientific Pub. Co, (2003)
