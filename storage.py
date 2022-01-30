import matplotlib.pyplot as plt
import numpy as np

class Storage():
    def __init__(self, units, kwhr_capacity, max_charge_power_kw, max_discharge_power_kw, charge_efficiency_percent) -> None:
        #
        '''
        The simulation runs in 1 hour timesteps, hence all energy/power values
        are in kwhr
        '''
        self._kwhr_capacity = kwhr_capacity * units
        self._max_charge_energy = max_charge_power_kw * units
        self._max_discharge_energy = max_discharge_power_kw * units
        self._charge_efficiency = charge_efficiency_percent / 100
        self._kwhr_stored = 0

    def get_energy_stored(self):
        return self._kwhr_stored

    def process(self, energy_in):
        '''
        if energy_in is positive it will charge the battery, if negative the battery
        will try to supply this amount of energy
        '''
        if energy_in > 0:
            excess_energy = energy_in

            # Limit the charging to the battery's maximum rate
            if energy_in > self._max_charge_energy:
                energy_in = self._max_charge_energy
            
            # Do not take more energy than what is needed to charge the battery
            kwhr_stored_deficit = self._kwhr_capacity - self._kwhr_stored
            if energy_in * self._charge_efficiency > kwhr_stored_deficit:
                energy_in = kwhr_stored_deficit / self._charge_efficiency
            
            # Charge the battery and calculate any excess
            self._kwhr_stored += energy_in * self._charge_efficiency
            excess_energy = excess_energy - energy_in
        
        else:
            excess_energy = energy_in
            energy_out = -energy_in

            # Limit the discharge to the battery's maximum rate
            if energy_out > self._max_discharge_energy:
                energy_out = self._max_discharge_energy
            
            # Do not supply more energy than is available in the battery
            if energy_out > self._kwhr_stored:
                energy_out = self._kwhr_stored
            
            self._kwhr_stored -= energy_out
            excess_energy = excess_energy + energy_out
            
        return excess_energy
