# importing necessary libraries 
from posixpath import join
import cv2 
import os
import numpy as np 
from send_mail import send_mail
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--dl_model',type=str, help='the deep learning model file',default='./ssd_mobilenet_v2_coco_2018_03_29/frozen_inference_graph.pb')
parser.add_argument('--label_file',type=str,default='./new_labels.txt',help='label file')
parser.add_argument('--config',type=str,default='./ssd_mobilenet.pbtxt.txt')
parser.add_argument('--detection_folder',type=str,default='./person_detector/objects/')
parser.add_argument('--to_mail_id',nargs='+',help="list of 'to mail' id")
parser.add_argument('--from_mail_id',type=str,help='senders mail id')
parser.add_argument('--pwd',type=str,help='password of the senders mail id')
parser.add_argument('--video',type=str,default=0,help='path of video file')

args = parser.parse_args()
dl_model = args.dl_model
config = args.config
label_file = args.label_file
detection_folder = args.detection_folder
from_mail_id = args.from_mail_id
uname = args.from_mail_id
pwd = args.pwd
to_mail_id = args.to_mail_id



if os.path.exists(detection_folder):
    pass
else:
    os.makedirs(detection_folder)
    print('directory created')

# making sure that our storage directory is clean
for i in os.listdir(detection_folder):
    os.remove(os.path.join(detection_folder,i))


def detected_object(video):
    
    # reading the class names and making a list out of it 
    with open(label_file,'r') as f: 
        class_names = f.read().split('\n') 
    colors = np.random.uniform(0,255,size=(len(class_names),3)) 
        
    # laoding the model
    model = cv2.dnn.readNet(model=dl_model,config=config,framework="Tensorflow") 
    frame_count = 0
    # loading the video
    video = cv2.VideoCapture(video)
    while video.isOpened():
        frame_count+=1
        
        ret, img = video.read()
        img_h, img_w, _  = img.shape 
        
        # creating blob as the model expects to be
        blob = cv2.dnn.blobFromImage(image=img, size = (300,300), mean=(104,117,123), swapRB=True) 
        model.setInput(blob) 
        output = model.forward() 
        object_count = 0
        for detection in output[0,0,:,:]: 
            object_count+=1
            confidence = detection[2] 
            try:
                if confidence > 0.5: 
                    class_id = detection[1] 
                    class_name = class_names[int(class_id)-1]+' '+str(confidence)[:4] 
                    color = colors[int(class_id)] 
                    box_x = int(detection[3] * img_w) 
                    box_y = int(detection[4] * img_h) 
                    box_w = int(detection[5] * img_w) 
                    box_h = int(detection[6] * img_h) 
                    img = cv2.rectangle(img,((box_x),(box_y)),((box_w),(box_h)),color,thickness =2) 
                    crop_img = img[box_y:,box_x:box_w]
                    cv2.imwrite(detection_folder+'frame_'+str(frame_count)+'object_'+str(object_count)+'_'+str(class_name)+'.jpg',crop_img)
                    detected_image = str(detection_folder+'frame_'+str(frame_count)+'object_'+str(object_count)+'_'+str(class_name)+'.jpg')
                    print('object detected')
                    print(class_name)
                    send_mail(uname,pwd,from_email=from_mail_id,to_emails=to_mail_id,attachment=detected_image)
                    if len(os.listdir(detection_folder))>=5: # limiting the number of images to 5, in order to save space
                        for i in os.listdir(detection_folder):
                            os.remove(os.path.join(detection_folder,i))
            except Exception as ex:
                print(str((ex)),'has occured')
                pass

    return detection_folder

detected_object(video=0)


