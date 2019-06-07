import paramiko

transport = paramiko.Transport(('192.168.220.135', 22))
transport.connect(username='root', password='hacker')

sftp = paramiko.SFTPClient.from_transport(transport)

sftp.get('/root/Linux.txt', 'Linux.txt')  # 将Linux上的/root/Linux.txt下载到本地

import os  # Python的标准库中的os模块包含普遍的操作系统功能
import re  # 引入正则表达式对象
import urllib  # 用于对URL进行编解码
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler  # 导入HTTP处理相关的模块


# 自定义处理程序，用于处理HTTP请求
class TestHTTPHandler(BaseHTTPRequestHandler):
    # 处理GET请求
    def do_GET(self):
        # 页面输出模板字符串
        templateStr = '''''   
<html>   
<head>   
<title>QR Link Generator</title>   
</head>   
<body>   
%s 
<br>   
<br>   
<form action="/qr" name=f method="GET"><input maxLength=1024 size=70   
name=s value="" title="Text to QR Encode"><input type=submit   
value="Show QR" name=qr>   
</form> 
</body>   
</html> '''

        # 将正则表达式编译成Pattern对象

        pattern = re.compile(r'/qr\?s=([^\&]+)\&qr=Show\+QR')
        # 使用Pattern匹配文本，获得匹配结果，无法匹配时将返回None
        match = pattern.match(self.path)
        qrImg = ''

        if match:
            # 使用Match获得分组信息
            qrImg = '<img src="http://chart.apis.google.com/chart?chs=300x300&cht=qr&choe=UTF-8&chl=' + match.group(
                1) + '" /><br />' + urllib.unquote(match.group(1))

        self.protocal_version = 'HTTP/1.1'  # 设置协议版本
        self.send_response(200)  # 设置响应状态码
        self.send_header("Welcome", "Contect")  # 设置响应头
        self.end_headers()
        self.wfile.write(templateStr % qrImg)  # 输出响应内容


# 启动服务函数
def start_server(port):
    http_server = HTTPServer(('', int(port)), TestHTTPHandler)
    http_server.serve_forever()  # 设置一直监听并接收请求


os.chdir('static')  # 改变工作目录到 static 目录
start_server(8000)  # 启动服务，监听8000端口

import socket


def handle_request(client):
    buf = client.recv(1024)
    client.send("HTTP/1.1 200 OK\r\n\r\n")
    client.send('<h30>Hello World</h10>')


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('192.168.68.128', 8006))
    sock.listen(1)
    while True:
        connection, address = sock.accept()
        handle_request(connection)
        connection.close()


if __name__ == '__main__':
    main()
