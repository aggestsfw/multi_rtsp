from ultralytics import YOLOv10
from PIL import Image
# import gi
 
# model里存放下载好的yolov10n.pt的路径信息
model = YOLOv10(model='/home/zeng/win/workdir/cmdt/yolov10-main/yolov10-master/yolov10x.pt')
 
# 这里的图片是源码里自带的，可以替换成自己的图片
results = model('/home/zeng/win/workdir/cmdt/yolov10-main/yolov10-master/7.png')
 
# 显示预测后的图片
im_array = results[0].plot()
im = Image.fromarray(im_array[..., ::-1])
im.show()
