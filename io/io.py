#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import select

class Request(object):
    '''还是执行自己的fileno方法'''

    def __init__(self, sock, info):
        self.sock = sock
        self.info = info

    def fileno(self):
        return self.sock.fileno()


class QinBing(object):
    def __init__(self, ):
        self.sock_list = []
        self.conns = []

    def add_request(self, req_info):
        '''
        req_info :  {'host':'www.baidu.com','port':80,'path':'/'}
        创建请求
        :return:
        '''
        sock = socket.socket()
        sock.setblocking(False)  # 设置不阻塞
        try:
            sock.connect((req_info['host'], req_info['port']))
        except BlockingIOError as e:
            pass

        obj = Request(sock, req_info)
        self.sock_list.append(obj)
        self.conns.append(obj)

    def run(self):
        '''
        开始事件循环: 连接成功?数据是否成功返回?
        :return:
        '''
        while True:
            # select.select([sock对象])
            # 可以是任何对象,对象一定要有fileno方法
            # select 执行的是对象的fielno方法 让操作系统来检测返回值
            r, w, e = select.select(self.sock_list, self.conns, [], 0.05)
            # w  是否连接成功
            for obj in w:
                # 检查obj:request对象
                # socket {'host':'www.baidu.com','port':80,'path':'/'}
                data = 'GET %s HTTP/1.1\r\nHost:%s\r\n\r\n' % (obj.info['path'], obj.info['host'])
                obj.sock.send(data.encode('utf-8'))
                self.conns.remove(obj)  # del obj  防止重复发送
            # r 数据返回,接收到数据
            for obj in r:
                response = obj.sock.recv(8096)
                print(obj.info['host'], response)
                self.sock_list.remove(obj)  # del obj 防止重复接收

            # 所有的请求已经返回
            if not self.sock_list:
                break


url_list = [
    {'host': 'www.baidu.com', 'port': 80, 'path': '/'},
    {'host': 'www.bing.com', 'port': 80, 'path': '/'},
    {'host': 'www.qq.com', 'port': 80, 'path': '/'},
]

obj = QinBing()
for item in url_list:
    obj.add_request(item)

obj.run()
