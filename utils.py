# utils.py v 1.0
# Date: 07-22-2018
# Author: Amit Gupta

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

def set_params(parser):
    """
    Parse, add and describe arguments using ArgumentParser
    
    Parameters:
    ----------
        parser: a ArgumentParser object
    
    Returns:
    --------
        profile:    name of the Instagram profile.
        num:        number of images to download.
        startdate:  Most recent date from which you wanna start downloading.
        enddate:    Date to specify the end of timeframe.
        mode:       To specify the usage mode of the pipeline
    
    """
    
    parser.add_argument('-p','--profile', help='specify Instagram profile name')
    parser.add_argument('-n','--num', help='specify num of images to download')
    parser.add_argument('-s','--startdate', help='specify startdate')
    parser.add_argument('-e','--enddate', help='specify enddate')
    
    parser.add_argument('-S','--season', help='specify season')
    
    parser.add_argument('-m','--mode', help='specify the mode for the pipeline functionality. Eg. 0: for complete Pipeline')
    args = parser.parse_args()
    
    profile = args.profile
    num = args.num
    startdate = args.startdate
    enddate = args.enddate
    mode = args.mode
    season = args.season
    
    return profile, num, startdate, enddate, mode, season

def conv_season_to_dates(season):
    """
    Convert the season specified by the user into start and end dates 
    """
    # TODO: the function only contains the specific start and end 
    # dates for different seasons. Code yet to be completed for returning
    # proper dates
    
    seasons = [('winter', (date(Y,  1,  1),  date(Y,  3, 20))),
           ('spring', (date(Y,  3, 21),  date(Y,  6, 20))),
           ('summer', (date(Y,  6, 21),  date(Y,  9, 22))),
           ('autumn', (date(Y,  9, 23),  date(Y, 12, 20))),
           ('winter', (date(Y, 12, 21),  date(Y, 12, 31)))]


def format_datetime(format1, startdate, enddate):
    """
    Specify format of the input date given by the user
    
    Parameters:
    ----------
        format1:    specify the format of datetime object.
        startdate:  Most recent date from which you wanna start downloading.
        enddate:    Date to specify the end of timeframe.
    
    Returns:
    --------
        
        startdate:  Most recent date from which you wanna start downloading.
        enddate:    Date to specify the end of timeframe.
    
    """
    startdate = datetime.datetime.strptime(startdate, format1).date()
    enddate = datetime.datetime.strptime(enddate, format1).date()
    return startdate, enddate

def set_download_dir(startdate, enddate):
    """
    Create the directory where the scraped images will be stored.
    
    Parameters:
    ----------
        startdate:  Most recent date from which you wanna start downloading.
        enddate:    Date to specify the end of timeframe.
    
    Returns:
    --------
        
        output:     The path of the output directory
    
    """
    
    output = 'images_'+str(startdate)+ '_' +str(enddate)
    if not os.path.exists(output):
        os.makedirs(output)
    output = "./"+output
    return output

def scrape_images(profile, num, startdate, enddate, out_dir):
    """
    Function to scrape images from Instagram using Instalooter
    
    Parameters:
    ----------
        profile:    name of the Instagram profile.
        num:        number of images to download.
        startdate:  Most recent date from which you wanna start downloading.
        enddate:    Date to specify the end of timeframe.
    
    Returns:
    --------
        
        output:     The path of the output directory
    
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
    Function to extract the average color and modified images to feed as imput for claasification
    
    Parameters:
    ----------
        profile:    name of the Instagram profile.
        num:        number of images to download.
        startdate:  Most recent date from which you wanna start downloading.
        enddate:    Date to specify the end of timeframe.
    
    Returns:
    --------
        
        The modified images and averaged colors are returned
    """
    milpy.directory_image_average(directory, filetype)

    
def classify_images(input_dir, filetype, model_name='color'):
    """
    Function to detect color using Clarifai API
    
    Parameters:
    ----------
        input_dir:    name of the folder containing Instagram scraped images or Milpy images.
        filetype:     mention the extension of the image files..eg. '.jpg'
        model:        specify name of the Clarifai model.
    
    Returns:
    --------
        
        The .csv or .xlsx file containing a dataframe with columns of image name, colors in that image and hex codes
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
            
        df.loc[count,"Colors"] = str(colors)
        df.loc[count,"Hex_Numbers"] = str(hex_numbers)
        
        #print(hex_number)
        #print(color)
    #print(df)
    df_to_csv(df)
        
        
def df_to_csv(df):
    df.to_csv("color_detection_df.csv")
    
def df_to_excel(df):
    df.to_excel("color_detection_df.xlsx")
    
    
    
###########################################
### Training a season trend classifier ####
###########################################


def label_images(input_dir, filetype, season):
    
    """
    Label images to be fed to Clarifai Model
    """
    # TODO: Figure out how to add concepts. 
    # Assign them IDs and specify concepts and non concepts.
    # figure out the bulk_create_images response error.
    
    seasons = ["spring","summer","fall", "winter"]
    
    concept = season
    seasons.remove(str(season))
    nonconcepts = seasons
    print(concept)
    print(nonconcepts)
    
    app = ClarifaiApp(api_key='f7e11a3064f8468087ca656dce9e7abc')
    
    images = [os.path.join(input_dir,i) for i in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir,i)) and i.endswith(filetype)]
    
    #print(app.inputs.get_all())
    for image in app.inputs.get_all():
        print(image.input_id)
    
    #app.concepts.bulk_create(['id1', 'id2','id3','id4'], ['spring', 'summer','fall', 'winter'])
    
    #df = pd.DataFrame(columns=['Image_Name','Colors','Hex_Numbers'])
    img_list = []
    #for count, picture in enumerate(images,1):
    image = ClImage(url='https://samples.clarifai.com/metro-north.jpg', concepts=[concept], not_concepts=[nonconcepts])
        #print(picture)
        #image = ClImage(file_obj=open(str(picture),'rb'), concepts=[concept], not_concepts=[nonconcepts])
        #img_list.append(image)
    #print(img_list)  
    #print(len(img_list))
    #app.inputs.bulk_create_images([image])
    
    
def create_model():
    
    """
    Create model
    """
    # TODO: Incomplete code for creating the model
   
    app = ClarifaiApp(api_key='f7e11a3064f8468087ca656dce9e7abc')
    
    model = app.models.create('trends', concepts = seasons)