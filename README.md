# message-channel

## 安装

1. 安装redis-serger
    ```shell
    # Linux
    sudo apt install redis
    redis-server
    
    # MacOS
    brew install redis
    brew services start redis
    
    # other: www.google.com | www.baidu.com
    ```
    
2. 安装python依赖

    ```shell
    pip3 install -r requirements.txt
    ```

## 使用

```bash
uvicorn app.main.message_channel --reloard
```

## API文档

详细文档见：[**localhost:8000/docs**](http://localhost:8000/docs)
