import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from generators import SolarPower
from generators import WindTurbine
from generators import HydroTurbine
from storage import Storage

# TODO: Write a function that will fetch the weather data from the database or a local source
# I have included this simple data source just to illustrate how the simulation works
##############################################
weather_data = pd.read_csv("example_data.csv")
##############################################

generator_list = []
storage_list = []

# TODO: Fill in the parameters of the generators and storage that you have selected. 
# You will get the required parameters from the catalogues provided.
# Make sure that you do not exceed your budget. You will need to check this manually.

generator_list.append(
    SolarPower(units=1, 
    rated_power_kw=200, 
    temperature_coefficient=-0.40, 
    cloud_sensitivity=2.00))

generator_list.append(
    WindTurbine(units=0, 
    rated_power_kw=0, 
    cut_in_speed_kph=0, 
    peak_speed_kph=0, 
    cut_out_speed_kph=0))

generator_list.append(
    HydroTurbine(units=0, 
    rated_power_kw=0, 
    cut_in_flow_m3ph=0,
    peak_flow_m3ph=0))

storage_list.append(
    Storage(units=1, 
    kwhr_capacity=400,
    max_charge_power_kw=100,
    max_discharge_power_kw=100,
    charge_efficiency_percent=95))

# Used for plotting graphs
dt_list = []
energy_generated_list = []
supplied_list = []

# Used to calculate performance metrics
total_energy = 0
total_hours = 0
supplied_hours = 0

# TODO: For the challenge this will need to be 50e3
constant_power_demand = 50 # kW per hour

for index, row in weather_data.iterrows():
    # Extract the data from the dataframe
    dt = pd.to_datetime(row['timestamp'])
    temperature = row['temperature']
    wind_speed = row['wind_speed']
    cloud_cover = row['cloud_cover'] / 100
    rainfall = row['precipitation']

    hour = dt.hour
    month = dt.month
    energy_generated = 0

    # Iterate through each generator and get the amount of energy generated from each
    for generator_unit in generator_list:
        p = generator_unit.process(temperature_c = temperature,
            cloud_cover_frac = cloud_cover,
            wind_speed = wind_speed,
            rainfall = rainfall,
            month = month,
            hour = hour)

        energy_generated += p

    # Calculate the amount of exccess energy after the demand has been subtracted.
    # If the energy excess is positive this will be used to charge the energy storage devices.
    # If the energy excess is negative the energy storage will try supply the shortfall (if energy available)
    energy_excess = energy_generated - constant_power_demand

    for storage_unit in storage_list:
        energy_excess = storage_unit.process(energy_excess)
    
    # If there is no or some excess energy then you were able to supply the demand, otherwise you were not able to meet demand.
    if energy_excess >= 0:
        supplied_hours += 1
        supplied_list.append(1)
    else:
        supplied_list.append(0)

    # Add data for graphs
    dt_list.append(dt)
    energy_generated_list.append(energy_generated)

    total_energy += energy_generated
    total_hours += 1

print("Average Energy [kWhr]:", total_energy / total_hours)
print("Supplied Hours [%]:", supplied_hours / total_hours * 100)

plt.plot(dt_list, energy_generated_list, label='Energy Generated')
plt.plot(dt_list, np.array(supplied_list) * np.max(energy_generated_list), label='Supply Met')
plt.title("Total Energy Supplied Per Hour")
plt.ylabel("KwHr")
plt.xticks(rotation=60)
plt.legend()
plt.grid()
plt.show()