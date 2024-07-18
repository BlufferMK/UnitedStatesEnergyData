# USElectricalEnergyData

This repository contains python Jupyter notebook for calling information from the Electricity Map api to get power production breakdown by source type, along with Carbon intensity data in gCO2e/kWh for utilities across the United States.  In addition, there is information about large solar power installations in New Mexico from the NREL. There are also images of maps showing utility geographical boundaries from electricity map api, as well as maps that identify different types of electrical generation facililites.  

the Elec_Generation_US.ipynb file, when run, calls the previous 24 hours of information on powerbreakdown and Carbon intensity for U.S. electrical utilities, merges the data with previously collected data and exports a csv file named runningUSenergy_data.csv.  It also filters this data file, removing estimated values for power breakdown.  These are updated as the data become available.  

Electricitymaps.com is the source of the power generation data.  electricitymaps.com

All power plants in the United States are mapped out with information at https://synapse.maps.arcgis.com/apps/dashboards/201fc98c0d74482d8b3acb0c4cc47f16

The US Wind Turbine Database has an interactive heatmap showing wind turbine locations and details at https://eerscmap.usgs.gov/uswtdb/viewer/#6.43/41.947/-93.738

US Solar Photovoltaic Database viewer is at https://eerscmap.usgs.gov/uspvdb/viewer/#3/37.25/-96.25

Hydroelectric power plants in the U.S. are mapped at https://hub.arcgis.com/maps/purdueuniversity::hydroelectric-power-plants-in-the-u-s-/explore?location=36.490988%2C-100.319900%2C4.85

Solar Irradiance data come from the NSRDB solar irradiance database at https://nsrdb.nrel.gov/data-viewer
