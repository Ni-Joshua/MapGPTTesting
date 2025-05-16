import json
import os
import pandas as pd
import numpy
from openai import OpenAI, AzureOpenAI
import base64
from pydantic import BaseModel
from PIL import Image
import io

#change api key to Azure one
# gpt = OpenAI(api_key=os.environ.get("GPT_API_KEY"))
gpt = AzureOpenAI(
    # model="gpt-4o",
    # deployment_name="gpt-4o",
    api_key=os.environ.get("AZURE_GPT_API_KEY"),
    azure_endpoint='https://seai-westus.openai.azure.com/',
    api_version="2025-03-01-preview",
)
#Longitude: -180 to 180, Latitude: -90 to 90

infoFolder = "Map2Loc_Full_Test_Data/testing_data_json"
imgFolder = "Map2Loc_Full_Test_Data/testing_data_jpeg"
tifimgFolder = 'Img2Loc_Test_Data/Images'

dfCols = ["imgPath", "Prompt", "Response","Ground Truth"]
model = "4o"
#add return format to prompts
prompts = [
"The image provided is a map of a street or region in the world. Please locate the top left and bottom right longitude and latitude coordinates of the provided location's bounding box. The longitude values should range from -180 degrees to 180 degrees and the latitude values should range from -90 degrees to 90 degrees. Please provide reasoning for your response. Please provide your response in the following format: \"(leftmost longitude number, rightmost longitude number, top latitude number, bottom latitude number)\"",
"The image provided is a map of a street or region in the world. Please locate the top left and bottom right longitude and latitude coordinates of the provided location's bounding box. The longitude values should range from -180 degrees to 180 degrees and the latitude values should range from -90 degrees to 90 degrees. Please provide reasoning for your response and provide an educated guess if there is not enough information to deduce a response. Please provide your response in the following format: \"(leftmost longitude number, rightmost longitude number, top latitude number, bottom latitude number)\"",
"The image provided is a map of a street or region in the world. First describe the region displayed and find points of interest in the image. Then, using the description and the image, please locate the top left and bottom right longitude and latitude coordinates of the provided location's bounding box. The longitude values should range from -180 degrees to 180 degrees and the latitude values should range from -90 degrees to 90 degrees. Please provide reasoning for your response and provide an educated guess if there is not enough information to deduce a response. Please provide your response in the following format: \"(leftmost longitude number, rightmost longitude number, top latitude number, bottom latitude number)\"",
"The image provided is a map of a street or region in the world. Please locate the top left and bottom right longitude and latitude coordinates of the provided location's bounding box. The longitude values should range from -180 degrees to 180 degrees and the latitude values should range from -90 degrees to 90 degrees. Please provide no additional text in your response and provide an educated guess if there is not enough information to deduce a response. Please provide your response in the following format: \"(leftmost longitude number, rightmost longitude number, top latitude number, bottom latitude number)\". These numbers should not include text and the ° symbol. The values can include decimal values.",
"Your sole task is to look at the provided historical map image and determine its geographic bounding box. You must output **only** four decimal-degree numbers in this exact order and format, with no extra text: (leftmost_longitude, rightmost_longitude, top_latitude, bottom_latitude). Include parentheses, commas, and spaces.  These numbers should not include text and the ° symbol.",
"Your sole task is to look at the provided historical map image and determine its geographic bounding box. You should mainly utilize geographic features found in the map. You must output **only** four decimal-degree numbers in this exact order and format, with no extra text: (leftmost_longitude, rightmost_longitude, top_latitude, bottom_latitude). Include parentheses, commas, and spaces.  These numbers should not include text and the ° symbol.",
]

def convert_tiff_to_jpg(tiff_filepath, quality):
    try:
        img = Image.open(tiff_filepath)
        buffer = io.BytesIO()
        
        rgb_img = img.convert('RGB')        
        rgb_img.save(buffer, 'JPEG', quality=quality, optimize=True)

        jpgbytes =  buffer.getvalue()
        # jpg =Image.open(buffer)
        buffer.close()
        file_size_bytes = len(jpgbytes)
        file_size_kb = file_size_bytes / 1024
        file_size_mb = file_size_kb / 1024
        if (file_size_mb >= 20):
            convert_tiff_to_jpg(tiff_filepath, quality-5)
        else:
            return jpgbytes
    except Exception as e:
        print(f"Error converting {tiff_filepath}: {e}")

def loadFiles(infoFolder, imgFolder, df):
    index = 0
    for filename in os.listdir(imgFolder):
        temp = []
        infoFile = os.path.join(infoFolder, filename.split(".")[0] + ".json")
        imgFile = os.path.join(imgFolder, filename)
        temp.append(imgFile)
        prompt = constructPrompt(infoFile)
        temp.append(prompt)
        response = callGPT(imgFile, prompt)
        print(response)
        temp.append(response)
        temp.append(json.load(open(infoFile))['locn_geometry'].split("ENVELOPE")[1])
        df.append(temp)
        index+=1
        if(index%10 == 0):
            df2 = pd.DataFrame(df, columns=dfCols)
            df2.to_csv(f"Map2Loc_GPTResults/{model}TestResults{promptid}.csv", index = False)
        

def constructPrompt(infoFile):
    prompt = prompts[promptid]
    return prompt

def callGPT(currentImage, prompt):
    currentImage = convert_tiff_to_jpg(currentImage, 90)
    for i in range(0,7):
        try:
            response = gpt.chat.completions.create(
                        # model="o1-2024-12-17",
                        model = "gpt-4o",
                        messages=[                    
                            {"role": "system", "content": "You are an expert in geospatial analysis."},
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text":  prompt},
                                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{encodeImage(currentImage)}"}}
                                ]
                            }
                        ],
                    )
            return ' '.join(response.choices[0].message.content.splitlines())
        except Exception as e:
            print(e)
            print("Retrying...")
            continue
    return "Error: Could not Generate a Response"

def encodeImage(bytes):
    # with open(filePath, "rb") as image_file:
    #     image_data = base64.b64encode(image_file.read()).decode('utf-8')
    image_data = base64.b64encode(bytes).decode('utf-8')
    return image_data

for promptid in range(4,6):
    df = []
    loadFiles(infoFolder, imgFolder, df)
    df = pd.DataFrame(df, columns=dfCols)
    df.to_csv(f"Map2Loc_GPTResults/{model}TestResults{promptid}.csv", index = False)

#IOU or DICE for evaluation, 

#Optimize pipeline
#Obtain eval function from Zeping
#o1 Baseline
#test files

#try 4o, o1, 4V, do Prompt tuning
#complete processing GPT response and do evaluation