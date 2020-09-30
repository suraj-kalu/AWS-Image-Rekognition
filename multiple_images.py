import boto3
import json
import os
import re


class Rekognition():
    def __init__(self):
        pass
        
    def display(self, details):
        if len(details)  > 0:
            for outcomes in details:
                emotion = ''
                features = ''
                if len(outcomes['emotion']) > 0:
                    emotion = outcomes['emotion'][0]
                else:
                    emotion = "Unable to detect emotion"

                if len(outcomes['features']) > 0:
                    for f in outcomes['features']:
                        features += f + ' '
                else:
                    features = "Unable to detect features"
                
                print('*' * 50)
                print("For image {}".format(outcomes['img']))
                print("Gender : {} \n Age Range : {} \n Emotion : {} \n Features : {}"
                        .format(outcomes['gender'], outcomes['age'],
                        emotion, features))
        
    def detect(self):
        #Establish connection to aws image recokniition
        client = boto3.client('rekognition')
        
        #set the path to the directory containing image
        current_path = os.getcwd()
        img_path = os.path.join(current_path, 'imgs')
        image_details = []
        for file in os.listdir(img_path):
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
                        
                        image_details.append({
                            'gender' : gender,
                            'age' : age,
                            'emotion' : emotion_present,
                            'features' : features_present,
                            'img' : image
                        })        
            else:
                print("The give file is not an image file")
        return image_details 
            
          


def main():
    recognize = Rekognition()
    details = recognize.detect()
    recognize.display(details)

if __name__ == '__main__':
    main()

        