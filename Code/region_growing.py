# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 13:24:22 2024

@author: mfth
"""

import numpy as np

        
def region_growing(mean_array,
                   std_array,
                   seed_array,
                   mean_comb,
                   std_threshold,
                   diagonal=True,
                   overwrite=20): 
    """
  Perform a region-growing algorithm to identify and label regions in an array
  based on similarity in mean and standard deviation values. The function expands
  regions starting from given seed points and grows them based on dynamic
  statistical thresholds applied to neighboring pixels.

  Parameters
  ----------
  mean_array : np.ndarray
      A 2D array representing the mean values for each pixel. Regions will grow
      based on the similarity of these mean values to the current region’s cumulative
      mean, adjusted by `mean_comb`.
  
  std_array : np.ndarray
      A 2D array of the same shape as `mean_array` containing the standard deviation
      values for each pixel. A region will only grow into a pixel if its standard
      deviation is below `std_threshold`.
  
  seed_array : np.ndarray
      A 2D array of shape (N, 2) where each row represents the coordinates (y, x) of a
      seed point from which a region will begin growing.
  
  mean_comb : float
      The combination tolerance for mean similarity. A region will only grow to include
      a neighboring pixel if its mean value falls within the range:
      `(current_mean - mean_comb, current_mean + mean_comb)`.
  
  std_threshold : float
      The threshold for standard deviation. A region will only grow into pixels with a
      standard deviation below this threshold.
  
  diagonal : bool, optional, default=True
      If True, the region-growing algorithm will consider diagonal neighbors in addition
      to the four cardinal directions (left, right, up, down). If False, only the
      four cardinal neighbors are considered.
  
  overwrite : int, optional, default=20
      A limit on the number of pixels that can be overwritten in an existing region.
      If a neighboring region has more pixels than this limit, it will not be merged
      into the current growing region.

  Returns
  -------
  grown : np.ndarray
      A 2D array of the same shape as `mean_array` with each pixel labeled with a
      unique integer representing the region to which it belongs. Pixels that are
      not part of any region remain labeled as 0.

  Notes
  -----
  The region-growing algorithm works as follows:
    1. Starting from each seed point, a region is initialized.
    2. For each pixel in the region, neighboring pixels are checked for inclusion.
    3. A neighboring pixel is included if:
       - Its mean value lies within a dynamic range centered around the region’s
         cumulative mean, adjusted by `mean_comb`.
       - Its standard deviation is below `std_threshold`.
       - The neighboring pixel either does not belong to any region, or belongs to a
         smaller region that can be overwritten (determined by `overwrite`).
    4. If `diagonal` is set to True, diagonal neighbors are also considered.

  Example
  -------
  grown = region_growing(mean_array, std_array, seed_array, mean_comb=0.5, std_threshold=1.0)
  """
    height = mean_array.shape[0]
    width = mean_array.shape[1]
    grown = np.zeros((height, width), dtype=np.uint32)

    neighbors = [(0, -1), (-1, 0), (0, 1), (1, 0)]
    diag_neighbors = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    
    i = 0
    for seed_idx in range(seed_array.shape[0]):
        i += 1
        
        y, x = seed_array[seed_idx]
        
        if grown[y, x] > 0:
            continue
            
        grown[y, x] = i
        
        if std_array[y, x] >= std_threshold:
            continue
        
        queue = [(y, x)]
        sum_value = mean_array[y, x]
        count = 1
        mean_up_comb = sum_value / count + mean_comb
        mean_down_comb = sum_value / count - mean_comb

        while queue:
            py, px = queue.pop(0)
            
            for dy, dx in neighbors:
                ny, nx = py + dy, px + dx
                if 0 <= nx < width and 0 <= ny < height:
                    neighbor_value = grown[ny, nx]
                    if neighbor_value != i:
                        neighbor_count = np.sum(grown == neighbor_value) if neighbor_value != 0 else 0
                        if neighbor_count <= overwrite:
                            mean_value = mean_array[ny, nx]
                            stdev_value = std_array[ny, nx]
                            if mean_down_comb <= mean_value <= mean_up_comb and stdev_value < std_threshold:
                                grown[ny, nx] = i
                                queue.append((ny, nx))
                                sum_value += mean_value
                                count += 1
                                mean_up_comb = sum_value / count + mean_comb
                                mean_down_comb = sum_value / count - mean_comb
            
            if diagonal:
                for dy, dx in diag_neighbors:
                    ny, nx = py + dy, px + dx
                    if 0 <= nx < width and 0 <= ny < height:
                        neighbor_value = grown[ny, nx]
                        if neighbor_value != i:
                            neighbor_count = np.sum(grown == neighbor_value) if neighbor_value != 0 else 0
                            if neighbor_count <= overwrite:
                                mean_value = mean_array[ny, nx]
                                stdev_value = std_array[ny, nx]
                                if mean_down_comb <= mean_value <= mean_up_comb and stdev_value < std_threshold:
                                    grown[ny, nx] = i
                                    queue.append((ny, nx))
                                    sum_value += mean_value
                                    count += 1
                                    mean_up_comb = sum_value / count + mean_comb
                                    mean_down_comb = sum_value / count - mean_comb

    return grown