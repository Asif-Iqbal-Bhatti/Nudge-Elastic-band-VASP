#!/usr/bin/env python3

'''
##########################################################################
# Author: Asif Iqbal
# GitHub: Asif_em2r
# USAGE:  Generate spline NEB plot for VTST script using force based
#         spline plot and estimate the barrier.
##########################################################################
'''

import os
import numpy as np 
import matplotlib.pyplot as plt


# READ IN THE MEP FILE
data = np.loadtxt("neb.dat", usecols=(1, 2, 3))
R, E, F = data[:, 0], data[:, 1], data[:, 2]
NumI = len(R)

# CALCULATE THE CUBIC PARAMETERS FOR EACH INTERVAL (A, B, C, D)
dR = np.diff(R)
F1 = F[:-1] * dR
F2 = F[1:] * dR
U1 = E[:-1]
U2 = E[1:]
Fs = F1 + F2
Ud = U2 - U1
a = U1
b = -F1
c = 3 * Ud + F1 + Fs
d = -2 * Ud - Fs

NumJ = 20 # default
# GENERATING THE OUTPUT FILE CONTAINING THE SPLINE
with open("spline.dat", 'w') as f:
    for i in range(NumI):
        f.write(f"{i:10.9f} {R[i]} {E[i]} {F[i]}\n")
        if i != (NumI - 1):
            for j in range(1, NumJ):
                fraction = j / NumJ
                Ispl = i + fraction
                Rspl = R[i] + fraction * dR[i]
                Espl = d[i] * fraction**3 + c[i] * fraction**2 + b[i] * fraction + a[i]
                Fspl = -(3 * d[i] * fraction**2 + 2 * c[i] * fraction + b[i]) / dR[i]
                f.write(f"{Ispl:10.9f} {Rspl:12.9f} {Espl:12.9f} {Fspl:12.9f}\n")

# FINDING EXTREMA ALONG THE MEP
Desc = c**2 - 3 * b * d
f = np.zeros_like(Desc)

# Quadratic case
quadratic_mask = np.logical_and(d == 0, c != 0)
f[quadratic_mask] = -(b[quadratic_mask] / (2 * c[quadratic_mask]))

# Cubic case 1
cubic_case1_mask = np.logical_and(d != 0, Desc >= 0)
f[cubic_case1_mask] = -(c[cubic_case1_mask] + np.sqrt(Desc[cubic_case1_mask])) / (3 * d[cubic_case1_mask])

# Check if f is within [0, 1]
valid_f_mask = np.logical_and(f >= 0, f <= 1)

# Calculate the positions and values of extrema
Pos = np.where(valid_f_mask, np.arange(NumI - 1) + f, 0)
extrema_values = d * f**3 + c * f**2 + b * f + a
Ext = {pos: value for pos, value in zip(Pos, extrema_values) if pos != 0}

# Cubic case 2
cubic_case2_mask = np.logical_and(d != 0, Desc >= 0)
f[cubic_case2_mask] = -(c[cubic_case2_mask] - np.sqrt(Desc[cubic_case2_mask])) / (3 * d[cubic_case2_mask])

# Check if f is within [0, 1]
valid_f_mask = np.logical_and(f >= 0, f <= 1)

# Calculate the positions and values of extrema
Pos = np.where(valid_f_mask, np.arange(NumI - 1) + f, 0)
extrema_values = d * f**3 + c * f**2 + b * f + a
Ext.update({pos: value for pos, value in zip(Pos, extrema_values) if pos != 0})

k = 0
# Write out the extrema information to EXTREMUM.dat
with open("EXTREMUM.dat", 'w') as f:
    for Pos in sorted(Ext.keys()):
        k += 1
        outline = f"Extremum {k} found at image {Pos:9.6f} with energy: {Ext[Pos]:9.6f}\n"
        f.write(outline)

########
# PLOTING THE SPLINE CURVE BASED ON FORCE
########
data = np.loadtxt("spline.dat")
x_spline = data[:, 1]
y_spline = data[:, 2]

# Read data from the neb.dat file for comparison points
data1 = np.loadtxt("neb.dat")
x_neb = data1[:, 1]
y_neb = data1[:, 2]

# Plot the spline curve and neb.dat points
plt.figure(figsize=(8, 6))
plt.grid(False)
plt.xlabel("Reaction Coordinate [$\\AA$]")
plt.ylabel("Energy [eV]")
plt.plot(x_spline, y_spline, label="Spline Curve", color='b', linewidth=2.5)
plt.scatter(x_neb, y_neb, label="NEB Points", color='red', marker='o', s=30)
plt.legend()
plt.savefig("MEP.pdf", dpi=300, bbox_inches='tight')
plt.show()
