### 项目内容

#### backend

- utils.py：socket处理文件

- cutoff.py：数据文件

- server.py：socket服务器端

  包含基于Flask框架的后端模块

- client.py：socket客户端

  包含基于Flask框架的后端模块

#### sys-frontend

基于naive admin ui开发，采用Vue3 + Vite2 + TS.

#### cli-frontend

原生开发，采用Vue3 + Vite2 + TS.

### 工作说明

1. 通过命令行直接运行server.py和client.py，实现支持多连接的半双工通信。

2. GUI模块：

   前端：sys-frontend: cd进入对应文件夹后，运行yarn add安装依赖，执行yarn dev运行在web上。

   ​			cli-frontend: cd进入对应文件夹后，运行npm i 安装依赖，执行npm run dev运行在web上。

   后端：backend中的server.py和client.py

### 现有问题

由于socket通信需要在端口A打开服务器，而flask作为后端为前端网页提供支持时需要在同一个程序进程中在端口B打开服务器，由于操作系统的安全策略，会造成**“OSError: [WinError 10048] 通常每个套接字地址(协议/网络地址/端口)只允许使用一次”**。

因此暂时GUI无法和socket一起正常工作，只能够进行模块分离测试。