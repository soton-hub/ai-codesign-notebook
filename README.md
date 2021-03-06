# ai-codesign-notebook

[![DOI](https://zenodo.org/badge/472441450.svg)](https://zenodo.org/badge/latestdoi/472441450) 

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/soton-hub/ai-codesign-notebook/main?labpath=cotads_notebook.ipynb)

COdesigning Trustworthy Autonomous Diabetes Systems `codesign_notebooks`.

This software is Copyright (c) 2022 University of Southampton and released on the Apache 2.0 License.

Authors: Chris Duckworth\*, Amid Ayobi\*, Jakub Dylag, Aisling O'Kane, Paul Marshall, Anitha Kumaran, Matthew Guy, Michael Boniface

\* Co-first authors.

Contact : C.J.Duckworth@soton.ac.uk

## Introduction

This repository contains an interactive computational notebook (and underlying code) used to facilate codesign sessions for the application of machine learning in type-1 diabetes. The notebook introduces a basic example machine learning model and the data it learns from to facilate discussion about machine learning's role in type-1 diabetes management. The notebook is designed to be used for a total of 5 hours (5 1-hour sessions). 

The project, COdesigning Trustworthy Autonomous Diabetes Systems (COTADS), is funded by [The UKRI Trustworthy Autonomous Systems (TAS) Hub](https://www.tas.ac.uk/) which brought together young people with type-1 diabetes (and their care-givers), clinicians, human-computer interaction experts and data scientists to design algorithms for diabetes management. The software contained here was used in these sessions.

## Try the notebook yourself

You can try the notebook and interactive elements yourself by accessing it on Binder:

[COTADS Codesign Notebook on Binder](https://mybinder.org/v2/gh/soton-hub/ai-codesign-notebook/HEAD?labpath=cotads_notebook.ipynb)

## Notebook topics

The notebook introduces a basic machine learning model and the data it learned from to facilate discussion. The notebook primarily uses diagrams, text, and interactive widgets to introduce topics. 
Here is the over-arching structure of the notebook and the key features.

### Part I: How can data support our health and wellbeing?
- Health and Wellbeing Data (Text, Diagram)
- Blood Glucose Level Data (Text, Interactive Widget)

### Part II: What does a dataset look like?
- Type-1 Diabetes Exchange Dataset (Text, Interactive Tabledata)
- Data and Representation (Text, Diagram, Question)

### Part III: What is a machine learning model?
- Introduction to machine learning (Text, Diagram, Question)

### Part IV: Can a machine learning model predict health risks?
- Example model (Text, Interactive Widget, Question)

### Part V: How does a machine learning model predict risk?
- Example model feature importance (Text, Diagram, Question)
- How would you rate the ML model features? (Text, Interactive Task and Widget) 
- How would you define your own fictional ML Model? (Interactive Task)

## Key files 

- [`cotads_notebook.ipynb`](./cotads_notebook.ipynb) : static version of the notebook used for the co-design sessions. Has dependencies on data in `./data`,  `./static_elements` and `./cotads_code.py`.
- [`cotads_code.py`](./cotads_code.py) : version of code used in the notebook used for the co-design sessions. Has dependencies on data in `./data`. 

## Sub-directories

- `data` : Contains data used for notebook content. All data used is publically available. Tabledata is taken or derivative of the [T1DExchange](https://t1dexchange.org/). Example CGM data is taken anonymously from the [CITY](https://clinicaltrials.gov/ct2/show/NCT03263494) study.
- `static_elements` : All images used in the current version of the jupyter notebook.
