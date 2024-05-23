import uvicorn

if __name__ == "__main__":
    is_dev = False
    uvicorn.run(
        app="jiucai_api:news_agent_app",
        host="0.0.0.0",  # 设置监听地址
        port=6007,  # 设置监听端口
        log_level="debug" if is_dev else "info",  # 设置日志级别
        workers=1,  # 设置工作进程数量
        reload=False,
    )