from comyx.network import (
    UserEquipment,
    BaseStation,
    STAR_RIS,
    Link,
    cascaded_channel_gain,
)

from comyx.propagation import get_noise_power
from comyx.utils import dbm2pow, get_distance, generate_seed, db2pow

import numpy as np
from matplotlib import pyplot as plt

CRt = 0 #Achievable communication rate for User on transmitter side
CRr = 0 #Achievable communication rate for User on reflector side
Pmax = 20 #insert max value (dBm)
Pt = np.linspace(0, Pmax, 1) # dBm
Pt_lin = dbm2pow(Pt) # Watt
Bw = 180e3 #Bandwidth (Hz)
mc = 32 #Number of channel realizations
K = 10 #Rician factors
fc = 2.4e9 #carrier frequency
temperature = 300 # Kelvin

N0 = -80 #power of AWGN (dBm)

M = 4 #number of antenna at the BS
N = 30 #number of  STAR-RIS elements

los_fading = {"type": "rayleigh", "sigma": 1 / 2} #G(n)LoS & h(n)LoS componenets both follow Rayleigh fading

br_pathloss_args = {"type": "reference", "alpha": 2.2, "p0": -30, "frequency": fc}
ru_pathloss_args = {"type": "reference", "alpha": 2.5, "p0": -30, "frequency": fc}

BS = BaseStation("BS", position = [0, 0, 0], n_antennas = M, t_power = Pt_lin)
SR = STAR_RIS("SR", position = [30, 40, 0], n_elements = N)

shape_starris = (N)

#SR.reflection_phases = np.zeros(N) #initialise reflection phase shifts
#SR.reflection_amplitudes = np.ones(N) #initialise reflection amplitudes
#SR.reflection_amplitudes.fill(0.5)

#SR.transmission_phases = np.zeros(N) #initialise transmission phase shifts
#SR.transmission_amplitudes = np.ones(N) #initialise transmission amplitudes
#SR.transmission_amplitudes.fill(0.5)


UER = UserEquipment("UE1", position = [34, 37, 0], n_antennas = 1)
UET = UserEquipment("UE2", position = [38, 46, 0], n_antennas = 1)

# Shapes for channels
shape_br = (N, M)
shape_ru = (N, 1)

# Links

link_bs_starris = Link(
    BS, SR,
    los_fading, br_pathloss_args,
    shape = shape_br, seed = generate_seed("STAR_RIS-BS")
)

link_starris_uer = Link(
    SR, UER,
    los_fading, br_pathloss_args,
    shape = shape_ru, seed = generate_seed("STAR_RIS-UE1"),
    rician_args = {"K": db2pow(K), "order":"pre"} 
)


link_starris_uet = Link(
    SR, UET,
    los_fading, br_pathloss_args,
   shape = shape_ru, seed = generate_seed("STAR_RIS-UE1"),
    rician_args = {"K": db2pow(K), "order":"pre"} 
)

#channel_gain_UER = cascaded_channel_gain(link_bs_starris, link_starris_uer, style = "matrix")
#channel_gain_UET = cascaded_channel_gain(link_bs_starris, link_starris_uet, style = "matrix")