"""
This Code can be Used to add fake sources to a Data Cube
This is the First Draft therefore Still many Bugs to Fix
Known Bugs:
    1. Defining the Std of the Gaussians in all 3 dimensions
    2. The Sources are identical
    3. When Sources are defined out of Range
    4. Defining Positions in WCS

But it Runs, Yay!!!!!!!
"""


# Importing Libraries
import numpy as np
from astropy.io import fits
from astropy.coordinates import Angle
from astropy import units as u

# Importing Source Generator
from gaus_generator import gaussian_source


#Loading Fits File
filename = input('Enter the File Name:')
hdul = fits.open(filename)
hdr = hdul[0].header                        #Header
data = hdul[0].data[0]                      #Data


#Calculating Beam to Pixel Ratio
cdel_1 = Angle(hdr['CDELT1'],u.degree)      #pixel increment from header
dmaj = Angle(hdr['BMAJ'],u.degree)          #BMAJ FWHM from header

c_1 = np.abs(cdel_1.arcsec)
d_1= dmaj.arcsec

cdel_2 = Angle(hdr['CDELT2'],u.degree)      #pixel increment from header
dmIN = Angle(hdr['BMIN'],u.degree)          #BMIN FWHM from header

c_2 = np.abs(cdel_1.arcsec)
d_2 = dmIN.arcsec

t_x = d_1/c_1;t_y = d_2/c_2

# Number of Spanning Channells
r = input('Enter the Number Channels to Span: ')
r = int(r)

#Generating 3D Gaussian Source
gs,x_l,y_l,mu_z = gaussian_source(data,t_x,t_y,r)

# Entering the Number of Sources and their positions
ns = input('Enter the Number of Sources:')
ns = int(ns)
sources = []
for i in range(ns):
    x_1 = input('Enter x value of Source {}: '.format(i+1))
    y_1 = input('Enter y value of Source {}: '.format(i+1))
    z_1 = input('Enter z value of Source {}: '.format(i+1))
    x_1 = float(x_1)
    y_1 = float(y_1)
    z_1 = float(z_1)
    pos = (x_1,y_1,z_1)
    sources.append(pos)

#Adding sources to the Cube
for source in sources:
    x,y,z = source
    y_1 = int(y)
    y_2 = int(y+y_l)
    x_1 = int(x)
    x_2 = int(x+x_l)
    z_1 = int(z-mu_z)
    z_2 = int(z+mu_z)
    arr = data[z_1:z_2,x_1:x_2,y_1:y_2]
    arr+=gs


hdul.writeto('sources_'+filename,overwrite=True)

