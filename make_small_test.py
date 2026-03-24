#!/usr/bin/env python3
from generate_aligned_100 import gen_catalyst, gen_healthy
cases = [gen_catalyst(), gen_healthy()]
import csv
with open('test_small.csv','w',newline='',encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['ID','Fuel','CO_Pct','CO2_Pct','HC_PPM','O2_Pct','NOx_PPM','Lambda_Gas','OBD_STFT','OBD_LTFT','OBD_Lambda','OBD_DTC','Expected_Result','Confidence_Score','ECU_Health'])
    w.writeheader()
    for i,c in enumerate(cases,1):
        c['ID']=f'TC{i:03d}'
        w.writerow(c)
print("Wrote test_small.csv with 2 cases")