import glob
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class bip:
    def __init__(self, ev, la, result):
        self.ev = ev
        self.la = la
        self.result = result

class ev_la_group:
    def __init__(self, ev, la):
        self.ev = ev
        self.la = la
        self.every_bip = []
        self.xba

    def add_bip(self, bip):
        self.every_bip.append(bip)

    def xba(self):
        ab = 0
        hit = 0
        for bip in self.every_bip:
            ab += 1
            if bip.result != "Out" and bip.result != "FieldersChoice" and bip.result != "Error":
                hit += 1
        xba = round(hit/ab, 3)
        return round(hit/ab, 3)

    def display(self):
        return f"EV: {self.ev}, LA: {self.la}, Count: {len(self.every_bip)}, XBA: {self.xba()}"

class player:
    def __init__(self, name):
        self.name = name
        self.bip = []
        #self.xba

    def add_bip(self, bip):
        self.bip.append(bip)

    def display(self):
        return self.name

def round_to_nearest_5(x):
    return int(round(x / 5.0) * 5)

x = []
trojans= []

csv_files = glob.glob("*.csv")
# Read and combine all into one DataFrame (optional)
dfs = []
for file in csv_files:
    df = pd.read_csv(file)
    if not df.empty and df.dropna(axis=1, how='all').shape[1] > 0:
        dfs.append(df)

if not dfs:
    print("No valid CSV files with data.")
    exit()

combined_df = pd.concat(dfs, ignore_index=True)

for index, row in combined_df.iterrows():
    if(row['Bearing'] >= -45 and row['Bearing'] <= 45):
        current_bip = bip(round_to_nearest_5(row['ExitSpeed']), round_to_nearest_5(row['Angle']), row['PlayResult'])
        has = False
        for i in x:
            if(i.ev == current_bip.ev and i.la == current_bip.la):
                has = True
                i.add_bip(current_bip)
                break
        if(has == False):
            current_ev_la_group = ev_la_group(round_to_nearest_5(row['ExitSpeed']), round_to_nearest_5(row['Angle']))
            current_ev_la_group.add_bip(current_bip)
            x.append(current_ev_la_group)
        has = False
        if (row['BatterTeam'] == "SOU_TRO"):
            for i in trojans:
                if i.name == row['Batter']:
                    has = True
                    i.add_bip(current_bip)
                    break
            if(has == False):
                xplayer = player(row['Batter'])
                xplayer.add_bip(current_bip)
                trojans.append(xplayer)

x_sorted = sorted(x, key=lambda group: len(group.every_bip), reverse=True)

for group in x_sorted:
    print(group.display())

for i in trojans:
    count = 0
    totalxba = 0
    for p in i.bip:
        #print(str(p.ev) + " " + str(p.la) + " " + p.result)
        count += 1
        for b in x_sorted:
            if p.ev == b.ev and p.la == b.la:
                totalxba += b.xba()
    print(i.display() + ": " + str(totalxba/count) + ", " + str(count))