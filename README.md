# Image Cropping Automation

This is a simple script to automate the process of cropping images to a specific size and centers the face in the image. I developed this script to automate the process of cropping speaker images for my work and save some time on everyday tasks.
It uses OpenCV (https://opencv.org/) to detect faces in the image and crop the image to the size of the face with some excess. Then the image is uploaded to an FTP server. 

# Installation and Requirements

This script requires Python 3.6 or higher. You can install the required packages by running the following command:

```pip install -r requirements.txt````

Additionally download the OpenCV face detection model (https://github.com/codingforentrepreneurs/OpenCV-Python-Series/blob/master/src/cascades/data/haarcascade_frontalface_alt2.xml) and place it in the same directory as the script.

Then, create a `.env` file in the same directory as the script and add the following variables:
```
FTP_HOST=ftp.example.com
FTP_USER=user
FTP_PASSWORD=password
FTP_PATH=/path/to/upload
```

# Usage

Put the images you want to process in a subfolder called `/in` and run the script with `python process_image.py`. The processed images will be saved in a subfolder called `/out` and further moved to a subfolder `/done` if the upload to FTP was successful.
If no face was found, an error will be printed to the console.
