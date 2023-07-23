
import cv2
import os
import ftplib
from dotenv import load_dotenv


load_dotenv()

FTP_HOST = os.getenv('FTP_HOST')
FTP_USER = os.getenv('FTP_USER')
FTP_PASS = os.getenv('FTP_PASS')
FTP_PATH = os.getenv('FTP_PATH')

ftp = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS)
ftp.encoding = "utf-8"
ftp.cwd(FTP_PATH)

# setup load image recognition cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')

# Read the input images
filenames = next(os.walk("in/"), (None, None, []))[2]  # [] if no file
# remove unwanted filenames
filenames.remove('.DS_Store') if '.DS_Store' in filenames else None
imgs = [cv2.imread('in/' + filename) for filename in filenames]

for (img, filename) in zip(imgs, filenames):
    os.remove('in/' + filename)
    if "jpeg" in filename:
        filename = filename.replace(".jpeg", ".jpg")
    if "png" in filename:
        filename = filename.replace(".png", ".jpg")
    filename = filename.replace(" ", "").lower()

    # Convert into grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    img_height = img.shape[0]
    img_width = img.shape[1]

    if len(faces) == 0:
        print("No faces found in image " + filename)

    # Draw rectangle around the faces and crop the faces
    for (x, y, w, h) in faces:
        h = int(h * 2.3)
        y = y - int(h/4.1)
        w = int(w * 2.3)
        x = x - int(w/4)
        if (y < 0):
            y = 0
        if (x < 0):
            x = 0
        # make image square
        if x > y:
            y = x
        elif y > x:
            x = y
        # find face
        size = min(h, w, img_height, img_width)
        faces = img[y:y + size, x:x + size]
        # scale to 600px
        desired_image_size = 600
        scale_percent = desired_image_size / size
        dimensions = (int((y + size) * scale_percent), int((x + size) * scale_percent))
        # choose better interpolation depending on shrinking or enlarging img
        interpolation_choice = cv2.INTER_AREA if scale_percent < 1  else cv2.INTER_CUBIC
        faces = cv2.resize(faces, dimensions, interpolation=interpolation_choice)
        # save
        cv2.imwrite('out/' + filename, faces)
        with open("out/" + filename, "rb") as file:
            ftp.storbinary(f"STOR {filename}", file)
        os.rename('out/' + filename, 'out/done/' + filename)
        
ftp.quit()
