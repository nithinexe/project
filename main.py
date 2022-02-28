import cv2
import time
import uuid
import os

IMAGES_PATH = '/Users/sunny/projects/RealTimeObjectDetection/Tensorflow/workspace/images/collectedimages/'
labels = ['hello','thanks','iloveyou','yes','no']
number_imgs = 15


for label in labels:
    os.mkdir ('Users\sunny\projects\RealTimeObjectDetection\Tensorflow\workspace\images\collectedimages\\'+label)
    cap = cv2.VideoCapture(0)
    print('collecting images for{}'.format(label))
    time.sleep(5)
    for imgnum in range(number_imgs):
        ret, frame = cap.read()
        imgname = os.path.join(IMAGES_PATH,label,label + '.'+'{}.jpg'.format(str(uuid.uuid1())))
        cv2.imwrite(imgname, frame)
        cv2.imshow('frame', frame)
        time.sleep(2)
        
                                 
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()



/Users/sunny/projects/RealTimeObjectDetection/Tensorflow/workspace/images/collectedimages