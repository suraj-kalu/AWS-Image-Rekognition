import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import boto3
import json
import os
import re


class Rekognition(QWidget):

    def __init__(self):
        super().__init__()
        self.outcomes = self.detect()
        if self.outcomes != 1:
            self.initUI()
        else:
            sys.exit()
        
    def initUI(self):

        emotion = ''
        features = ''
        if len(self.outcomes['emotion']) > 0:
            emotion = self.outcomes['emotion'][0]
        else:
            emotion = "Unable to detect emotion"

        if len(self.outcomes['features']) > 0:
            for f in self.outcomes['features']:
                features += f + ' '
        else:
            features = "Unable to detect features"

        l1 = QLabel("Gender : {} \n Age Range : {} \n Emotion : {} \n Features : {}"
                    .format(self.outcomes['gender'], self.outcomes['age'],
                    emotion, features),self)
        l2 = QLabel(self)
        
        l1.setAlignment(Qt.AlignCenter)
        l2.setAlignment(Qt.AlignCenter)
        l2.setPixmap(QPixmap(self.outcomes['img']))

        #Set vertical layout for widgets where widgets will be placed one after another below it
        vbox = QVBoxLayout(self)
        vbox.addWidget(l1)
        vbox.addStretch()
        vbox.addWidget(l2)

        self.resize(500, 500)
        self.setWindowTitle("Image Rekognition")
        self.show()

    def detect(self):
        #Establish connection to aws image recokniition
        client = boto3.client('rekognition')
        
        #set the path to the directory containing image
        current_path = os.getcwd()
        img_path = os.path.join(current_path, 'img')
        if len(os.listdir(img_path)) > 0:
            file = os.listdir(img_path)[0]

            #Check image extension
            is_img_file = re.search(r'.jpg$|.png$|.jpeg$', file)
            if is_img_file:
                print("The given file is an image file")
                image = os.path.join(img_path, file)
                with open(image, 'rb') as img_file:
                    responses = client.detect_faces(Image ={
                        'Bytes':img_file.read()
                    }, Attributes = ['ALL'])

                    for response in responses['FaceDetails']:
                        gender = response['Gender']['Value']
                        age = str(response['AgeRange']['Low']) + ' - ' + str(response['AgeRange']['High'])
                        emotions = dict()
                        for emotion in response['Emotions']:
                            emotions[emotion['Type']] = emotion['Confidence']
                        # max_val = max(emotions.values())
                        # print(max_val)
                        emotion_present = []
                        for key, value in emotions.items():
                            if value >= 75:
                                emotion_present.append(key)
        
                        features = ['Eyeglasses', 'Sunglasses', 'Beard', 'Mustache']
                        features_present  = []
                        for f in features:
                            if response[f]['Value']:
                                features_present.append(f)
                        
                        return {
                            'gender' : gender,
                            'age' : age,
                            'emotion' : emotion_present,
                            'features' : features_present,
                            'img' : image
                        }
                        
            else:
                print("The give file is not an image file")
                return 1
        else:
            print("No file detected")
            return  1
          


def main():
    app = QApplication(sys.argv)
    recognize = Rekognition()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

        