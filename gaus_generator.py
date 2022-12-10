import numpy as np
def gaussian_source(data,t_x,t_y,r):
    mu_x = t_x/2
    mu_y = t_y/2
    mu_z = r/2
    b_x = t_x/300
    b_y = t_y/200                               # b values need work
    b_z = r/640
    x,y,z = np.meshgrid(np.linspace(0,t_x,int(t_x)),np.linspace(0,t_y,int(t_y)),np.linspace(0,r,r))
    Amp = 4*np.max(data)
    gs = Amp*np.exp(-(((x-mu_x)**2)/2*b_x**2+((y-mu_y)**2)/2*b_y**2)+((z-mu_z)**2/2*b_z**2))
    gs = np.transpose(gs,(2,1,0))
    x_l = gs.shape[1]
    y_l = gs.shape[2]
    return gs,x_l,y_l,mu_z