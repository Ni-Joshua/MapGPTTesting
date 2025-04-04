import json
import os
import pandas as pd
import numpy
from openai import OpenAI, AzureOpenAI
import base64

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

infoFolder = "Img2Loc_Test_Data/Georeference"
imgFolder = "Img2Loc_Test_Data/JPGs"
dfCols = ["imgPath", "Prompt", "Response","Ground Truth"]

#add return format to prompts
prompts = [
"You are an expert geolocator. The image provided is a map of a street or region in the world. Please locate the top left and bottom right longitude and latitude coordinates of the provided location's bounding box. The longitude values should range from -180 degrees to 180 degrees and the latitude values should range from -90 degrees to 90 degrees. Please provide reasoning for your response. Please provide your response in the following format: \"(leftmost longitude value, rightmost longitude value, top latitude value, bottom latitude value)\"",
"You are an expert geolocator. The image provided is a map of a street or region in the world. Please locate the top left and bottom right longitude and latitude coordinates of the provided location's bounding box. The longitude values should range from -180 degrees to 180 degrees and the latitude values should range from -90 degrees to 90 degrees. Please provide reasoning for your response and provide an educated guess if there is not enough information to deduce a response. Please provide your response in the following format: \"(leftmost longitude value, rightmost longitude value, top latitude value, bottom latitude value)\"",
"You are an expert geolocator. The image provided is a map of a street or region in the world. First describe the region displayed and find points of interest in the image. Then, using the description and the image, please locate the top left and bottom right longitude and latitude coordinates of the provided location's bounding box. The longitude values should range from -180 degrees to 180 degrees and the latitude values should range from -90 degrees to 90 degrees. Please provide reasoning for your response and provide an educated guess if there is not enough information to deduce a response. Please provide your response in the following format: \"(leftmost longitude value, rightmost longitude value, top latitude value, bottom latitude value)\"",
]

def loadFiles(infoFolder, imgFolder, df):
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
        temp.append(json.load(open(infoFile))['locn_geometry'])
        df.append(temp)

def constructPrompt(infoFile):
    prompt = prompts[promptid]
    return prompt

def callGPT(currentImage, prompt):
    response = gpt.chat.completions.create(
                # model="o1-2024-12-17",
                model = "gpt-4o",
                messages=[
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

def encodeImage(filePath):
    with open(filePath, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')
    return image_data

for promptid in range(2,3):
    df = []
    loadFiles(infoFolder, imgFolder, df)
    df = pd.DataFrame(df, columns=dfCols)
    df.to_csv(f"TestResults{promptid}.csv", index = False)

#IOU or DICE for evaluation, 

#Optimize pipeline
#Obtain eval function from Zeping
#o1 Baseline
#test files