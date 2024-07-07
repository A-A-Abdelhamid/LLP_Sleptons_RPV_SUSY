import numpy as np
import shutil

f = open("input.txt", "w")

mass_start = float(input("Enter the minimum particle mass in GeV: "))
mass_end = float(input("Enter the maximum particle mass in GeV: "))
mass_increment = float(input("Enter the mass step size in GeV: "))
num_masses = int( ( (mass_end - mass_start) / mass_increment ) + 1 )

tau_start = float(input("Enter the minimum particle lifetime in ns: "))
tau_end = float(input("Enter the maximum particle lifetime in ns: "))
tau_increment = float(input("Enter the lifetime step size in ns: "))
num_taus = int( ( (tau_end - tau_start) / tau_increment ) + 1 )

print("Creating input card...")

for mass in np.linspace(mass_start, mass_end, num_masses):
    for tau in np.linspace(tau_start, tau_end, num_taus):
        f.write( str(mass) + " " + str(tau) + "\n")

f.close()
shutil.move("input.txt","submission/input.txt")

print("Input card 'input.txt' created and moved to the submission directory.")
