# Pegasus

## Project 1: Fashion Trend Predictor

This project aims at building a Fashion Trend Predictor. For the purpose of the trend prediction, the repo contains the code for the prediction pipeline which consists of the following **3** parts:
  1. **The Instagram Scraper**: using Instalooter API-less library has the ability to download `num` amount of images from any public `profile` on Instagram within a `timeframe`
  2. **MILpy Image Manipulator**: Modifies the scraped images and saves them to a new directory
  3. **Clarifai Color Detector**: Detects color of the scraped images and exports the report in the form of a `.csv` or `.xlsx` file.
  
  ### Steps to run the pipeline on your local machine
  1. Clone the repo.
  2. Download the requirements using the requirements.txt file using the following command:
  </br>`$ pip3 install -r requirements.txt`
  3. Run the following command to scrape the images (mode `0`) and use (`-m 1`) to detect colors of the image and export the report:
  </br>`$ python3 unlimited_scraper.py -p "mad_tesla" -n 30 -s '2018-03-09' -e '2017-03-09' -m 0 `
