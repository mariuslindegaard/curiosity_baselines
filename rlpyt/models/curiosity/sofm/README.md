# SOFM - Self-organizing Feature Maps module in C++ with Python wrappings

## Install

### C++

Requires `cmake`, c++ compiler and Eigen. All can probably be installed with (on Ubuntu 18.04)
```{bash}
sudo apt install cmake build-essential libeigen3-dev
```

### Python wrappings

Requires [pybind11](https://github.com/pybind/pybind11), which can installed with
```{bash}
pip install -r requirements.txt
```
**Note**: not tested, so might need to do
```{bash}
pip install "pybind11[global]"
```
This does a system-wide installation, so if you're using conda, you might need to use 
```{bash}
conda install -c conda-forge pybind11
```
This command is not tested, but instructions for installing pybind11 can be found here: https://pybind11.readthedocs.io/en/stable/installing.html.