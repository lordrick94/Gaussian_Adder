import numpy as np
from astropy.modeling.models import Gaussian2D as g2d, Gaussian1D as g1d


def Gaussian_Generator(t_x,t_y,t_z,x_m,y_m,z_m,b_x,b_y,b_z,amp,bpa):
    z,y,x = np.ogrid[0:t_z,0:t_y,0:t_x]
    g_2 = g2d(amplitude=amp, x_mean=x_m, y_mean=y_m, x_stddev=b_x, y_stddev=b_y, theta=bpa) # Generating 2d gaussian psf
    g_xy = g_2(x,y)
    g_1 = g1d(amplitude=1, mean=z_m, stddev=b_z) # generating 1d gaussian in the spectral direction
    g_z = g_1(z)
    gs = g_xy*g_z
    return gs