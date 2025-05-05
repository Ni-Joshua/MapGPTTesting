from PIL import Image
import os
import pandas as pd

def convert_tiff_to_png(tiff_filepath, png_filepath):
    try:
        img = Image.open(tiff_filepath)
        img.save(png_filepath, 'PNG')
    except Exception as e:
        print(f"Error converting {tiff_filepath}: {e}")
    
def convert_directory_tiff_to_png(dir_path, pngPath):
    for filename in os.listdir(dir_path):
        if filename.lower().endswith(('.tif', '.tiff')):
            tiff_filepath = os.path.join(dir_path, filename)
            png_filepath = os.path.join(pngPath, os.path.splitext(filename)[0] + '.png')
            convert_tiff_to_png(tiff_filepath, png_filepath)

def convert_tiff_to_jpg(tiff_filepath, jpg_filepath, quality):
    try:
        img = Image.open(tiff_filepath)
        rgb_img = img.convert('RGB')
        rgb_img.save(jpg_filepath, 'JPEG', quality=quality, optimize=True)

        file_size_bytes = os.path.getsize(jpg_filepath)
        file_size_kb = file_size_bytes / 1024
        file_size_mb = file_size_kb / 1024
        if (file_size_mb >= 20):
            convert_tiff_to_jpg(tiff_filepath, jpg_filepath, quality-5)
    except Exception as e:
        print(f"Error converting {tiff_filepath}: {e}")
    
def convert_directory_tiff_to_jpg(dir_path, jpgPath, quality):
    for filename in os.listdir(dir_path):
        if filename.lower().endswith(('.tif', '.tiff')):
            tiff_filepath = os.path.join(dir_path, filename)
            jpg_filepath = os.path.join(jpgPath, os.path.splitext(filename)[0] + '.jpeg')
            convert_tiff_to_jpg(tiff_filepath, jpg_filepath, quality)

def convert_fileList_tiff_to_jpg(fileList, jpgPath, quality):
    for filename in fileList:
        if filename.lower().endswith(('.tif', '.tiff')):
            tiff_filepath = None
            for id in folders:
                if (id in filename):
                    tiff_filepath = os.path.join(folders[id], filename)
                    break
            print(tiff_filepath)
            jpg_filepath = os.path.join(jpgPath, os.path.splitext(filename)[0] + '.jpeg')
            convert_tiff_to_jpg(tiff_filepath, jpg_filepath, quality)

folders = {
    "utaustin": "C:/Users/Joshua Ni/Dropbox/Map2Loc Team Folder/testing_data_SScale_tif",
    "utlmaps": "C:/Users/Joshua Ni/Dropbox/Map2Loc Team Folder/testing_data_LScale_tif"
}

filelist = pd.read_csv('Map2Loc_Full_Test_Data/FileList.csv')["File"].values

# convert_directory_tiff_to_png('Img2Loc_Test_Data/Images', "Img2Loc_Test_Data/PNGs")
convert_directory_tiff_to_jpg('Img2Loc_Test_Data/Images', "Img2Loc_Test_Data/JPEGs", 90)
# convert_fileList_tiff_to_jpg(filelist, "Map2Loc_Full_Test_Data/testing_data_jpeg",90)