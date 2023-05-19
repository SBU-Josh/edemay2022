import numpy as np
import os

#Define parameters of interest
blowup = 1e6
cut_ell = 650
label = 'plik_lite_v22_TT650'
path = './external_modules/data/planck/plc_3.0/hi_l/plik_lite/'

#For Cosmomc only
#Create batch .ini file that correctly points to the clik folder
#copy_batch3 = 'cp batch3/plik_lite_TTTEEE.ini batch3/'+label+'.ini'
#os.system(copy_batch3)
#f = open('batch3/'+label+'.ini','r')
#list_of_lines = f.readlines()
#list_of_lines[3] = 'clik_data_plikLite  = %DATASETDIR%clik_14.0/hi_l/plik_lite/'+label+'.clik \n'
#f = open('batch3/'+label+'.ini','w')
#f.writelines(list_of_lines)
#f.close()

#Create a copy of .clik folder to place the modified covariance matrix into
copy_clik = 'cp -R '+path+'plik_lite_v22_TT.clik/ '+path+label+'.clik'
#print(copy_clik)
os.system(copy_clik)
#print('done')

#Import the covariance matrix to modify
dt=np.dtype([('header', np.int32, (1,)), ('cov', np.float64, (375769))])
temp = np.fromfile(path+label+'.clik/'+'clik/lkl_0/_external/c_matrix_plik_v22.dat', dtype=dt, count=1)
#print(temp['cov'].copy())
pliklite_cov = temp['cov'].copy().reshape(613,613)
#print(blowup*pliklite_cov[75:215,:])


#Define the cutoff bin to affect
bin_min = np.genfromtxt(path+label+'.clik/'+'clik/lkl_0/_external/blmin.dat')
cut_bin = np.argmin(np.abs(bin_min[:215] + 30 - cut_ell))
print(cut_bin)

#Blow up the error on elements that you do not want to contribute
pliklite_cov[cut_bin:215,:] *= blowup
pliklite_cov[:,cut_bin:215] *= blowup

#Put the new covariance matrix back into the c_matrix_plik_v22.dat file
temp['cov'] = pliklite_cov.reshape(1,375769)
temp.tofile(path+label+'.clik/'+'clik/lkl_0/_external/c_matrix_plik_v22.dat')
