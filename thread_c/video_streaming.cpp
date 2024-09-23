#include "video_streaming.h"

VideoStreaming::VideoStreaming(int num_threads, std::vector<std::string>& addrs, bool is_polling)
	:num_threads_(num_threads), addrs_(addrs), is_polling_(is_polling)
{
    num_addrs_ = addrs_.size();
}

VideoStreaming::~VideoStreaming()
{

}

void VideoStreaming::Init() {
    //打开视频路数
    for (size_t i = 0; i < num_addrs_; i++)
    {
        cv::VideoCapture cap(addrs_[i]);
//        int frameCount = static_cast<int>(cap.get(cv::CAP_PROP_FRAME_COUNT));
        caps_.push_back(cap);
        //std::string name_win = "win_" + std::to_string(i);
        //cv::namedWindow(name_win, cv::WINDOW_NORMAL);
    }
    //打开窗口
    if (is_polling_)
    {
        //for (size_t i = 0; i < num_threads_; i++)
        //{
        //    std::string name_win = "win_" + std::to_string(i);
        //    cv::namedWindow(name_win, cv::WINDOW_NORMAL);
        //}
    }
}

//多线程同时显示
void VideoStreaming::PerceptionCallBack(const int& cap_id) {

    while (true)
    {
        cv::Mat frame;
        caps_[cap_id] >> frame;
        if (frame.empty())
        {
            break;
        }
        std::string name_win = "win_" + std::to_string(cap_id);
//        cv::namedWindow(name_win, cv::WINDOW_AUTOSIZE);
        mux_.lock();//不加锁的话，imshow会显示不了
        cv::namedWindow(name_win, cv::WINDOW_NORMAL);
        cv::resizeWindow(name_win, 320, 192);
        cv::imshow(name_win, frame);
        printf("处理了视频%d\n", cap_id);
        cv::waitKey(1);
        mux_.unlock();
    }
}

void VideoStreaming::ProcessPool() {
    int num_blocks = num_addrs_ / num_threads_;
    int num_res = num_addrs_ % num_threads_;
    //多线程处理
    ThreadPool* pool = new ThreadPool(num_threads_); // 创建一个有4个线程的线程池
    //处理前面的满线程的块
    for (int i = 0; i < num_blocks; ++i) {
        for (int j = 0; j < num_threads_; ++j) {
            int cap_id = i * num_threads_ + j;
            // 向线程池中添加任务
            pool->enqueue(&VideoStreaming::PerceptionCallBack, this, cap_id);
        }
    }
    //处理最后一个不满线程的块
    for (int i = 0; i < num_res; ++i) {
        int cap_id = num_blocks * num_threads_ + i;
        // 向线程池中添加任务
        pool->enqueue(&VideoStreaming::PerceptionCallBack, this, cap_id);
    }
    delete pool;//注意这里要先销毁线程池，才能做后面的，不然会有问题
}

//固定开几个窗口轮询
void VideoStreaming::PerceptionPollingCallBack(const int& cap_id) {
    cv::Mat frame;
    caps_[cap_id] >> frame;
    if (frame.empty())
    {
        return;
    }
    int win_num = cap_id % num_threads_;
    std::string name_win = "win_" + std::to_string(win_num);
//    cv::namedWindow(name_win, cv::WINDOW_NORMAL);
    mux_.lock();//不加锁的话，imshow会显示不了
    cv::namedWindow(name_win, cv::WINDOW_NORMAL);
    cv::resizeWindow(name_win, 320, 192);
    cv::imshow(name_win, frame);

    printf("处理了视频%d\n", cap_id);

    cv::waitKey(1);
    mux_.unlock();
    //cv::destroyWindow(name_win);
}

void VideoStreaming::ProcessPollingPool() {
    int num_blocks = num_addrs_ / num_threads_;
    int num_res = num_addrs_ % num_threads_;
    //多线程处理
    ThreadPool* pool = new ThreadPool(num_threads_); // 创建一个有4个线程的线程池

    for (size_t query_i = 0; query_i < 1000; query_i++)
    {
        //处理前面的满线程的块
        for (int i = 0; i < num_blocks; ++i) {
            for (int j = 0; j < num_threads_; ++j) {
                int cap_id = i * num_threads_ + j;
                // 向线程池中添加任务
                pool->enqueue(&VideoStreaming::PerceptionPollingCallBack, this, cap_id);
            }
        }
        //处理最后一个不满线程的块
        for (int i = 0; i < num_res; ++i) {
            int cap_id = num_blocks * num_threads_ + i;
            // 向线程池中添加任务
            pool->enqueue(&VideoStreaming::PerceptionPollingCallBack, this, cap_id);
        }
    }
    delete pool;//注意这里要先销毁线程池，才能做后面的，不然会有问题
}

void VideoStreaming::Process() {
    if (is_polling_)
    {
        ProcessPollingPool();
    }
    else
    {
        ProcessPool();
    }
}