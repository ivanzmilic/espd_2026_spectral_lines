import numpy as np
import os, sys
import matplotlib.pyplot as plt
from tqdm import tqdm
from astropy.io import fits
from glob import glob

# ====================================================================
def avg2D(data,nbin):
	"""
        Rebin a 2D array into `nbin` bins by averaging
        Parameters
        ----------
        data : ndarray
            a 2D array
        nbin : int
            number of bins

        Returns
        -------
        rebin : ndarray
            rebinned 2D array
        Example
        -------
        >>> databin = avg2D(data, 10)
        :Author:
            Rahul Yadav (ISP/SU 2019)
        """

	nx,ny = data.shape
	npx = int(nx/nbin)
	npy = int(ny/nbin)
	rebin = np.zeros((npx, npy),dtype = np.float64)
	if (nbin/nx > 1):
		print('Error: Bin size > the array size!')
	else:
		for i in range(npx):
			for j in range(npy):
				rebin[i,j] = np.mean(data[i*nbin:i*nbin+nbin,j*nbin:j*nbin+nbin])

	return rebin


# ====================================================================
# Let's read the data:
glob_list = glob('*.xb1.yb1.*.fits')

for datai in tqdm(glob_list):
    data = fits.getdata(datai)
    header = fits.getheader(datai)
    # ====================================================================
    # Let's bin the data:
    bin_factor = 2
    bin_data = np.empty((int(data.shape[0]/bin_factor),data.shape[1],data.shape[2],int(data.shape[3]/bin_factor)),dtype=np.float32)
    for ww in tqdm(range(data.shape[2])):
        for ss in tqdm(range(data.shape[1]),leave=False):
            bin_data[:,ss,ww,:] = avg2D(data[:,ss,ww,:],bin_factor)
    # ====================================================================
    # Let's write the data:
    fits.writeto(datai.replace('.xb1.yb1.','.xb2.yb2.'),bin_data,header,overwrite=True)