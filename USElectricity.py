# %% [markdown]
# # Electricity Generation from api.electricitymap.org
# ---

# %% [markdown]
# SECTION 1 
# collect data on carbon intensity, zones within SW , and power breakdown from the electricitymap api

# %%
# Dependencies and Setup


import pandas as pd 
import requests 


# %%

# zones for electrical utilities in US
zones = ["US-SW-PNM", "US-SW-EPE", "US-SW-WALC", "US-NW-PACE", "US-NW-PSCO", "US-CENT-SWPP", "US-TEX-ERCO", "US-MIDW-AECI","US-SW-AZPS","US-SW-AZPS",
         "US-NW-WACM", "US-SW-SRP", "US-SW-TEPC", "US-CENT-SPA", "US-CAL-IID", "US-CAL-CISO", "US-CAL-BANC","US-CAL-BANC", "US-CAL-TIDC", 
          "US-CAR-CPLE", "US-CAR-CPLW", "US-CAR-DUK", "US-CAR-SC", "US-CAR-SCEG", "US-CAR-YAD", "US-FLA-FMPP", "US-FLA-FPC" , "US-FLA-FPL",
          "US-FLA-GVL" , "US-FLA-HST", "US-FLA-JEA", "US-FLA-SEC", "US-FLA-TAL", "US-FLA-TEC", "US-MIDW-AECI" , "US-MIDW-LGEE", "US-MIDW-MISO",
          "US-NE-ISNE", "US-NW-BPAT", "US-NW-CHPD", "US-NW-DOPD", "US-NW-GCPD", "US-NW-GRID",  "US-NW-IPCO" , "US-NW-NWMT", "US-NW-NEVP", 
           "US-NW-PACW",  "US-NW-PGE", "US-NW-PSEI", "US-NW-SCL", "US-NW-TPWR", "US-NW-WAUW", "US-NY-NYIS", "US-SE-SEPA", "US-SE-SOCO" , 
           "US-TEN-TVA"]


# %%

# get carbon intensity history for the US utilities
urls = []
for index, url in enumerate(zones):
    url = f'https://api.electricitymap.org/v3/carbon-intensity/history?zone={zones[index]}'
    urls.append(url)

responses_dict = {}
for idx, url in enumerate(urls):
    response = requests.get(url)
    responses_dict[f"response_{idx+1}"] = response.json()

# Specify the file path where you want to save the JSON file
import json

file_path = "C:/Users/mrkol/USElecGenerationData/C_intensity_history_data.json"

# Write the dictionary to a JSON file
with open(file_path, 'w') as json_file:
    json.dump(responses_dict, json_file, indent=4)

print("Dictionary successfully exported to JSON file.")

df_carbon_intensity_history = pd.read_json(file_path)


# %%
#request power breakdown
pburls = []
for index, url in enumerate(zones):
    pburl = f'https://api.electricitymap.org/v3/power-breakdown/history?zone={zones[index]}'
    pburls.append(pburl)

power_breakdown_responses_dict = {}
for idx, pburl in enumerate(pburls):
    response = requests.get(pburl)
    power_breakdown_responses_dict[f"response_{idx+1}"] = response.json()

# Specify the file path where you want to save the JSON file

file_path = "C:/Users/mrkol/USElecGenerationData/power_breakdown_history_data.json"

# Write the dictionary to a JSON file
with open(file_path, 'w') as json_file:
    json.dump(power_breakdown_responses_dict, json_file, indent=4)
print("Dictionary successfully exported to JSON file.")
df_power_breakdown_history = pd.read_json(file_path)

# %% [markdown]
# SECTION 2     
# PowerBreakdown data transformation

# %%
# pull data from power breakdown json in dataframe
region = df_power_breakdown_history['response_1']['history'][0]['zone']
datetime = df_power_breakdown_history['response_1']['history'][0]['datetime']
nuclear = df_power_breakdown_history['response_1']['history'][0]["powerConsumptionBreakdown"]['nuclear']
geothermal = df_power_breakdown_history['response_1']['history'][0]["powerConsumptionBreakdown"]['geothermal']
biomass = df_power_breakdown_history['response_1']['history'][0]["powerConsumptionBreakdown"]['biomass']
coal = df_power_breakdown_history['response_1']['history'][0]["powerConsumptionBreakdown"]['coal']
wind = df_power_breakdown_history['response_1']['history'][0]["powerConsumptionBreakdown"]['wind']
solar = df_power_breakdown_history['response_1']['history'][0]["powerConsumptionBreakdown"]['solar']
hydro = df_power_breakdown_history['response_1']['history'][0]["powerConsumptionBreakdown"]['hydro']
gas = df_power_breakdown_history['response_1']['history'][0]["powerConsumptionBreakdown"]['gas']
oil = df_power_breakdown_history['response_1']['history'][0]["powerConsumptionBreakdown"]['oil']
unknown = df_power_breakdown_history['response_1']['history'][0]["powerConsumptionBreakdown"]['unknown']
hydro_discharge = df_power_breakdown_history['response_1']['history'][0]["powerConsumptionBreakdown"]['hydro discharge']
battery_discharge = df_power_breakdown_history['response_1']['history'][0]["powerConsumptionBreakdown"]['battery discharge']
renewable_percentage = df_power_breakdown_history['response_1']['history'][0]["renewablePercentage"]
total_consumption = df_power_breakdown_history['response_1']['history'][0]["powerConsumptionTotal"]
estimated = df_power_breakdown_history['response_1']['history'][0]["isEstimated"]

# create a dictionary with first values for this zone
us_pnm1 = {'region':region,'datetime':datetime,'nuclear':nuclear,'geothermal':geothermal,'biomass':biomass, 'coal':coal, 'wind':wind, 'solar':solar, 
           'hydro':hydro, 'gas':gas, 'oil':oil, 'unknown':unknown, 'hydro-discharge':hydro_discharge, 
           'battery_discharge':battery_discharge, 'renewable_percentage':renewable_percentage, 'total_consumption':total_consumption, 
           'estimated':estimated}

print("Dictionary created.")

# Create a dataFrame with the first values
df_US = pd.DataFrame.from_dict(us_pnm1,orient='index')


# %%
df_US

# %%
# Data wrangling from the response to create a legible dataFrame
# outer for loop for regions/responses
for reg in range(len(zones)):
    #for each zone
    response = f"response_{reg+1}"
   
# pull data from json for each time in this file for this region and add to the existing dataframe
    for i in range(24):
        # 24 is for the 24 hours of data for each zone
        region = df_power_breakdown_history[f"{response}"]['history'][i]['zone']
        datetime = df_power_breakdown_history[f"{response}"]['history'][i]['datetime']
        nuclear = df_power_breakdown_history[f"{response}"]['history'][i]["powerConsumptionBreakdown"]['nuclear']
        geothermal = df_power_breakdown_history[f"{response}"]['history'][i]["powerConsumptionBreakdown"]['geothermal']
        biomass = df_power_breakdown_history[f"{response}"]['history'][i]["powerConsumptionBreakdown"]['biomass']
        coal = df_power_breakdown_history[f"{response}"]['history'][i]["powerConsumptionBreakdown"]['coal']
        wind = df_power_breakdown_history[f"{response}"]['history'][i]["powerConsumptionBreakdown"]['wind']
        solar = df_power_breakdown_history[f"{response}"]['history'][i]["powerConsumptionBreakdown"]['solar']
        hydro = df_power_breakdown_history[f"{response}"]['history'][i]["powerConsumptionBreakdown"]['hydro']
        gas = df_power_breakdown_history[f"{response}"]['history'][i]["powerConsumptionBreakdown"]['gas']
        oil = df_power_breakdown_history[f"{response}"]['history'][i]["powerConsumptionBreakdown"]['oil']
        unknown = df_power_breakdown_history[f"{response}"]['history'][i]["powerConsumptionBreakdown"]['unknown']
        hydro_discharge = df_power_breakdown_history[f"{response}"]['history'][i]["powerConsumptionBreakdown"]['hydro discharge']
        battery_discharge = df_power_breakdown_history[f"{response}"]['history'][i]["powerConsumptionBreakdown"]['battery discharge']
        renewable_percentage = df_power_breakdown_history[f"{response}"]['history'][i]["renewablePercentage"]
        total_consumption = df_power_breakdown_history[f"{response}"]['history'][i]["powerConsumptionTotal"]
        estimated = df_power_breakdown_history[f"{response}"]['history'][i]["isEstimated"]

        # this 24 is also for the 23 hours of data for each zone
        df_US[24*reg+i]= {'region':region, 'datetime':datetime,'nuclear':nuclear,'geothermal':geothermal,'biomass':biomass, 'coal':coal, 'wind':wind, 'solar':solar, 
           'hydro':hydro, 'gas':gas, 'oil':oil, 'unknown':unknown, 'hydro-discharge':hydro_discharge, 
           'battery_discharge':battery_discharge, 'renewable_percentage':renewable_percentage, 'total_consumption':total_consumption, 
           'estimated':estimated}
#set up the times as rows and measurements as columns
print("Dataframe 1 created.")

df_US_new = df_US.transpose()

# check data types
df_US_new.describe()

# %%
# fill NA values with zeroes for energy values
df_US_new = df_US_new.fillna({'nuclear': 0,'geothermal': 0,'biomass': 0, 'coal': 0, 'wind': 0, 'solar': 0, 
           'hydro': 0, 'gas': 0, 'oil': 0, 'unknown': 0, 'hydro-discharge':0, 'renewable_percentage':0,
           'battery_discharge':0, 'total_consumption': 0})
df_US_new.describe()

# %%
# convert measured Energy values to integers in Giga Watts
#convert_dict = {'hydro': int}
convert_dict = {'nuclear': int, 'geothermal': int, 'biomass': int, 'coal': int, 'wind': int, 'solar': int, 'hydro': int, 'gas': int, 'oil': int, 
              'unknown': int, 'hydro-discharge': int, 'battery_discharge': int, 'renewable_percentage': int, 'total_consumption': int
               }
 # note - the unknown column only has values rarely - converting null values to integer doesn't work so this is left as an object
df_US_new = df_US_new.astype(convert_dict)

print("Cleaned dataframe 1.")

#check that data types are changed to int
df_US_new.dtypes

# %%
# Date Time work

# import datetime dependencies

from datetime import datetime

# set up lists to hold parsed data and DateTime as a datetime datetype
dates=[]
times = []
DateTime =[]

# convert date time strings
for i in range(len(df_US_new['datetime'])):

    # Parse the timestamp string to a datetime object
    dt_obj = datetime.strptime(df_US_new.iloc[i,1], '%Y-%m-%dT%H:%M:%S.%fZ')

    date = dt_obj.strftime('%Y-%m-%d')
    time = dt_obj.strftime('%H:%M:%S')

#add the new times and dates to lists

    dates.append(date)
    times.append(time)
    DateTime.append(dt_obj)

# add the times and dates to new columns in the data frame
df_US_new['UTC time'] = times
df_US_new['UTC date'] = dates
df_US_new['UTC DateTime'] = DateTime

# %%
#set the UTC DateTime as the index
df_US_new_reindex = df_US_new.set_index('UTC DateTime', inplace=True)

#drop the datetime column that contains a string
df_US_newer = df_US_new.drop('datetime', axis=1)
df_US_newer.head()

# %% [markdown]
# Section 3
# Transform carbon intensity data

# %%
# pull data from C intensity json in dataframe
region = df_carbon_intensity_history['response_1']['history'][0]['zone']
datetime = df_carbon_intensity_history['response_1']['history'][0]['datetime']
carbon_Intensity = df_carbon_intensity_history['response_1']['history'][0]["carbonIntensity"]
estimated = df_carbon_intensity_history['response_1']['history'][0]["isEstimated"]

# create a dictionary with first values for this zone
us_pnm1C = {'region':region,'datetime':datetime,'Carbon_Intensity':carbon_Intensity, 'estimated':estimated}

# Create a dataFrame with the first values
df_US_C = pd.DataFrame.from_dict(us_pnm1C,orient='index')

# %%
# Data wrangling from the response to create a legible dataFrame for carbon intensity history

# outer for loop for regions/responses
for reg in range(len(zones)):
    response = f"response_{reg+1}"
    
# pull data from json for each time in this file for this region and add to the existing dataframe
    for i in range(24):
        # 24 is for the 24 hours of data for each zone
        region = df_carbon_intensity_history[f"{response}"]['history'][i]['zone']
        datetime = df_carbon_intensity_history[f"{response}"]['history'][i]['datetime']
        carbon_Intensity = df_carbon_intensity_history['response_1']['history'][i]["carbonIntensity"]
        estimated = df_carbon_intensity_history['response_1']['history'][i]["isEstimated"]
        
        # this 24 is also for the 24 hours of data in each zone
        df_US_C[24*reg+i]= {'region':region, 'datetime':datetime,'Carbon_Intensity':carbon_Intensity, 'estimated':estimated}

# make the datetime the rows and carbon_intensity a column
df_US_C_new = df_US_C.transpose()

# check data types
df_US_C_new.dtypes

# %%
# convert carbon intensity measurement to an integer in g CO2e/kWh
convert_dict_C= {'Carbon_Intensity': int}
 
df_US_C_new = df_US_C_new.astype(convert_dict_C)

#check that the datatype has been changed
df_US_C_new.dtypes

# %%
# add the times and dates to new columns in the data frame   -    This assumes the data for carbon intensity is pulled at the same time as power breakdown
df_US_C_new['UTC time'] = times
df_US_C_new['UTC date'] = dates
df_US_C_new['UTC DateTime'] = DateTime

#set the UTC DateTime as the index
df_US_C_new_reindex = df_US_C_new.set_index('UTC DateTime', inplace=True)
#drop the datetime column that contains a string
df_US_C_newer = df_US_C_new.drop('datetime', axis=1)

# %% [markdown]
# Section 4
# Merge dataframes

# %%
df_power_and_carbon= pd.merge(df_US_newer, df_US_C_newer,on=['UTC DateTime','region','UTC time','UTC date'])



df_power_and_carbon.rename(columns={'Carbon_Intensity':'Carbon_Intensity(gCO2eq/kWh)','total_consumption':'total_consumption(GW)', 'nuclear':'nuclear(GW)', 
                                    'geothermal':'geothermal(GW)', 'biomass':'biomass(GW)', 'coal':'coal(GW)', 'wind':'wind(GW)', 'solar':'solar(GW)', 
                                    'hydro':'hydro(GW)','gas':'gas(GW)', 'region_x': 'region', 'estimated_x': 'breakdown estimated?','estimated_y':'intensity estimated?'}, inplace=True)




df_power_and_carbon.head()

# %%
# import previous cleaned file into a pandas dataframe
df_us_energy = pd.read_csv('C:/Users/mrkol/USElecGenerationData/data/runningUSenergy_data.csv')
df_us_energy_reindex=df_us_energy.set_index("UTC DateTime")
df_us_energy_reindex.describe()

# %%
df_us_energy_reindex.drop_duplicates(inplace=True)
df_us_energy_reindex.describe()

# %%
# concatentate current data with existing file
df_both = pd.concat([df_us_energy_reindex,df_power_and_carbon])

# drop duplicate rows
df_both.drop_duplicates(inplace=True)
df_both.describe()

# %%
df_both.to_csv('C:/Users/mrkol/USElecGenerationData/data/runningUSenergy_data.csv')

# %%
df_both_cleaned = df_both.loc[df_both['breakdown estimated?']==False,:]
df_both_cleaned.describe()

# %%
df_both_cleaned.to_csv('C:/Users/mrkol/USElecGenerationData/data/runningUSenergy_data_filtered.csv')


