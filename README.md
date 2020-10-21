# Calculate Peierls barrier for HEAs using Nudge Elastic band or Drag Method

NB: The setting for the NEB calculations can be tricky at times therefore, caution should be taken while using the provided code.

The barrier obtained (Ta: 46.3 meV/b) with this setup agrees favorably with 
the values given in the references. Hence, I can be sure my setup is right, 
and I can extend this approach to High Entropy Alloys.

- Initial and final geometry should be fully relaxed. 
- Generate with ASE-NEB the transition path (initial guess path) between the initial 
  and final configuration by interpolating linearly or using idpp. 
- The intermediate images should be constrained and relaxed accordingly.

#---------------------------------------------------------------------------------------

neb_vasp.py calls selective_dynamics.sh bash file to append T T F to the POSCAR file (This is just an example).
For Drag method, you should constrained the atoms according to the problem but for NEB calculation, it
will find the path automatically.
Calling a script from python is not a good idea, I am sure there must be a best and 
quick way to internally call the function using "ase" module (https://wiki.fysik.dtu.dk/ase/). 
```
#----------------- Constraining the atoms ---------------------
#shutil.copyfile('POSCAR_'+str(cnt).zfill(2), 'POSCAR' )
initial = read( 'POSCAR_'+str(cnt).zfill(2) )
p_pos   = initial.get_positions()
p_ucell = initial.get_cell()
p_type  = initial.get_chemical_symbols()
p_ll = Atoms(positions=p_pos, symbols=p_type, cell=p_ucell, pbc=(1,1,1) )
#for atom in p_ll:
#	p_constr.append( FixedPlane(atom.index, ( 0, 0, 1)) )
p_constr = [ FixedPlane( atom.index, ( 0, 0, 1) )  for atom in p_ll ]
p_ll.set_constraint(p_constr)
write_vasp("POSCAR", atoms=p_ll, vasp5=True, ignore_constraints=False)
#subprocess.call(['../selective.sh'], shell = False)
os.chdir('../')		
cnt +=1
```

#---------------------------------------------------------------------------------------

NB :: The relaxation should be done perpendicular to the screw dislocation line, 
that is on the plane. (T T F VASP5 format), if you are using "Drag method".

REF:

1 --> https://prod-ng.sandia.gov/techlib-noauth/access-control.cgi/2017/1711595.pdf

2 --> https://slideplayer.com/slide/2350579/

3 --> Peierls potential of screw dislocations in bcc transition metals: Predictions from density functional theory
