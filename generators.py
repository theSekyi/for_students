import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

class Generator():
    def __init__(self) -> None:
        self._solar_month_factor = {}
        self._solar_month_factor[1] = 1.0
        self._solar_month_factor[2] = 0.988
        self._solar_month_factor[3] = 0.956
        self._solar_month_factor[4] = 0.914
        self._solar_month_factor[5] = 0.876
        self._solar_month_factor[6] = 0.853
        self._solar_month_factor[7] = 0.853
        self._solar_month_factor[8] = 0.876
        self._solar_month_factor[9] = 0.914
        self._solar_month_factor[10] = 0.956
        self._solar_month_factor[11] = 0.988
        self._solar_month_factor[12] = 1

        self._solar_hour_factor = {}
        for hour in range(24):
            power_factor = np.cos((hour - 12)/24 * 2 * np.pi)
            if power_factor < 0:
                power_factor = 0
            
            self._solar_hour_factor[hour] = power_factor

    def process(self,temperature_c, cloud_cover_frac, wind_speed, rainfall, month, hour):
        return 0

class SolarPower(Generator):
    def __init__(self, units, rated_power_kw, temperature_coefficient, cloud_sensitivity) -> None:
        super().__init__()

        self._units = units
        self._installed_capcity = self._units * rated_power_kw # kW / hour
        self._temperature_coefficient = temperature_coefficient / 100 # percent installed capacity centered around 25C
        self._cloud_sensitivity = cloud_sensitivity # a number between 0 and 2
    
    def process(self,temperature_c, cloud_cover_frac, wind_speed, rainfall, month, hour):
        cloud_factor = (1 - cloud_cover_frac) ** (1 + self._cloud_sensitivity)
        temperature_factor = 1 + (temperature_c - 25) * self._temperature_coefficient

        return self._installed_capcity * cloud_factor * self._solar_hour_factor[hour] * self._solar_month_factor[month] * temperature_factor

class WindTurbine(Generator):
    def __init__(self, units, rated_power_kw, cut_in_speed_kph, peak_speed_kph, cut_out_speed_kph) -> None:
        super().__init__()

        self._units = units
        self._installed_capcity = self._units * rated_power_kw # kW / hour

        cut_in_speed_kph = cut_in_speed_kph # kph
        peak_speed_kph = peak_speed_kph # kph
        cut_out_speed_kph = cut_out_speed_kph # kph

        speed = [0, cut_in_speed_kph, peak_speed_kph, cut_out_speed_kph, cut_out_speed_kph+1, 1000]
        power = [0, 0, self._installed_capcity, self._installed_capcity, 0, 0]
        self._wind_function = interp1d(speed, power, kind='linear', bounds_error=False,fill_value=(0,0))

    def process(self,temperature_c, cloud_cover_frac, wind_speed, rainfall, month, hour):
        return self._wind_function(wind_speed) # kwhr

class HydroTurbine(Generator):
    def __init__(self, units, rated_power_kw, cut_in_flow_m3ph, peak_flow_m3ph) -> None:
        super().__init__()

        self._units = units
        self._installed_capcity = self._units * rated_power_kw # kW / hour

        cut_in_speed = cut_in_flow_m3ph # m3 per hour
        peak_speed = peak_flow_m3ph # m3 per hour

        speed = [0, cut_in_flow_m3ph, peak_flow_m3ph, 1000]
        power = [0, 0, self._installed_capcity, self._installed_capcity]

        self._water_function = interp1d(speed, power, kind='linear',bounds_error=False,fill_value=(0,self._installed_capcity))
        
        self._catchment_area = 15000 * 10000 # m^2
        self._catchment_water = 0
        self._dam_water = 0
        self._water_flow = 0
    
    def process(self,temperature_c, cloud_cover_frac, wind_speed, rainfall, month, hour):
        water_in = self._catchment_area * (rainfall / 1000) # m3 
        self._catchment_water += water_in # m3 

        water_to_dam = self._catchment_water * 0.01
        self._catchment_water -= water_to_dam
        self._dam_water += water_to_dam

        water_to_stream = self._dam_water * 0.05
        self._dam_water -= water_to_stream
        self._water_flow = water_to_stream # m3 per hour


        return self._water_function(self._water_flow) # kwhr
    

