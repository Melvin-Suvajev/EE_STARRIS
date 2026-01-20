'''
from comyx.network import (
    UserEquipment,
    BaseStation,
    STAR_RIS, RIS,
    Link,
    cascaded_channel_gain,
)

from comyx.propagation import get_noise_power
from comyx.utils import dbm2pow, get_distance, generate_seed, db2pow

import numpy as np
from numba import jit


CRt = 0 #Achievable communication rate for User on transmitter side
CRr = 0 #Achievable communication rate for User on reflector side
EE_t = np.zeros(20)
EE_r = np.zeros(20)
Pmax = 20 #insert max value (dBm)
Pt = np.linspace(0, Pmax, 20) # dBm
Pt_lin = dbm2pow(Pt) # Watt
Bw = 180e3 #Bandwidth (Hz)
mc = 32 #Number of channel realizations
K = 10 #Rician factors
fc = 2.4e9 #carrier frequency
temperature = 300 # Kelvin

N0 = -80 #power of AWGN (dBm)
N0_lin = dbm2pow(N0)

N = 4 #number of antenna at the BS
M = 30 #number of  STAR-RIS elements

los_fading = {"type": "rayleigh", "sigma": 1 / 2} #G(n)LoS & h(n)LoS componenets both follow Rayleigh fading

br_pathloss_args = {"type": "reference", "alpha": 2.2, "p0": -30, "frequency": fc}
ru_pathloss_args = {"type": "reference", "alpha": 2.5, "p0": -30, "frequency": fc}

BS = BaseStation("BS", position = [0, 0, 0], n_antennas = M, t_power = Pt_lin)
STr = RIS("STr", position = [30, 40, 0], n_elements = N)
STt = RIS("STt", position = [30, 40, 0], n_elements = N)

shape_starris = (N)

STr.phase_shifts = np.zeros(N)
STr.amplitudes = np.ones(N)
STr.amplitudes.fill(0.5)
#SR.reflection_phases = np.zeros(N) #initialise reflection phase shifts
#SR.reflection_amplitudes = np.ones(N) #initialise reflection amplitudes
#SR.reflection_amplitudes.fill(0.5)
STt.phase_shifts = np.zeros(N)
STt.amplitudes = np.ones(N)
STt.amplitudes.fill(0.5)
#SR.transmission_phases = np.zeros(N) #initialise transmission phase shifts
#SR.transmission_amplitudes = np.ones(N) #initialise transmission amplitudes
#SR.transmission_amplitudes.fill(0.5)


UER = UserEquipment("UE1", position = [34, 37, 0], n_antennas = 1)
UET = UserEquipment("UE2", position = [38, 46, 0], n_antennas = 1)

# Shapes for channels
shape_br = (N, M)
shape_ru = (N, M)

# Links

link_bs_starris_r = Link(
    BS, STr,
    los_fading, br_pathloss_args,
    shape = shape_br, seed = generate_seed("STAR_RIS-BS")
)

link_bs_starris_t = Link(
    BS, STt,
    los_fading, br_pathloss_args,
    shape = shape_br, seed = generate_seed("STAR_RIS-BS")
)


link_starris_uer = Link(
    STr, UER,
    los_fading, br_pathloss_args,
    shape = shape_ru, seed = generate_seed("STAR_RIS-UE1"),
    rician_args = {"K": db2pow(K), "order":"pre"} 
)


link_starris_uet = Link(
    STt, UET,
    los_fading, br_pathloss_args,
   shape = shape_ru, seed = generate_seed("STAR_RIS-UE1"),
    rician_args = {"K": db2pow(K), "order":"pre"} 
)

channel_gain_UER = cascaded_channel_gain(link_bs_starris_r, link_starris_uer, style = "matrix")
#assert channel_gain_UER.shape == link_starris_uer, "Shapes do not match"
channel_gain_UET = cascaded_channel_gain(link_bs_starris_t, link_starris_uet, style = "matrix")
#assert channel_gain_UET.shape == link_starris_uet, "Shapes do not match"

#Magnitude of channel gains
mag_UER = np.abs(channel_gain_UER) ** 2
mag_UET = np.abs(channel_gain_UET) ** 2

print("power of basestation is" , BS.t_power)


CRr = np.log2(1 +  mag_UER/(mag_UER+N0_lin))

#print("achievable comms rate of reflection is", CRr)

CRt = np.log2(1 +  mag_UET/(mag_UET+N0_lin))

for i in range(20):
    p = BS.t_power[i]
    total_com = sum(CRt)
    total_com = sum(total_com)
    EE_t[i] = (Bw * total_com) / p

for i in range(20):
    p = BS.t_power[i]
    total_com = sum(CRr)
    total_com = sum(total_com)
    EE_r[i] = (Bw * total_com) / p



plt.plot(Pt, EE_r)
plt.xlabel("Transmit power (dBm)")
plt.ylabel("Energy efficiency (kBits/Joule)")
plt.savefig("testgraph", dpi = 300, bbox_inches = "tight")


print("energy efficiency of transmission is " , EE_t)
print("energy efficiency of reflection is " , EE_r)


'''


#attempt to rebuild without comyx library
import numpy as np
from matplotlib import pyplot as plt

M = 30 #number of elements in the STAR-RIS
N = 10 #number of antennae in the BS
P_c = 40 #total power comsumption (dBm)

G = np.zeros((M,N))
v_ut = np.zeros((1, M))
v_ur = np.zeros((1, M))

PHI_T = np.zeros(M) #transmission coefficients
PHI_R = np.zeros(M) #reflection coefficients

#print("this is the G matrix", G)
#print("and this is the v matrix", v_ut)