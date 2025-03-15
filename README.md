alphafold_pulldown_wrapper

#### Wrapper / utility functions around alphafoldpulldown

This code is set up to work on Chavez Lab machines, and if you are re-using it for any other purpose, you will need to do additional set-up. See [Github - KosinskiLab/AlphaPulldown](https://github.com/KosinskiLab/AlphaPulldown) for instructions on setting up local data needed to run AlphaPulldown

#### Install instructions on Chavez Lab machines:

```
conda create -n alphafold_pulldown
conda activate alphafold_pulldown
mamba install -c conda-forge -c bioconda -c omnia python=3.11 openmm=8.0 pdbfixer=1.9 kalign2 hhsuite hmmer modelcif
python3 -m pip install alphapulldown
pip install -U "jax[cuda12]"
```
