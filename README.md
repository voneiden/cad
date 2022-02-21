# Setup

1) Grab miniforge from https://github.com/conda-forge/miniforge
2) `conda install mamba`
3) `mamba install -c cadquery -c conda-forge cq-editor=master`



# Force reinstall

`mamba install -c conda-forge -c cadquery cadquery=master --force-reinstall`

`mamba install -c cadquery -c conda-forge cq-editor=master --force-reinstall`

# Install cqlib in editable mode

cqlib contains some helper functions that I use. If you want to run my scripts
you can install this project as editable library using

`pip install -e .`

