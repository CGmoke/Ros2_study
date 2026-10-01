import face_recognition
import cv2
from ament_index_python.packages import get_package_share_directory #获取功能包share目录绝对路径
import os
def main():
    #获取图片真实路径
    default_image_path = os.path.join(get_package_share_directory('demo_python_service'), 'resource', 'image.png')

    print(f"图片的真实路径:{default_image_path}")
    #是用cv2加载图片
    image = cv2.imread(default_image_path)
    #检测人脸
    face_recognitions = face_recognition.face_locations(image,number_of_times_to_upsample=self.number_of_times_to_upsample,model=self.model)
    #绘制人脸框
    for top,right,bottom,left in face_recognitions:
        cv2.rectangle(image,(left,top),(right,bottom),(255,0,0),4)
    cv2.imshow('Face Detecte Result',image)
    cv2.waitKey(0)