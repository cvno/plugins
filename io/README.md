## 异步IO模块 多路复用
**待优化**
### 1. socket 发送http
- GET/POST请求要写Host
- POST发送数据要写`Content-Length`,`Content-Type`
- 请求非阻塞`req.setblocking(False)` or 设置为 0
### 2. IO多路复用原理
IO多路复用是指内核一旦发现进程指定的一个或者多个IO条件准备读取，它就通知该进程

**用来检测多个socket对象是否有变化**

结论:
>1. 发送Http请求
>2. 设置为非阻塞
>3. try: 捕捉报错区域
>4. 定义一些操作
```python
# socket 代码
# 异步IO 伪代码
import socket,time

def conf(ip, url, path, port=80, ):
    v=len('k1=v1&k2=v2\r\n')
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.setblocking(False)  # 非阻塞
    try:
        # 异步IO原理  ->死循环 -> 连接成功之后通知
        client.connect((ip, port))  # 请求已经发送出去  # 阻塞
    except BlockingIOError as e :
        print(e)
    time.sleep(5)    # 计算
    data = bytes('GET %s?k1=v1&k2=v2 HTTP/1.1\r\nHost: %s\r\nContent-Length:%d\r\nContent-Type: application/x-www-form-urlencoded\r\nConnection: close\r\n\r\nk1=v1&k2=v2\r\n' % (path,url,v), encoding='utf8')
    client.send(data)  # headers
    time.sleep(5)  # 计算
    # 异步IO原理 ->死循环 -> 连接成功之后通知
    print(client.recv(1024))    # 阻塞
    client.close()

if __name__ == '__main__':
    conf(ip='61.135.169.121', url='www.baidu.com', path='/')
    # conf(ip='127.0.0.1', url='127.0.0.1', path='/login.html')
```
### 3. IO多路复用 select
- 知识点
    - client.setblocking(False) 不阻塞
    - select.select检测：连接成功，数据回来了 
```python
import select,socket
socket_list = []
for i in [www.baid.......,.....]:
    client = socket.socket()
    client.setblocking(False)
    # 连接
    try:
        client.connect((i,80)) # 连接的请求已经发送出去，
    except BlockingIOError as e:
        print(e)
    socket_list.append(client)

# 事件循环    
while True:
    # 0.05 is out time 超时时间
    r,w,e = select.select([sk1,sk2...],[],[],0.05)
    # w [sk1,sk2...] 谁连接成功了 就是谁
    for obj in w:
        obj.send('GET / HTTP/1.1\r\n...')
    # r 检测第一个列表的对象,如果出现变化就返回它   可读 -> 收数据
    for obj in r:
        response = obj.recv(...)
```


# 使用

```python
# 导入模块
from .io import QinBing

# 自定义回调函数
def done(response):
    print(response)

# url 参数 
url_list = [
    {'host': 'www.baidu.com', 'port': 80, 'path': '/','callback':[done,]},  # 如果是列表循环取出来
    {'host': 'www.bing.com', 'port': 80, 'path': '/','callback':[done]},
    {'host': 'www.qq.com', 'port': 80, 'path': '/','callback':[done]},
]

# 使用
obj = QinBing()
for item in url_list:
    obj.add_request(item)

obj.run()

```

