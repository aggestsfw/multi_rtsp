// multi_rtsp.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//

//#include <iostream>
#include "video_streaming.h"

int main()
{
    //// 打开视频文件
    //cv::VideoCapture cap("D:/data_dir/录像/轮询.mp4");
    //if (!cap.isOpened()) {
    //    std::cerr << "无法打开视频文件。" << std::endl;
    //    return -1;
    //}

    //// 获取视频帧率和总帧数
    //double fps = cap.get(cv::CAP_PROP_FPS);
    //int frameCount = static_cast<int>(cap.get(cv::CAP_PROP_FRAME_COUNT));

    //// 设置输出文件名和帧率
    //std::string outputFileName = "D:/data_dir/录像/output.gif";
    //cv::VideoWriter writer(outputFileName, cv::VideoWriter::fourcc('G', 'I', 'F', ' '), fps, cv::Size(640, 480));

    //// 逐帧读取视频并写入 GIF 文件
    //cv::Mat frame;
    //while (cap.read(frame)) {
    //    // 可以对帧进行处理，这里直接写入
    //    writer.write(frame);
    //}

    //// 释放资源
    //cap.release();
    //writer.release();

    //std::cout << "转换完成！" << std::endl;

    //exit(1);

	//修改视频目录
	std::ifstream input_file("/home/zeng/win/workdir/cmdt/multi_rtsp/1/video.txt");
	int num_threads = 8;
	std::vector<std::string> lines;
	if (input_file.is_open())
	{
		std::string line;
        std::string target = "\r";
		while (std::getline(input_file, line))
		{
            size_t pos = 0;
            if ((pos = line.find(target, pos)) != std::string::npos)
            {
                line.replace(pos, target.length(), "");
            }
			lines.push_back(line);
		}
	}

	printf("haha");

//    cv::VideoCapture cap("/home/zeng/win/workdir/cmdt/multi_rtsp/1/000.mp4");

	//输入true表示多线程轮询模式，输入false表示普通多线程模式
	VideoStreaming* vs = new VideoStreaming(num_threads, lines, false);
	vs->Init();
	vs->Process();

}
