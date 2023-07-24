#!/usr/bin/env python3.11

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

cwd = os.getcwd()
NumJ = 20 # default

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
Ext = {}
for i in range(NumI - 1):
    Desc = c[i]**2 - 3 * b[i] * d[i]
    if Desc >= 0:
        f = -1
        # Quadratic case
        if d[i] == 0 and c[i] != 0:
            f = -(b[i] / (2 * c[i]))
        # Cubic case 1
        elif d[i] != 0:
            f = -(c[i] + np.sqrt(Desc)) / (3 * d[i])
        if 0 <= f <= 1:
            Pos = i + f
            Ext[Pos] = d[i] * f**3 + c[i] * f**2 + b[i] * f + a[i]
        # Cubic case 2
        if d[i] != 0:
            f = -(c[i] - np.sqrt(Desc)) / (3 * d[i])
            if 0 <= f <= 1:
                Pos = i + f
                Ext[Pos] = d[i] * f**3 + c[i] * f**2 + b[i] * f + a[i]

NumE = 0
# Write out the extrema information to exts.dat
with open("EXTS.dat", 'w') as f:
    for Pos in sorted(Ext.keys()):
        NumE += 1
        outline = f"Extremum {NumE} found at image {Pos:9.6f} with energy: {Ext[Pos]:9.6f}\n"
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
plt.savefig("mep.pdf", dpi=300, bbox_inches='tight')
plt.show()
