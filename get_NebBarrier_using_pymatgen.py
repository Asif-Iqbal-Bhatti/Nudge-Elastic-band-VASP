#!/usr/bin/env python3

'''
##########################################################################
# Author: Asif Iqbal
# GitHub: Asif_em2r
# USAGE:  Generate spline NEB plot using pymatgen tools
##########################################################################
'''

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pymatgen.analysis.transition_state import NEBAnalysis

outFile = 'Fe210'
nb = NEBAnalysis.from_dir(root_dir = 'Fe210', )
ext = nb.get_extrema(normalize_rxn_coordinate=True)

r, e, f = nb.r, nb.energies, nb.forces
data = pd.DataFrame({'Reaction Coordinate [A]': r, 
                     'Energy [eV]': e, 
                     'Relative Energy [eV]': e-e[0], 
                     'Forces [eV/A]': f}
                     )

data.to_csv(outFile + '_data.csv', index=False)
print(data)

nb.setup_spline(spline_options={'saddle_point': 'zero_slope'})
nb.get_plot(normalize_rxn_coordinate=True, label_barrier=True)
plt.xlabel("Reaction Coordinate [$\\AA$]")
plt.savefig(outFile+"_PMG.pdf", dpi=300, bbox_inches='tight')
plt.show()
