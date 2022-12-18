#Code to add Beam Size and Area to header files in ALMA Data Cubes

#Importing Libraries
from astropy.io import fits
import pandas as pd
from astropy.coordinates import Angle as Ang

#Opening fits file
file = input('Please enter file name and Path here:')
hdul = fits.open(file)

hdr = hdul[0]   #accesing Primary extension

bm = hdul[1].data # accessing beam data from BinTable Extension


# Creating a DataFrame for Calculation
data = pd.DataFrame(bm, columns=['BMAJ','BMIN','BPA','CHAN','POL'])

#Appending header with Beam Info
hdr.header['BMAJ'] = data['BMAJ'].median()* 2.7777756825297936e-05*10
hdr.header['BMIN'] = data['BMIN'].median()* 2.7777756825297936e-05*10

BPA = str(data['BPA'].median()) + 'd'
BPA = Ang(BPA)
hdr.header['BPA'] = BPA.radian * 70139.80849035224

# Creating New Fits file with Beam info in the Header
hdul.writeto('edited_'+file,overwrite=True)

print('The file has been updated to contain Beam Information')