from PIL import Image
import os

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


convert_directory_tiff_to_png('Img2Loc_Test_Data/Images', "Img2Loc_Test_Data/PNGs")