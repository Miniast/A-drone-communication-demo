### 使用指南
运行server.py打开服务器，此后可并发运行client.py进行无人机客户端模拟。

### 无人机客户端：

#### 运行过程

1. 使用指定密钥进行初步鉴权，与服务器建立连接。
2. 通过初步鉴权后，通过一对标识符（user，pwd）进行身份注册与身份标识（二次鉴权），作为临时识别码。
3. 指定数据包进行通信

#### 实现功能与技术路线

- 通过定义好的加密与解密接口（可在utils.py文件中修改）与服务端进行socket通信
- 支持多客户端并发（同一AP控制多台无人机）
- 生成运行日志

### 服务端：

#### 运行过程

1. 服务器开始运行，等待客户端连接
2. 处理通信数据包
3. 断开连接与服务器关闭

#### 实现功能与技术路线

- 错误处理
- 生成运行日志