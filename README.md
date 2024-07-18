# NewMexicoEnergyData

This repository contains python Jupyter notebook for calling information from the Electricity Map api to get power production breakdown by source type, along with Carbon intensity data in gCO2e/kWh for utilities serving New Mexico.  In addition, there is information about large solar power installations in New Mexico from the NREL. 

the Elec_Generation_one_export.ipynb file, when run, calls the previous 24 hours of information on powerbreakdown and Carbon intensity for the utilities serving New Mexico, merges the data and exports a csv file.