from instalooter.looters import ProfileLooter
import argparse
import datetime
import os

# For extracting main colors and averaging
import milpy

# For Detecting Color and saving it to a .csv file
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage

# Create DF and exporting
import pandas as pd



def scrape_images(profile, num, startdate, enddate, out_dir):
    """
    """
    #output = 'images_'+str(startdate)+ '_' +str(enddate)
    looter = ProfileLooter(profile)
    #if not os.path.exists(output):
    #    os.makedirs(output)
    #output = "./"+output
    looter.download(output, media_count=int(num), timeframe=(startdate, enddate))
    
    return output
    
    
def extract_average_color(directory, filetype):
    """
    """
    milpy.directory_image_average(directory, filetype)

    
def classify_images(input_dir, filetype, model_name='color'):
    """
    """
   
    # Create your API key in your account's `Manage your API keys` page:
    # https://clarifai.com/developer/account/keys

    app = ClarifaiApp(api_key='f7e11a3064f8468087ca656dce9e7abc')

    # You can also create an environment variable called `CLARIFAI_API_KEY` 
    # and set its value to your API key.
    # In this case, the construction of the object requires no `api_key` argument.

    #app = ClarifaiApp()
    
 
    model = app.models.get(model_name)
    images = [os.path.join(input_dir,i) for i in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir,i)) and i.endswith(filetype)]
    
    df = pd.DataFrame(columns=['Image_Name','Colors','Hex_Numbers'])
    
    for count, picture in enumerate(images,1):
        #image = ClImage(url='https://samples.clarifai.com/metro-north.jpg')
        image = ClImage(filename = picture)
        response = model.predict([image])
        #print(response)
        #print(type(response))
        hex_numbers=[]
        colors=[]
        df.loc[count, "Image_Name"] = picture.split('/')[2]
        for i in range(0, len(list(response['outputs'][0]['data']['colors']))):
            hex_numbers.append(response['outputs'][0]['data']['colors'][i]['w3c']['hex'])
            colors.append(response['outputs'][0]['data']['colors'][i]['w3c']['name'])
            
        df.loc[count,"Colors"] = [colors]
        df.loc[count,"Hex_Numbers"] = [hex_numbers]
        
        #print(hex_number)
        #print(color)
    #print(df)
    df_to_csv(df)
        
        
def df_to_csv(df):
    df.to_csv("color_detection_df.csv")
    
def df_to_excel(df):
    df.to_excel("color_detection_df.xlsx")
    
    
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-p','--profile', help='specify Instagram profile name')
    parser.add_argument('-n','--num', help='specify num of images to download')
    parser.add_argument('-s','--startdate', help='specify startdate')
    parser.add_argument('-e','--enddate', help='specify enddate')
    
    parser.add_argument('-m','--mode', help='specify the mode for the pipeline functionality. Eg. 0: for complete Pipeline')
    args = parser.parse_args()
    
    profile = args.profile
    num = args.num
    startdate = args.startdate
    enddate = args.enddate
    
    mode = args.mode
    
    #Output directory for Scraped Images
    output = 'images_'+str(startdate)+ '_' +str(enddate)
    if not os.path.exists(output):
        os.makedirs(output)
    output = "./"+output
    
    format1 = '%Y-%m-%d'
    startdate = datetime.datetime.strptime(startdate, format1).date()
    enddate = datetime.datetime.strptime(enddate, format1).date()
    
    # Mode for scraping images and saving them in output folder
    if mode == '0':
        print("starting download.....")
        scrape_images(profile, num, startdate, enddate, output)
        print("Download Complete!")
    
    # Mode for detecting color and exporting dataframe as .csv
    elif mode == '1':
        classify_images(output, '.jpg','color')
    