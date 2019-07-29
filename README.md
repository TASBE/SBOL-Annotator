[![Build Status](https://travis-ci.org/TASBE/SBOL-Annotator.svg?branch=master)](https://travis-ci.org/TASBE/SBOL-Annotator)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/TASBE/SBOL-Annotator/master)
# SBOL Interaction Annotation Tool
There are two options to running the Jupyter Notebook: install it locally on your computer or using Binder. To use Binder, click on the badge to launch Binder. This will run it for 12 hours, but after 10 minutes of inactivity, it will be need to be launched again. To install it locally, follow the instructions below.
### Instructions for Installation
- Install [Jupyter](https://jupyter.org/install) and [Python 3](https://www.python.org/downloads/) (if not installed already)  
  
  
_The following instructions must be run in command line:_  
- Install the required Python modules with:  
    `pip3 install -r requirements.txt`
- Enable the extensions:  
    `jupyter contrib nbextension install --user`  
    `jupyter nbextension enable init_cell/main`  
    `jupyter trust SBOLAnnotations.ipynb`
- In the folder with the .ipynb file, run:  
    `jupyter notebook SBOLAnnotations.ipynb`
### Instructions for Use
- Enable Initialization Cells (on initial install)  
  
![](enableinitializationcells.gif)
### Example Material
The BBa_K808000.gb and BBa_K808000.xml are example GenBank and SBOL files respectively.
