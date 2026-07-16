#libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings


#preferences
warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

df = pd.read_csv("/Users/ethanc/test_sample_cleaned_v2.csv")
print(df.head(1))


#making combined datasets
fall_files = ["/Users/ethanc/medicare project/Medicare Current Beneficiary Survey - Survey File/2020/SFPUF2020_Data/sfpuf2020_1_fall.csv",
         "/Users/ethanc/medicare project/Medicare Current Beneficiary Survey - Survey File/2021/SFPUF2021_Data/sfpuf2021_1_fall.csv",
         "/Users/ethanc/medicare project/Medicare Current Beneficiary Survey - Survey File/2022/SFPUF2022_Data/sfpuf2022_1_fall.csv",
         "/Users/ethanc/medicare project/Medicare Current Beneficiary Survey - Survey File/2023/SFPUF2023_Data/sfpuf2023_1_fall.csv"]




winter_files = ["/Users/ethanc/medicare project/Medicare Current Beneficiary Survey - Survey File/2020/SFPUF2020_Data/sfpuf2020_2_winter.csv",
                "/Users/ethanc/medicare project/Medicare Current Beneficiary Survey - Survey File/2021/SFPUF2021_Data/sfpuf2021_2_winter.csv",
                "/Users/ethanc/medicare project/Medicare Current Beneficiary Survey - Survey File/2022/SFPUF2022_Data/sfpuf2022_2_winter.csv",
                "/Users/ethanc/medicare project/Medicare Current Beneficiary Survey - Survey File/2023/SFPUF2023_Data/sfpuf2023_2_winter.csv"]

f_datasets = [pd.read_csv(f) for f in fall_files]
w_datasets = [pd.read_csv(f) for f in winter_files]

fall = pd.concat(f_datasets, ignore_index=True)
winter = pd.concat(w_datasets, ignore_index = True)

winter_to_merge = winter.drop(columns=['SURVEYYR', 'VERSION'])
df = fall.merge(winter_to_merge, on = 'PUF_ID', how = 'inner')

#exploratory data analysis
#print(df.info())
#print(df.shape)
#print(df.head(1))
#print(df.isnull().sum())



#cleaning data
drop_prefix = ['PUFF', 'PUFW']
prefix_cols = [c for c in df.columns
        if not any(c.startswith(p) for p in drop_prefix)]
df = df[prefix_cols]

drop_cols = ['']


#print(df.columns.tolist())







