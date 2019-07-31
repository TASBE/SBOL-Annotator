[![Build Status](https://travis-ci.org/TASBE/SBOL-Annotator.svg?branch=master)](https://travis-ci.org/TASBE/SBOL-Annotator)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/TASBE/SBOL-Annotator/master?filepath=SBOLAnnotations.ipynb)
# SBOL Interaction Annotation Tool
There are two options to running the Jupyter Notebook: install it locally on your computer or using Binder. To use Binder, click on the badge to launch Binder. This will run it for 12 hours, but after 10 minutes of inactivity, it will be need to be launched again. To install it locally, follow the instructions below.
### Instructions for Installation
- Install [Jupyter](https://jupyter.org/install) and [Python 3.6](https://www.python.org/downloads/) (if not installed already)  
  
  
_The following instruction must be run in command line:_  
- Run `./install` to install the required modules and enable extensions

### Instructions for Use
1. In the folder with the .ipynb file, run:  
    `jupyter notebook SBOLAnnotations.ipynb`
2. Follow the flow in the Jupyter notebook. Upload the GenBank files first, then follow fill out the subsequent sections. If you make a mistake, start over by reuploading the GenBank files. For now, there is no option to delete the interactions and components, but there will be in the future.
3. Upload the annotated construct to SynBioHub.

### Example Material
The BBa_K808000.gb and BBa_K808000.xml are example GenBank and SBOL files respectively.
