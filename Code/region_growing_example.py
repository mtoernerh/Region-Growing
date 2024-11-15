# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 10:52:40 2024

@author: mfth
"""
import os
import sys
import numpy as np

current_dir = os.path.dirname(os.path.abspath(__file__))
code_dir = os.path.join(current_dir, 'Code')
data_dir = os.path.join(current_dir, 'Data')
out_dir  = os.path.join(current_dir, 'Output')
sys.path.append(code_dir)

from region_growing import region_growing 

mean_array = np.load(os.path.join(data_dir, 'mean_array.npy'))
std_array = np.load(os.path.join(data_dir, 'std_array.npy'))

# Find the indices (coordinates) where std_array is non-NaN
seeds = np.argwhere(~np.isnan(std_array))

# Get the corresponding values for each coordinate 
seed_values = std_array[seeds[:, 0], seeds[:, 1]]

# Sort seeds and seed_values based on the values in ascending order
sorted_pairs = sorted(zip(seeds, seed_values), key=lambda x: x[1])
seeds, seed_values = zip(*sorted_pairs)

# Convert to array and int32
seeds = np.array(seeds, dtype=np.int32)

# Define input variables for Region Growing
mean_comb     = 0.05
std_threshold = 0.1

# Execute region growing algorithm
region = region_growing(
    mean_array, 
    std_array, 
    seeds, 
    mean_comb, 
    std_threshold
)

# Save as npy
np.save(os.path.join(out_dir, 'region_array.npy'), region)
