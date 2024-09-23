#ifndef VIDEO_STREAMING_H
#define VIDEO_STREAMING_H

#include <vector>
#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <map>
#include <memory>
#include <numeric>

#include <thread>
#include <mutex>
#include <queue>
#include <condition_variable>
#include <functional>

#include "opencv2/opencv.hpp"

class ThreadPool {
public:
    ThreadPool(size_t threads) : stop(false) {
        for (size_t i = 0; i < threads; ++i) {
            workerThreads.emplace_back(
                [this] {
                    while (true) {
                        std::function<void()> task;

                        {
                            std::unique_lock<std::mutex> lock(this->queueMutex);
                            this->condition.wait(lock,
                                [this] { return this->stop || !this->tasks.empty(); });
                            if (this->stop && this->tasks.empty())
                                return;
                            task = std::move(this->tasks.front());
                            this->tasks.pop();
                        }

                        task();
                    }
                }
            );
        }
    }

    template<class F, class... Args>
    void enqueue(F&& f, Args&&... args) {
        auto task = std::bind(std::forward<F>(f), std::forward<Args>(args)...);

        {
            std::unique_lock<std::mutex> lock(queueMutex);
            if (stop)
                throw std::runtime_error("enqueue on stopped ThreadPool");

            tasks.emplace(task);
        }
        condition.notify_one();
    }

    ~ThreadPool() {
        {
            std::unique_lock<std::mutex> lock(queueMutex);
            stop = true;
        }
        condition.notify_all();
        for (std::thread& worker : workerThreads)
            worker.join();
    }

private:
    std::vector<std::thread> workerThreads;
    std::queue<std::function<void()>> tasks;

    std::mutex queueMutex;
    std::condition_variable condition;
    bool stop;
};

class VideoStreaming
{
public:
    VideoStreaming(int num_threads, std::vector<std::string>& addrs, bool is_polling);
    ~VideoStreaming();

    void Init();
    void Process();

    void PerceptionCallBack(const int& cap_id);
    void ProcessPool();
    //轮询机制
    void PerceptionPollingCallBack(const int& cap_id);
    void ProcessPollingPool();

private:
    bool is_polling_{ false };
    int num_threads_;
    std::vector<std::string> addrs_;
    std::vector<cv::VideoCapture> caps_;
    int num_addrs_;
    std::mutex mux_;
};



#endif // !VIDEO_STREAMING_H
