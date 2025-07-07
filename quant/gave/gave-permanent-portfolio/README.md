# activate venv
```
conda activate portfolio_simulation
```

# recreate conda env
```
conda env create -f conda_environment.yml
```

# install new package
```
conda search <package-name>
conda install -c conda-forge <package-name>
# add <package-name> in conda_environment.yml
conda env update --file conda_environment.yml --prune
conda list <package-name>
```