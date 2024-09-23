import shutil

from ultralytics import YOLOv10
from PIL import Image
import cv2
import os
import skvideo.io
from tqdm import tqdm

def get_filelist(dir):
    Filelist = []
    for home, dirs, files in os.walk(dir):
        for filename in files:
            # 文件名列表，包含完整路径
            # Filelist.append(os.path.join(home, filename).replace('\n', '').replace('\r', '').replace('\\', '/'))
            # # 文件名列表，只包含文件名
            Filelist.append( filename)
    return Filelist

if __name__ == '__main__':

    # model里存放下载好的yolov10n.pt的路径信息
    model = YOLOv10(model='/home/zeng/win/workdir/cmdt/yolov10-main/yolov10-master/yolov10x.pt')

    data_dir = '/home/zeng/win/data_dir/cmdt/250'
    res_dir = '/home/zeng/win/data_dir/cmdt/res'
    finish_dir = '/home/zeng/win/data_dir/cmdt/finish'
    person_dir = data_dir + '/person'
    no_person_dir = data_dir + '/no_person'
    if not os.path.exists(person_dir):
        os.mkdir(person_dir)
    if not os.path.exists(no_person_dir):
        os.mkdir(no_person_dir)
    list = get_filelist(data_dir)
    list = sorted(list, reverse=False)

    # 11%|█         | 4/36 [30:59<4:13:06, 474.58s/it]
    # #split res and finished
    # for i in range(len(list)):
    #     if i < 65:
    #         shutil.move(data_dir + '/' + list[i], finish_dir + '/' + list[i])
    #     else:
    #         shutil.move(data_dir + '/' + list[i], res_dir + '/' + list[i])

#56%|█████▌    | 20/36 [3:12:33<2:34:03, 577.69s/it]
    for i in tqdm(range(23, len(list))):
        video1 = cv2.VideoCapture(data_dir + '/' + list[i])
        # 获取视频文件的帧率、宽度和高度
        fps = video1.get(cv2.CAP_PROP_FPS)
        width = int(video1.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video1.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # 创建VideoWriter对象，设置输出视频文件的名称、编码格式、帧率、尺寸和是否为彩色视频
        # video2 = cv2.VideoWriter('/home/zeng/hd1/data_dir/cmdt/output.avi', cv2.CAP_MSMF, cv2.VideoWriter_fourcc(*'MP42'), fps, (width, height), True)
        # video2 = cv2.VideoWriter()
        # video2.open('appsrc ! videoconvert ! avenc_mpeg4 bitrate=100000 ! mp4mux ! filesink location=/home/zeng/hd1/data_dir/cmdt/video11.mp4', \
        #                          cv2.CAP_GSTREAMER, 0, 10, (width, height), True)

        # '-f': 'mp4', '-b': '300000000'
        writer_p = skvideo.io.FFmpegWriter(person_dir + '/' + list[i], outputdict={'-r':str(fps),\
                                                                                   '-threads': '16',\
                                                                                                '-vcodec': 'libx265'})
        writer_np = skvideo.io.FFmpegWriter(no_person_dir + '/' + list[i], outputdict={'-r':str(fps), \
                                                                                       '-threads': '16', \
                                                                                       '-vcodec': 'libx265'})

        # video2.set(cv2.CAP_PROP_BITRATE, 30000)
        step = 40
        step1 = step
        count = 0
        count_no_person = 0
        flag = False
        count_start = 0
        count_end = 0
        count_ret = 0
        while video1.isOpened():
            ret, frame = video1.read()
            if not ret:
                break
            else:
                count_ret = 0

                # if count_no_person >= 10:
                #     step1 = step * 10
                # else:
                #     step1 = step
                  # 显示预测后的图片
                if count % step1 == 0:
                    count_start = count
                    count_end = count + step1
                    results = model.predict(frame)
                    flag = False
                    for box in results[0].boxes:
                        cls = box.cls[0]
                        if results[0].names[cls.item()] == 'person':
                            flag = True
                            break
                    print('process %s video %d frame' % (list[i], count))

                frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
                if count < count_end and (count - count_start) % 4 == 0:
                    if flag == True:
                        writer_p.writeFrame(frame[:,:,::-1])
                        # count_no_person = 0
                    else:
                        writer_np.writeFrame(frame[:,:,::-1])
                        # count_no_person += 1
                count += 1

        video1.release()
        # video2.release()
        if os.path.exists(person_dir + '/' + list[i]):
            writer_p.close()
        if os.path.exists(no_person_dir + '/' + list[i]):
            writer_np.close()