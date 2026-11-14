# Bearing load in `swfea.static()`: what was measured

2026-11-14, holly-pc, SolidWorks 2026 SP0. The lead was a benchmark run's own copy
([eval/terra-high-c/swfea_bearing.py](../terra-high-c/swfea_bearing.py)), which needed a coordinate system made by hand
in the part and took one signed number along its X.

`('bearing', faces, (Fx, Fy, Fz))` is now a load kind of `static()`. The case is `python solidworks/selftest.py bearing`;
the comparison below is [compare.py](compare.py), with its numbers in [compare.json](compare.json).

## The part

A 60 x 60 x 10 mm plate, a 20 mm bore through the middle along Z, fixed on the edge face x = -30. 100 N on the bore.
Mesh 2.0 mm with 0.6 mm on the bore, 82,345 nodes. Printed PETG, E 1.9 GPa.

## Against hand values

Pressure is the radial stress on the bore wall with its sign turned, read at the nodes on the wall and clear of the two
rims. θ is the angle round the bore from the force direction. p₀ = 4 F / (π d t) = 0.6366 MPa.

| Check | Force +X | Force at 135° in XY | Hand |
| --- | --- | --- | --- |
| Reaction, N | -100.001, 0.000, 0.001 | 70.712, -70.710, 0.000 | equal and opposite |
| Pressure at θ = 0, MPa | 0.6398 | 0.6379 | 0.6366 |
| Largest pressure for θ over 95°, MPa | 0.0044 | 0.0019 | 0 |
| Pressure at θ = 45°, MPa | 0.2228 | 0.2248 | 0.2251 = p₀ cos³ 45° |
| Pressure summed over the bore, N | 75.15 | 74.89 | 75 = 3 F / 4 |
| Traction along the force summed over the bore, N | 99.99 | 99.86 | 100 |

A bore along X with the force (0, 60, -80) N reacted (-0.002, -59.998, 79.997) N, and its pressure peak faced
(0.57, -0.82) in YZ against (0.6, -0.8).

The first run at 0.5 mm on the bore (100,145 nodes) gave the whole curve:

| θ, degrees | 0 | 15 | 30 | 45 | 60 | 75 | 90 and beyond |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Measured pressure, MPa | 0.638 | 0.575 | 0.413 | 0.224 | 0.078 | 0.009 | under 0.001 |
| p₀ cos³ θ | 0.637 | 0.574 | 0.413 | 0.225 | 0.080 | 0.011 | 0 |
| p₀ cos θ (cosine normal pressure) | 0.637 | 0.615 | 0.551 | 0.450 | 0.318 | 0.165 | 0 |

So SolidWorks' "sinusoidal" bearing load is a traction in the direction of the force, of p₀ cos θ per projected area.
Per area of wall that is p₀ cos² θ, of which the normal part is p₀ cos³ θ and the rest is shear along the wall. The peak
is the textbook value; the shape is narrower than a cosine pressure, and a quarter of the force goes in as shear.

The parabolic option (`BEARING_PARABOLIC` as a fourth item) peaked at 0.7542 MPa against 3 F / (2 d t) = 0.750, with
pressure 0.421, 0.186 and 0.045 MPa at 30°, 45° and 60° against pₖ cos⁴ θ = 0.422, 0.188 and 0.047.

## Against the other two loads

| | `'bearing'` | `'bearing'` parabolic | `'remote'` at the bore centre | `'normal'` 100 N |
| --- | --- | --- | --- | --- |
| Reaction, N | 100.001 | 100.002 | 100.000 | **0.000** |
| Pressure at θ = 0, MPa | 0.640 | 0.754 | 0.028 | 0.159 |
| Radial stress on the back half, largest, MPa | 0.004 | 0.005 | 0.318 | 0.160 |
| Hoop stress on the wall at θ = ±90°, MPa | 0.992 | 0.969 | -0.005 | 0.175 |
| Largest von Mises on the wall, MPa (θ) | 1.189 (-70°) | 1.172 (-67°) | 0.358 (-129°) | 0.314 |
| `r.peak()` with the default mask, MPa | 0.539 | 0.607 | 0.317 | 0.162 |
| Wall moves along X: front, back, µm | 12.3, 0.4 | 13.0, 0.4 | 2.67, 2.67 | 1.8, -0.7 |

Nominal stress in the two ligaments beside the bore is 100 / (40 x 10) = 0.25 MPa, so the bearing load's 0.99 MPa is
a factor of 4.0 on it, in the range a pin-loaded lug of this proportion has. The rigid load holds the bore round, so
the ligaments beside it carry almost no hoop stress at the wall and the hole does not stretch.

## A bore in two halves

Every bore of a STEP import is two half faces. The plate went out to STEP and back ([split_bore.py](split_bore.py)); its
bore came back split along y = 0.

| Faces given | Force | Reaction, N | Pressure at θ = 0, MPa | at 45° | Back half, largest |
| --- | --- | --- | --- | --- | --- |
| both halves | +X (along the split) | -100.000, 0.000, 0.000 | 0.640 | 0.224 | 0.011 |
| both halves | +Y (into one half) | -0.001, -99.998, 0.000 | 0.640 | 0.223 | 0.010 |
| one half only | +X | -100.001, 0.000, -0.001 | 0.636 | 0.223 | 0.021 |

Both halves behave as the one face does. Given one half only, the reaction is still the whole 100 N: nothing warns
that half the bore was left out, so give a bearing load every face of its bore.

## What it cannot do

No contact and no clearance: the loaded arc is always exactly half the bore. The pin does not bend, and the load does
not move towards one end of the bore. The force must be square to the bore axis; one load takes the faces of one axis.

## API facts found on the way

- `AddBearingLoad(feature, faces, err)` takes the coordinate-system feature itself; an array of it is a type mismatch
  (the benchmark run's first try).
- `FeatureManager.CreateCoordinateSystemUsingNumericalValues` makes the coordinate system from numbers. Face objects
  picked before it stay valid, and stay valid when it is deleted. The Euler order was read back, not assumed.
- `Extension.CreateCoordinateSystem` does not exist on SolidWorks 2026.
- `Direction = 0` is the system's X; a new bearing load starts with `Direction = 1`. `DistributionType` 0 is
  sinusoidal, 1 parabolic.
