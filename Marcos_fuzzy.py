#!/usr/bin/env python
# coding: utf-8

import pandas as pd

# read initial matrix file
imatrix = pd.read_csv("Matrix.csv")

# STEP 1
imatrix.set_index('Unnamed: 0', inplace=True)
print(imatrix)

# STEP 2

B = ['C11', 'C14']
C = ['C12', 'C13', 'C15', 'C16', 'C17', 'C21', 'C22', 'C23',
     'C24', 'C25', 'C26', 'C27', 'C31', 'C32', 'C33', 'C34', 'C35', 'C36',
     'C37']

# Formation of Extended Matrix

imatrix.loc['AAI'] = 0
for x in imatrix.columns:
    if x in B:
        imatrix[x]['AAI'] = imatrix[x].max()
    else:
        imatrix[x]['AAI'] = imatrix.drop('AAI')[x].min()

imatrix.loc['AI'] = 0
for x in imatrix.columns:
    if x in B:
        imatrix[x]['AI'] = imatrix.drop('AI')[x].min()
    else:
        imatrix[x]['AI'] = imatrix[x].max()


print(imatrix)


# STEP 3 Formation of Normalised Matrix

for x in imatrix.columns:
    if x in B:
        imatrix[x] = imatrix[x]['AI'] / imatrix[x]
    else:
        imatrix[x] = imatrix[x] / imatrix[x]['AI']


print(imatrix)

# #read weighted matrix( Economic, Social Environmental )

ematrix = pd.read_csv('environment.csv')
ematrix.set_index('DM', inplace=True)
print(ematrix)


ecomatrix = pd.read_csv('economic.csv')
ecomatrix.set_index('DM', inplace=True)
print(ecomatrix)


smatrix = pd.read_csv('social.csv')
smatrix.set_index('DM', inplace=True)
print(smatrix)


k1 = 0.592
k2 = 0.240
k3 = 0.168


# Calculation of Weighted Coefficient

weight_coff_eco = k1 * ecomatrix.loc['Mean']
weight_coff_e = k3 * ematrix.loc['Mean']
weight_coff_s = k2 * smatrix.loc['Mean']


weight_coff = weight_coff_eco
weight_coff = weight_coff.append(weight_coff_s)
weight_coff = weight_coff.append(weight_coff_e)


# STEP 4 Formation of weighted normalised matrix

weight_nor_imatrix = pd.DataFrame()
for x in imatrix.columns:
    weight_nor_imatrix[x] = imatrix[x] * weight_coff[x]

print(weight_nor_imatrix)

# STEP 5 AND 6, Calculation of utility degree and utility function values of each alternatives

Z = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8']

utility_func_values = []
Sai = sum(imatrix.loc['AI'])
Saai = sum(imatrix.loc['AAI'])
for x in range(len(Z)):
    k1 = sum(imatrix.iloc[x]) / Saai
    k2 = sum(imatrix.iloc[x]) / Sai
    f_k1 = k1 / (k1 + k2)
    f_k2 = k2 / (k1 + k2)
    f_k = (k1 + k2) / (1 + ((1 - f_k2) / f_k2) + ((1 - f_k1) / f_k1))
    utility_func_values.append(f_k)

print(utility_func_values)

