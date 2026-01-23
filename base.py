import numpy as np
import random 
from matplotlib import pyplot as plt
from dataclasses import dataclass

@dataclass  
class STAR_RIS:

    M: int #number of elements in the STAR-RIS
    N: int #number of antennae in the BS

    def __init__(self, M, N):
        self.elements = M
        self.antennae = N
        self.G = np.zeros((M, N))
        self.v_ut = np.zeros((M, 1))
        self.v_ur = np.zeros((M, 1))
        self.PHI_T = np.zeros(M) #transmission coefficients
        self.PHI_R = np.zeros(M) #reflection coefficients
        self.G_nlos = np.zeros((M, N))
        self.G_los = np.ones((M, N))
        self.v_nlos_i = np.zeros((M, 1))
        self.v_los_i = np.ones((M, 1))
        self.p_0_dB: int = -30  #path loss at reference distance 1m (dB)
        self.p_0: float = 10**(self.p_0_dB/10) #conversion to amplitude
        self.d_G: float = 50 #distance between BS and STAR-RIS (m)
        self.a_BR: float = 2.2 #path loss exponent between BS and STAR-RIS
        self.a_RU: float = 2.5 #path loss exponent between STAR-RIS and user
        self.K_BR: float = 10 #Rician factor between BS and STAR-RIS
        self.K_RU: float = 10 #Rician factor between STAR-RIS and user
        self.d_ut: float = 5 #distance between STAR-RIS and user on transmission side (m)
        self.d_ur: float = 10 #distance between STAR-RIS and user on reflection side (m)

def rayleigh_fading(STAR_RIS):
        #print("variance was ", var)
        for i in range(STAR_RIS.elements):
            var = random.uniform(0.5, 10)  #variance of rayleigh distribution
            for j in range(STAR_RIS.antennae):
                STAR_RIS.G_nlos[i,j] = 1 - np.exp(-(j**2)/(2*(var**2))) #defining the channel between each element of the STAR RIS and each antenna of the BS
            # print("j is currently", j)
            # print("answer this time is ", G_nlos[i,j])
        for i in range(STAR_RIS.elements):
            STAR_RIS.v_nlos_i[i,:] = 1 - np.exp((-(i**2)/(2*(var**2)))) #defining the channel between each user and each element       
        # print("i is currently", i)
        
   
def rician_channel(STAR_RIS):
    rayleigh_fading(STAR_RIS)
    STAR_RIS.G = np.sqrt((STAR_RIS.p_0/((STAR_RIS.d_G)**STAR_RIS.a_BR)))*((np.sqrt((STAR_RIS.K_BR/(1+STAR_RIS.K_BR)))*STAR_RIS.G_los)+(np.sqrt((1/(1+STAR_RIS.K_BR)))*STAR_RIS.G_nlos))
    STAR_RIS.v_ut = np.sqrt((STAR_RIS.p_0/((STAR_RIS.d_ut)**STAR_RIS.a_RU)))*(((np.sqrt((STAR_RIS.K_RU/(1+STAR_RIS.K_RU))))*STAR_RIS.v_los_i)+(np.sqrt((1/(1+STAR_RIS.K_RU)))*STAR_RIS.v_nlos_i))
    STAR_RIS.v_ur = np.sqrt((STAR_RIS.p_0/((STAR_RIS.d_ur)**STAR_RIS.a_RU)))*((np.sqrt((STAR_RIS.K_RU/(1+STAR_RIS.K_RU)))*STAR_RIS.v_los_i)+(np.sqrt((1/(1+STAR_RIS.K_RU)))*STAR_RIS.v_nlos_i))

 


def main():
    #print("Hello Maks")
    instance = STAR_RIS(30, 10)
    rician_channel(instance)
    print("G is defined as" , instance.G)
    print("\nv_ut is defined as" , instance.v_ut)
    print("\nv_ur is defined as" , instance.v_ur)


print("Hello Melvin")
if __name__ == "__main__":
    main()
