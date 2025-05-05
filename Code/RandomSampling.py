import os
import numpy as np
import pandas as pd
import random
from PIL import Image

# allJsons = os.listdir("Map2Loc_Full_Test_Data/testing_data_json")
folders = {
    "utaustin": os.listdir("C:/Users/Joshua Ni/Dropbox/Map2Loc Team Folder/testing_data_SScale_tif"),
    "utlmaps": os.listdir("C:/Users/Joshua Ni/Dropbox/Map2Loc Team Folder/testing_data_LScale_tif")
}

split = {
    "utaustin":50,
    "utlmaps":50
}

selected = []
random.seed(48)

# def fullyRandomSelection():
#     while (len(selected) < 100):
#         current = allJsons[np.random.randint(0, len(allJsons))]
#         if (not current in selected):
#             print(current)
#             selected.append(current)

def selectedSplitSelection(split):
    global selected
    for key in split:
        selected += random.sample(k=split[key], population=folders[key])

selectedSplitSelection(split)
df = pd.DataFrame(selected, columns = ["File"])
df.to_csv("Map2Loc_Full_Test_Data/FileList.csv", index=False)

# print(os.listdir("C:/Users/Joshua Ni/Dropbox/Map2Loc Team Folder/testing_data_LScale_tif"))