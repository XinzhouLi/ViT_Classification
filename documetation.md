bias field correction 
    add threshhold 0.5 
    ant package
fsl coregistion 


## Basic information of dataset

|| SPMS | Stable | Worsening |
|  ----  | ----  | ----  | ----  | 
| T1&T2&FLAIR | 65 | 57 | 31 |
|Miss Flair|1|0|1|
|Miss T1|13|12|7|
|Total|79|69|39|

|Stable| Missing T1 | Missing Flair |
|  ----  | ----  | ----  |
|  | CIMS_2098 |  |
|  | CIMS_2342 |  |
|  | CIMS_2627 |  |
|  | CIMS_2744 |  |
|  | CIMS_2875 |  |
|  | CIMS_3337 |  |
|  | CIMS_3367 |  |
|  | CIMS_4171 |  |
|  | CIMS_4427 |  |
|  | CIMS_4449 |  |
|  | CIMS_4702 |  |
|  | CIMS_86   |  |

|SPMS| Missing T1 | Missing Flair |
|  ----  | ----  | ----  |
|  | CIMS_1081 | CIMS_4992 |
|  | CIMS_1708 |           |
|  | CIMS_2574 |           |
|  | CIMS_2662 |           |
|  | CIMS_2717 |           |
|  | CIMS_2901 |           |
|  | CIMS_3721 |           |
|  | CIMS_4243 |           |
|  | CIMS_5129 |           |
|  | CIMS_5736 |           |
|  | CIMS_5761 |           |
|  | CIMS_6643 |           |
|  | CIMS_7247 |           |

|Worsening| Missing T1 | Missing Flair |
|  ----  | ----  | ----  |
|  | CIMS_1204 | CIMS_4195 |
|  | CIMS_1770 |           |
|  | CIMS_1857 |           |
|  | CIMS_2149 |           |
|  | CIMS_2975 |           |
|  | CIMS_3218 |           |
|  | CIMS_3887 |           |

# 7/30 

Now we tried the efficientNet and ViT on this longitudinal dataset, however the testing accuracy (effiNet: 60%, ViT: 50%) does not reach our expectation.

## image Preprocessing 

Firstly, reimplement the whole preprocessing by using python, the final result should be same as Olayinka's version. The raw data without any preprocessing were stored in original_data folder. the python script in original_data is going to finish N4, brain extraction and affine coregistration. 

Now the image preprocessing should contain Bias field correction, Brain extraction, affine co-registration(12 free degree keeps the size of each layers to be the same, previously rigid body 6 free degree were abandon ).



