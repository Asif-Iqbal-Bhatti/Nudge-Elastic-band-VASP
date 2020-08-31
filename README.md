# Nudge-Elastic-band

----------------------------NOTE----------------------------

Please, keep in mind the setup of the calculation in this directory. 
The barrier obtained (46.3 meV/b) with this setup agrees favorably with 
the values given in the references. Hence, I can be sure my setup is right, 
and I can extend this approach to High Entropy Alloys.

NB:: The relaxation should be done perpendicular to the screw dislocation line, 
that is on the plane. (T T F VASP5 format).

- Initial and finally geometry should be fully relaxed. 
- Then generate with ASE-NEB, images obtained linearly by interpolating betweeen
  the initial and final image. 
- The intermediate images should be constrained and relaxed accordingly.
- 

REF:

1 --> https://prod-ng.sandia.gov/techlib-noauth/access-control.cgi/2017/1711595.pdf
2 --> https://slideplayer.com/slide/2350579/
3 --> Peierls potential of screw dislocations in bcc transition metals: Predictions from density functional theory
