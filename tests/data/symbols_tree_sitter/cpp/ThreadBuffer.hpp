#pragma once
#include <mutex>
#include <queue>

template <typename T>
class FrameBuffer : public std::queue<T>
{
public:
    unsigned int frameCount;
    FrameBuffer() : frameCount(0) { mutex = new std::mutex(); };

    void pushFrame(const T &FrameBuffering)
    {
        std::lock_guard<std::mutex> lock(*mutex);

        std::queue<T>::push(FrameBuffering);
        frameCount += 1;
    }

    T getFrame()
    {
        std::lock_guard<std::mutex> lock(*mutex);
        T lastestFrame = this->front();
        this->pop();
        frameCount -= 1;
        return lastestFrame;
    }

    T peekFrame()
    {
        std::lock_guard<std::mutex> lock(*mutex);
        T lastestFrame = this->front();
        return lastestFrame;
    }

    void clearBuffer()
    {
        std::lock_guard<std::mutex> lock(*mutex);
        while (!this->empty())
            this->pop();
    }

private:
    std::mutex *mutex;
};