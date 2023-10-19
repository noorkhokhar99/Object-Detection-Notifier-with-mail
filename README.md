
## **Detect objects, capture them, and send them to mail with the image attachment**

Follow the below commands step by step to make this project run

Clone this repository and execute the commands as shown below

```
git clone https://github.com/noorkhokhar99/Object-Detection-Notifier-with-mail.git

cd Object-Detection-Notifier-with-mail

wget "http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v2_coco_2018_03_29.tar.gz"
```
Once the tar file gets downloaded, unzip it in the same folder (object_detection_notifier)

```
pip install -r requirements.txt
```


Run the below command with your username and password.

```python person_detector_video.py --to_mail_id programmingnet5@gmail.com --pwd idmiltycocmqqqao --from_mail_id pyresearch0@gmail.com ```



