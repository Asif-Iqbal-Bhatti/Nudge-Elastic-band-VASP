#!/usr/bin/env python3

""" 
################################################################################
# Author: Asif Iqbal
# GitHUb: AIB_EM
# Usage: For publication plot. THis script reads the neb.dat file
#        generated from VTST sctipts and using scipy perform the
#        cubic interpolation (spline). 
# 
#################################################################################
"""

import numpy as np
import matplotlib.pyplot as plt
from ase.io import read, write
from scipy.interpolate import CubicSpline

def get_NebPLot():
    outFile = 'Fe210'
    data = np.loadtxt("neb.dat")    
    pos = read('00/CONTCAR')
    natoms = len(pos.get_positions())
    
    x = data[:, 1]
    yy = data[:, 2] / natoms
    cs = CubicSpline(x, yy)
    new_x = np.linspace(min(x), max(x), 100)
    f_dft = cs(new_x)

    plt.figure(figsize=(8, 6))
    plt.plot(x, yy, "ko", label="Raw NEB points")
    plt.plot(new_x, f_dft, "m-", label="Interpolated NEB")
    plt.axhline(color="black", linestyle="--")
    plt.xlabel("Reaction coordinate [$ \AA $]")
    plt.ylabel("Energy [eV/atom]")
    plt.legend(loc="best")
    plt.grid(True)
    plt.title(f"{outFile}")
    plt.savefig(f"{outFile}_MEP.pdf", dpi=300, bbox_inches='tight')
    plt.show()

get_NebPLot()
