import glob
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class pitch_type:
    def __init__(self, name):
        self.name = name
        self.thrown = []

    def add_throw(self, pitch):
        self.thrown.append(pitch)

class pitch:
    def __init__(self, name, velocity, ivb, hb, sr, rh, x, y):
        self.name = name
        self.velocity = velocity
        self.ivb = ivb
        self.hb = hb
        self.sr = sr
        self.rh = rh
        self.x = x
        self.y = y

csv_files = glob.glob("*.csv")
dfs = []
for file in csv_files:
    df = pd.read_csv(file)
    if not df.empty and df.dropna(axis=1, how='all').shape[1] > 0:
        dfs.append(df)

if not dfs:
    print("No valid CSV files with data.")
    exit()

combined_df = pd.concat(dfs, ignore_index=True)

count = 0
pitches = []

for index, row in combined_df.iterrows():
    if(row['Pitcher'] == "Hunter, Caden"):
        count += 1
        has = False
        for i in pitches:
            if i.name == row['TaggedPitchType']:
                has = True
                current_thrown = pitch(row['TaggedPitchType'], row['RelSpeed'], row['InducedVertBreak'], row['HorzBreak'], row['SpinRate'], row['RelHeight'], row['PlateLocSide'], row['PlateLocHeight'])
                i.add_throw(current_thrown)
                break
        if has == False:
            current_pitch_type = pitch_type(row['TaggedPitchType'])
            current_thrown = pitch(row['TaggedPitchType'], row['RelSpeed'], row['InducedVertBreak'], row['HorzBreak'], row['SpinRate'], row['RelHeight'], row['PlateLocSide'], row['PlateLocHeight'])
            current_pitch_type.add_throw(current_thrown)
            pitches.append(current_pitch_type)
        #print(row['RelSpeed'])

for i in pitches:
    print(i.name)
    for k in i.thrown:
        print(k.velocity)
    print()
print(count)