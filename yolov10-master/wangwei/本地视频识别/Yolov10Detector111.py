##调用本地电脑摄像头识别

import cv2
import time
from ultralytics import YOLOv10


def Yolov10Detector(frame, model, image_size, conf_threshold):
    results = model.predict(source=frame, imgsz=image_size, conf=conf_threshold)
    frame = results[0].plot()
    return frame


def main():
    image_size = 640  # Adjust as needed
    conf_threshold = 0.1 # Adjust as needed
    model = YOLOv10("yolov10n.pt")
    source = "1.mp4"  # 0 for webcam
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        print("打开摄像头失败！")
        return
    while True:
        success, frame = cap.read()
        start_time = time.time()

        if success:
            print("读取帧成功！")

        if not success:
            print("读取帧失败！")
            ## TODO  https://www.cnblogs.com/haiyang21/p/11225060.html
            ## 原因：缺少ffmpeg的支持
            # 解决：一般opencv3.3版本及以上支持ffmpeg，实验4.1.0成功
            # pip install opencv-python
            # pip install opencv-contrib-python
            break
        frame = Yolov10Detector(frame, model, image_size, conf_threshold)
        end_time = time.time()
        fps = 1 / (end_time - start_time)
        framefps = "FPS:{:.2f}".format(fps)
        cv2.rectangle(frame, (10, 1), (120, 20), (0, 0, 0), -1)
        cv2.putText(frame, framefps, (15, 17), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        cv2.imshow("yolov10-本地摄像头识别", frame)  # Display the annotated frame
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Exit on 'q' key pres:
            break
    cap.release()
    cv2.destroyAllWindows()
main()
