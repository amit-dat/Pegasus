import argparse
from utils import set_params, set_download_dir, format_datetime, scrape_images, extract_average_color, classify_images, df_to_csv, df_to_excel, label_images
    
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    profile, num, startdate, enddate, mode, season = set_params(parser)
    
    #Output directory for Scraped Images
    output = set_download_dir(startdate, enddate)
    
    format1 = '%Y-%m-%d'
    
    startdate, enddate = format_datetime(format1, startdate, enddate)
    
    # Mode for scraping images and saving them in output folder
    if mode == '0':
        print("starting download.....")
        scrape_images(profile, num, startdate, enddate, output)
        print("Download Complete!")
    
    # Mode for detecting color and exporting dataframe as .csv
    elif mode == '1':
        classify_images(output, '.jpg','color')
    # Mode for labelling the images
    elif mode == '2':
        label_images(output, '.jpg', season)
    #elif mode == '3':
        
      
    