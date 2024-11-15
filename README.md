**Repository**  
This repository provides a region-growing function designed to segment an array into regions of similar values, based on a mean and standard deviation array. This can be used to group areas with similar characteristics in stochastic outputs from models.

**Region-Growing function**  
The region-growing function expands regions starting from predefined seed points, using a mean-combing approach. This means that regions only expand to neighboring pixels if they meet dynamic statistical criteria, specifically: 
 - Neighboring pixels must fall within a similarity range around the current region's mean.
 - Standard deviation thresholds are applied to ensure consistency in variability within regions.

![Alt text](./Figures/region_growing_data.svg)
