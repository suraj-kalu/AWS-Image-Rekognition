# AWS-Image-Rekognition
This project makes use of the AWS Image Rekognition in order to detect the faces in images.

### Before using AWS service from command line
Install the AWS CLI first. Follow the link below for the instructions.
[AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-windows.html)
Now you need to configure the AWS CLI
[Configuration](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)

Don't forget to set the proper region.

## Installation
All the required libraries are present in the requirements.txt
```
pip install -r requirements.txt
```
## Files
The project consist of two files and two folder. Images can be kept eithe in img or imgs folder. The img folder should contain atmost one image at a time while imgs folder an contain any number of images.The image files should be of .png, .jpg or .jpeg format.

image_rekognition.py makes use of img folder to obtain the image and the output is displayed with the help of PyQt5.

multiple_images.py makes use of imgs folder to obtain the images and the output are displayed in the console.
