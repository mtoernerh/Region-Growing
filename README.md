**Repository**  
This repository provides a region-growing function designed to segment an array into regions of similar values, based on mean and standard deviation arrays. This functionality is particularly useful for grouping areas with comparable characteristics in stochastic model outputs. For example, it can be applied to identify regions with similar nitrate retention properties across multiple model realizations.  

**Region-Growing function**  
The region-growing function expands regions starting from predefined seed points using a dynamic, mean-combing approach. Specifically:   
 - Neighboring pixels are included in a region only if their values fall within a similarity range around the current region's mean.
 - Standard deviation thresholds are applied to ensure that the variability within each region remains consistent.

The figure below illustrates the input and output arrays of the region-growing process. The mean array (left) represents normalized nitrate retention, derived from stochastic model realizations. The standard deviation array (middle) captures the variability in nitrate retention across model runs. The resultant region array (right) highlights regions of similiar nitrate retention attributes. In the provided example, every non-NaN pixel is used as a seed, resulting in a total of 1,112,171 seeds. The region-growing function segments the data into 279,428 unique regions in the output array. However, the majority of these regions are small and insignificant.
  
To address this, a secondary visualization is included where regions are color-coded based on their areal extent. Regions smaller than 50 hectares are shown in grey to emphasize more significant regions, enabling easier interpretation and highlighting zones of practical importance.
![Alt text](./Figures/region_growing_data.svg)
