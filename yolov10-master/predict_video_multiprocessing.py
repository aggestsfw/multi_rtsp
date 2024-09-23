import shutil

from ultralytics import YOLOv10
from PIL import Image
import cv2
import os
import skvideo.io
from tqdm import tqdm
import multiprocessing as mp
from functools import partial

def get_filelist(dir):
    Filelist = []
    for home, dirs, files in os.walk(dir):
        for filename in files:
            # 文件名列表，包含完整路径
            # Filelist.append(os.path.join(home, filename).replace('\n', '').replace('\r', '').replace('\\', '/'))
            # # 文件名列表，只包含文件名
            Filelist.append( filename)
    return Filelist

def YoloFilter(index, list, num_process, models):
    i = index
    video1 = cv2.VideoCapture(data_dir + '/' + list[i])
    # 获取视频文件的帧率、宽度和高度
    fps = video1.get(cv2.CAP_PROP_FPS)
    width = int(video1.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video1.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # '-f': 'mp4', '-b': '300000000'
    writer_p = skvideo.io.FFmpegWriter(person_dir + '/' + list[i], outputdict={'-r': str(fps), \
                                                                               '-vcodec': 'libx265'})
    writer_np = skvideo.io.FFmpegWriter(no_person_dir + '/' + list[i], outputdict={'-r': str(fps), \
                                                                                   '-vcodec': 'libx265'})
    # video2.set(cv2.CAP_PROP_BITRATE, 30000)
    step = 40
    step1 = step
    count = 0
    flag = False
    count_start = 0
    count_end = 0
    while video1.isOpened():
        ret, frame = video1.read()
        if not ret:
            break
            # 显示预测后的图片
        else:
            if count % step1 == 0:
                count_start = count
                count_end = count + step1
                results = models[int(i % num_process)].predict(frame)
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
                    writer_p.writeFrame(frame[:, :, ::-1])
                else:
                    writer_np.writeFrame(frame[:, :, ::-1])
            count += 1

    video1.release()
    if os.path.exists(person_dir + '/' + list[i]):
        writer_p.close()
    if os.path.exists(no_person_dir + '/' + list[i]):
        writer_np.close()

if __name__ == '__main__':


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
    index = []
    for i in tqdm(range(len(list))):
        index.append(i)

    print("开始建立进程池\n")
    # num_process = int(mp.cpu_count() * 0.8)
    num_process = 8
    #建立Model
    models = []
    for i in range(num_process):
        # model里存放下载好的yolov10n.pt的路径信息
        print('load %d model\n' % i)
        model = YOLOv10(model='/home/zeng/win/workdir/cmdt/yolov10-main/yolov10-master/yolov10x.pt')
        models.append(model)

    p = mp.Pool(processes=num_process)#processes=mp.cpu_count()
    # func = partial(calc_score, images=images, points3d=points3d, args=args, extrinsic=extrinsic)
    func = partial(YoloFilter, list=list, num_process=num_process, models=models)
    p.map(func, index)