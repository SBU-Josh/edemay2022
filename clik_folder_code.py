import numpy as np
import os

#Define parameters of interest
blowup = 1e6
cut_ell = 650
label = 'plik_lite_v22_TT650TEEE'
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

#Delete any previous .clik folder tat exists with the same name
os.system('rm -r '+path+label+'.clik')

#Create a copy of .clik folder to place the modified covariance matrix into
copy_clik = 'cp -R '+path+'plik_lite_v22_TTTEEE_copy.clik/ '+path+label+'.clik'
os.system(copy_clik)

#Import the covariance matrix to modify
dt=np.dtype([('header', np.int32, (1,)), ('cov', np.float64, (375769))])
temp = np.fromfile(path+label+'.clik/'+'clik/lkl_0/_external/c_matrix_plik_v22.dat', dtype=dt, count=1)
#print(temp['cov'].copy())
pliklite_cov = temp['cov'].copy().reshape(613,613)
duplicate = temp['cov'].copy().reshape(613,613)
#print(blowup*pliklite_cov[75:215,:])


#Define the cutoff bin to affect
bin_min = np.genfromtxt(path+label+'.clik/'+'clik/lkl_0/_external/blmin.dat')
cut_bin = np.argmin(np.abs(bin_min[:215] + 30 - cut_ell))
print(cut_bin)

#Blow up the error on elements that you do not want to contribute
pliklite_cov[cut_bin:215,:] *= blowup
pliklite_cov[:,cut_bin:215] *= blowup

#Symmetrize covariance
#i = 0
#for i in range(613):
#    j = 0
#    for j in range(j < i):
#        pliklite_cov[j,i] = pliklite_cov[i,j]
#        duplicate[j,i] = duplicate[i,j]

#Testing
#inv = np.linalg.inv(pliklite_cov)
#arr1 = np.ones(613)
#arr2 = arr1.copy()
#arr2[cut_bin:215] *= 0.5
#diff = arr1 - arr2
#print(np.dot(diff,np.dot(inv,diff)))
#print(np.sqrt(np.diagonal(duplicate[:215,:215])))

#Put the new covariance matrix back into the c_matrix_plik_v22.dat file
temp['cov'] = pliklite_cov.reshape(1,375769)
temp.tofile(path+label+'.clik/'+'clik/lkl_0/_external/c_matrix_plik_v22.dat')
