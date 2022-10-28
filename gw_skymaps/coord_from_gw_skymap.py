#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  6 11:44:18 2019

@author: deepake
"""




from ligo.skymap.io import fits
from ligo.skymap import postprocess
import numpy as np
import healpy as hp
from astropy.table import Table
from astropy.io import ascii
import matplotlib.pyplot as plt

'''
## Program to effectively create RA, Dec coordinates from a given GW map
##-------------------------------------------------------------------
##--------------------------------------------------------------------
'''

out = Table()
tab = Table()
fin = Table()


## Reading the GW fits file,getting the nside and  healpix numbering
## and calculating probability of each healpixel
#-------------------------------------------------------------------
skymap, metadata = fits.read_sky_map('GW190814_skymap.fits.gz', nest=None)
ns= hp.pixelfunc.get_nside(skymap)
print(ns)
out['hp'] = np.arange(hp.nside2npix(ns))
out['prob'] = 100 * postprocess.find_greedy_credible_levels(skymap)



x = int(input("the probability region needed: "))
tab = out[out['prob']< x]


## converting healpixel to ra, dec 
#-------------------------------------------------------------------
theta, phi = hp.pix2ang(ns,tab['hp'],nest='True')
tab['ra'] = np.rad2deg(phi)
tab['dec'] = np.rad2deg(0.5 * np.pi - theta)


#plt.scatter(tab['ra'],tab['dec'])
#print(tab)

nside = int(input("nside that you needed: "))


## converting each ra,dec to healpix of corresponding nside!
#-------------------------------------------------------------------
fin['hp']= hp.pixelfunc.ang2pix(nside, theta, phi, nest=True, lonlat=False)

#print(fin['hp'])

## again converting the healpixel to ra dec- for the user given nside
#-------------------------------------------------------------------
theta0, phi0 = hp.pix2ang(nside,fin['hp'],nest='True')
fin['ra'] = np.rad2deg(phi0)
fin['dec'] = np.rad2deg(0.5 * np.pi - theta0)


print(fin)
plt.figure()
plt.scatter(fin['ra'],fin['dec'])
plt.xlabel('RA (deg)')
plt.ylabel('Dec (deg)')
plt.show()

### Edit this line
ascii.write([fin['hp'],fin['ra'],fin['dec']], 'S190814bv-90probtest.csv', format='csv', fast_writer=False,  overwrite =True)  

