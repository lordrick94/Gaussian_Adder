"""
This Code can be Used to add fake sources to a Data Cube
This is the First Draft therefore Still many Bugs to Fix

But it Runs, Yay!!!!!!!
"""


# Importing Libraries
import numpy as np
from astropy.io import fits
from astropy.coordinates import Angle
from astropy import units as u
import pandas as pd

# Importing source 
from gaus_generator import Gaussian_Generator

#Loading Fits File
filename = input('Enter the File Name:')
hdul = fits.open(filename)
hdr = hdul[0].header                        #Header
data = hdul[0].data[0]                      #Data

#Taking shape of data_cube
sh = data.shape
t_x,t_y,t_z = sh[1],sh[2],sh[0]


#Calculating Beam to Pixel Ratio
cdel_1 = Angle(hdr['CDELT1'],u.degree)      #pixel increment from header
dmaj = Angle(hdr['BMAJ'],u.degree)          #BMAJ FWHM from header

c_1 = np.abs(cdel_1.arcsec)
d_1= dmaj.arcsec

cdel_2 = Angle(hdr['CDELT2'],u.degree)      #pixel increment from header
dmIN = Angle(hdr['BMIN'],u.degree)          #BMIN FWHM from header

c_2 = np.abs(cdel_1.arcsec)
d_2 = dmIN.arcsec

b_x = int(d_1/c_1);b_y = int(d_2/c_2)

v = hdr['BPA']/70139.80849035224
bpa = Angle(v,u.radian)

# Number of Spanning Channells
r = input('Enter the Number Channels to Span: ')
b_z = int(r)

#Number of sources to be added
n  = input('Enter the Number of Sources: ')
ns  = int(n)

#Genrating source positions and Amplitudes
a = 2*np.max(data)
Amp = np.random.uniform(a,a/4,ns)
s_x = np.random.randint(0,t_x,ns)
s_y = np.random.randint(0,t_y,ns)
s_z = np.random.randint(0,t_z,ns)

df = pd.DataFrame(list(zip(s_x, s_y, s_z, Amp)),columns =['x_mean', 'y_mean', 'z_mean', 'Amplitude'])
df.to_csv('source_data.csv')
print(df)

#Adding the Sources to data_cube
for (x_m, y_m, z_m, amp) in zip(s_x, s_y, s_z, Amp):
    gs = Gaussian_Generator(t_x,t_y,t_z,x_m,y_m,z_m,b_x,b_y,b_z,amp,bpa)
    hdul[0].data[0] = hdul[0].data[0]+gs

#Saving to new fits file
hdul.writeto('sources + '+filename,overwrite=True)

print('{} sources have been added to the {} data cube'.format(n,filename))