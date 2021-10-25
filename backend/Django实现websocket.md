## 初识 websocket

### **一. WebSocket 简介**

![img](https://pic2.zhimg.com/80/v2-cfa1bb15b6ffe66e07f6e0955ff45981_1440w.jpg)

`WebSocket` 是一种基于 `TCP` 的**网络协议**。在 2009 年诞生，于 2011 年被 IETF 定为标准 `RFC 6455` 通信标准，并由 `RFC7936` 补充规范。`WebSocket API` 也被 `W3C` 定为标准。

`WebSocket` 也是一种**全双工通信**的协议，既允许客户端向服务器主动发送消息，也允许服务器主动向客户端发送消息。在 `WebSocket` 中，浏览器和服务器只需要完成一次握手，两者之间就可以建立持久性的连接，进行双向数据传输。

### **二. WebSocket 特点**

1. 连接握手阶段使用 `HTTP` 协议，在此之前已经完成TCP/IP的三次握手；
2. 协议标识符是 `ws`，如果采用加密则是 `wss`；
3. 数据格式比较轻量，性能开销小，通信高效；
4. 没有同源限制，客户端可以与任意服务器通信；
5. 建立在 `TCP` 协议之上，服务器端的实现比较容易；
6. 通过 `WebSocket` 可以发送文本，也可以发送二进制数据；
7. 与 `HTTP` 协议有着良好的兼容性。默认端口也是 `80` 和 `443`，并且握手阶段采用 `HTTP` 协议，因此握手时不容易屏蔽，能通过各种 `HTTP` 代理服务器；

### **三. 为什么需要 WebSocket？**

谈起为什么需要 `WebSocket` 前，那得先了解在没有 `WebSocket` 那段时间说起，那时候基于 `Web` 的消息基本上是靠 `Http` 协议进行通信，而经常有”**聊天室**”、”**消息推送**”、”**股票信息实时动态**”等这样需求，而实现这样的需求常用的有以下几种解决方案：

![img](https://pic3.zhimg.com/80/v2-51d2bee236d3827c63b2b86ca6e4042e_1440w.jpg)

#### **1. 短轮询(Traditional Polling)**

短轮询是指客户端每隔一段时间就询问一次服务器是否有新的消息，如果有就接收消息。这样方式会增加很多次无意义的发送请求信息，每次都会耗费流量及处理器资源。

**优点**：短连接，服务器处理简单，支持跨域、浏览器兼容性较好。

**缺点**：有一定延迟、服务器压力较大，浪费带宽流量、大部分是无效请求。

#### **2. 长轮询(Long Polling)**

长轮询是段轮询的改进，客户端执行 `HTTP` 请求发送消息到服务器后，等待服务器回应，如果没有新的消息就一直等待，直到服务器有新消息传回或者超时。

这也是个反复的过程，这种做法只是减小了网络带宽和处理器的消耗，但是带来的问题是导致消息实时性低，延迟严重。而且也是基于循环，最根本的带宽及处理器资源占用并没有得到有效的解决。

**优点**：减少轮询次数，低延迟，浏览器兼容性较好。

**缺点**：服务器需要保持大量连接。

#### **3. 服务器发送事件(Server-Sent Event)**

> 目前除了 `IE/Edge`，其他浏览器都支持。

服务器发送事件是一种服务器向浏览器客户端发起数据传输的技术。一旦创建了初始连接，事件流将保持打开状态，直到客户端关闭。该技术通过传统的 `HTTP` 发送，并具有 `WebSockets` 缺乏的各种功能，例如”自动重新连接”、”**事件ID**” 及 “**发送任意事件**”的能力。

> 服务器发送事件是单向通道，只能服务器向浏览器发送，因为流信息本质上就是下载。

**优点**：适用于更新频繁、低延迟并且数据都是从服务端发到客户端。

**缺点**：浏览器兼容难度高。

#### **总结**

显然，上面这几种方式都有各自的优缺点，虽然靠轮询方式能够实现这些一些功能，但是其对性能的开销和低效率是非常致命的，尤其是在移动端流行的现在。

现在客户端与服务端双向通信的需求越来越多，且现在的浏览器大部分都支持 `WebSocket`。所以对实时性和双向通信及其效率有要求的话，比较推荐使用 `WebSocket`。

### **四. * WebSocket 连接流程**

#### 1. 客户端发起握手请求

客户端先用带有 `Upgrade:Websocket` 请求头的 `HTTP` 请求，向服务器端发起连接请求，实现握手(`HandShake`)。

客户端 `HTTP` 请求的 `Header` 头信息如下：

```text
Connection: Upgrade
Sec-WebSocket-Extensions: permessage-deflate; client_max_window_bits
Sec-WebSocket-Key: IRQYhWINfX5Fh1zdocDl6Q==
Sec-WebSocket-Version: 13
Upgrade: websocket
```

- `Connection`： Upgrade 表示要升级协议。
- `Upgrade`： Websocket 要升级协议到 websocket 协议。
- `Sec-WebSocket-Extensions`： 表示客户端所希望执行的扩展(如消息压缩插件)。
- `Sec-WebSocket-Key`：浏览器生成的随机字符串， 用于WebSocket协议的校验，对应服务端响应头的 `Sec-WebSocket-Accept`。
- `Sec-WebSocket-Version`： 表示 `websocket` 的版本。如果服务端不支持该版本，需要返回一个`Sec-WebSocket-Versionheader`，里面包含服务端支持的版本号。

#### 2. 服务器加密随机字符串

- 从请求【握手】信息中提取 Sec-WebSocket-Key
- 利用magic_string 和 Sec-WebSocket-Key 进行hmac1加密，再进行base64加密

*注：magic string为：258EAFA5-E914-47DA-95CA-C5AB0DC85B11*    全球公认的固定字符串

```python
# 伪代码
import hashlib
import base64

magic_string = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
socket_key = headers['Sec-WebSocket-Key']

# 将客户端传过来的随机字符串和magic_string拼接，sha1加密
cipher1 = hashlib.sha1((socket_key + magic_string).encode('utf-8')).digist()
cipher2 = base64.b64encode(cipher1)
```



#### 3. 服务器将密文返回给客户端

服务端响应的 HTTP Header 头信息如下：

```text
Connection: upgrade
Sec-Websocket-Accept: TSF8/KitM+yYRbXmjclgl7DwbHk=
Upgrade: websocket
```

- `Connection`： Upgrade 表示要升级协议。
- `Upgrade`： Websocket 要升级协议到 websocket 协议。
- `Sec-Websocket-Accept`： 对应 `Sec-WebSocket-Key` 生成的密文，返回给客户端，让客户端对此值进行校验，证明服务端支持 `WebSocket`。



#### 4. 客户端校验服务器密文

客户端同样会根据握手时生成的随机字符串和 magic_string 生成一段密文，并同服务器返回的密文进行对比、校验。

若通过，则说明两端用的同一个magic string，同一种加密手段，即可以判定服务端支持websocket协议，握手成功；若校验不通过，则代表服务端不支持websocket协议，握手失败。

握手成功后，由 `HTTP` 协议升级成 `Websocket` 协议，进行长连接通信，两端相互传递信息。



### 五、* WebSocket 收发数据

收发数据：**数据是加密的**

- 浏览器将数据加密发往服务端

- 服务端接收到数据之后进行的解密（解密是全球公认的）

  -  拿到第2个字节（8位），取其后7位(即前两个字节的10-16位)，也就是数据的前9位都不要，我们取到的7位称之为payload length（7位最大值是127）；

  -  服务端对payload length的值进行判断：

    - 若payload length =  127：
      再往后读8个字节（64位），也就是说前10个字节(8+2)是数据头，剩余字节是 数据
    -  若payload length =  126：
      再往后读2个字节（16位），也就是说前4个字节(2+2)是数据头，剩余字节是 数据
    - 若payload length <= 125：
      不再往后读，前面2个字节就是数据头，剩余字节是 数据

  - 通过前面解密过程获取到的数据，仍然不是明文，还需要再解密

    - 获取到数据部分后，读取前4个字节，这4个字节称之为**masking key**，剩下部分是真正的密文数据；

    - 让masking key与数据的每一个字节进行位运算（异或运算），运算完之后就获取到了最终的铭文数据；

      ```python
      # 伪代码
      var decrypt_text = ''
      for index, b in enuencrypt_byte(encrypt_text):
        decrypt_text += b ^ MASK[index % 4]  # MASK 就是 masking key
      ```

      

### **六. WebSocket 使用场景**

1. **数据流状态**： 比如说上传下载文件，文件进度，文件是否上传成功。
2. **协同编辑文档**： 同一份文档，编辑状态得同步到所有参与的用户界面上。
3. **多玩家游戏**： 很多游戏都是协同作战的，玩家的操作和状态肯定需要及时同步到所有玩家。
4. **多人聊天**： 很多场景下都需要多人参与讨论聊天，用户发送的消息得第一时间同步到所有用户。
5. **社交订阅**： 有时候我们需要及时收到订阅消息，比如说开奖通知，比如说在线邀请，支付结果等。
6. **股票虚拟货币价格**： 股票和虚拟货币的价格都是实时波动的，价格跟用户的操作息息相关，及时推送对用户跟盘有很大的帮助。





## Django 实现 WebSocket

Django 本身不支持websocket，需要安装第三方插件。

1. 安装第三方插件：

   ```python
   pip3 install channels
   ```

2. 创建项目和app：

   ```python
   django-admin startproject backend  # 创建django项目
   
   # 进入到项目目录，创建app
   python3 manage.py startapp chatroom
   ```

3. settings.py 配置：

   1. 注册channels

      ```python
      INSTALLED_APPS = [
          'django.contrib.admin',
          'django.contrib.auth',
          'django.contrib.contenttypes',
          'django.contrib.sessions',
          'django.contrib.messages',
          'django.contrib.staticfiles',
          
          'channels'
      ]
      ```

   2. 添加配置参数 ASGI_APPLICATION

      ```python
      ASGI_APPLICATION = 'backend.asgi.application'
      ```

4. 修改asgi.py文件

   ```python
   import os
   
   from django.core.asgi import get_asgi_application
   from channels.routing import ProtocolTypeRouter, URLRouter
   
   from . import routing
   
   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
   
   # application = get_asgi_application()
   
   application = ProtocolTypeRouter({  # 通过协议类型分发路由
       'http': get_asgi_application(),
       'websocket': URLRouter(routing.websocket_urlpatterns)
   })
   ```

5. 在settings.py 文件的同级目录下创建 routing.py 文件

   ```python
   # 本文件是asgi在项目中的主路由文件。等价于wsgi在本目录中的urls.py文件
   from django.urls import re_path
   
   from apps.chatroom import consumers
   
   websocket_urlpatterns = [
       re_path(r'chat/(?P<group>\w+)/$', consumers.ChatConsumer.as_asgi())
   ]
   ```

6. 在app chatroom中，添加consumers.py文件

   ``` python
   # 本文件是asgi在app中的视图文件。等价于wsgi在本目录中的views.py文件。
   from channels.generic.websocket import WebsocketConsumer
   from channels.exceptions import StopConsumer
   
   class ChatConsumer(WebsocketConsumer):
       def websocket_connect(self, message):
           # 客户端向服务端发送websocket连接请求时，自动触发。
           # 服务端允许客户端创建连接
           self.accept()
   
       def websocket_receive(self, message):
           # 客户端基于websocket向服务器发送数据是，自动触发。
           print(message)
           self.send("欢迎大哥光临！")
   
           # 服务器也可以主动断开连接
           # self.close()
   
       def websocket_disconnect(self, message):
           # 客户端与服务器断开连接时，自动触发。
           raise StopConsumer
   ```

7. 至此一个基础的Django-websocket框架就搭建好了

   ```
   python3 manage.py runserver
   ```



## Vue 2.x 项目构建

Vue 3.x问题稍多，再过一年再用。

1. 创建vue3.x项目

   ``` shell
   vue create project_name
   
   // 自定义配置，vue版本选择2.x
   ```

2. 引入vuetify组件库

   相对 element-ui 更花里胡哨的组件库。

   ```shell
   cd project_name
   vue add vuetify
   
   # 其他配置，为了使用vuetify的组件样式，将项目的App.vue中，<router-view/> 放到<v-app>标签中
   ```

   官方文档：https://vuetifyjs.com/zh-Hans/getting-started/installation/

   

## Channels Layers 实现多人聊天

- Settings.py 文件配置

  - 基于内存实现channels layers

    ```python
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels.layers.InMemoryChannelLayer",
        }
    }
    ```

  - 基于redis实现channel layers

    安装第三方插件：

    ```python
    pip3 install channels-redis
    ```

    配置settings

    ```python
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": ["redis://:password@121.4.47.229:6330/10"]
            }
        }
    }
    ```

- consumers.py文件修改

  ```python
  from channels.generic.websocket import WebsocketConsumer
  from channels.exceptions import StopConsumer
  from asgiref.sync import async_to_sync
  
  
  class ChatConsumer(WebsocketConsumer):
      def websocket_connect(self, message):
          # 客户端向服务端发送websocket连接请求时，自动触发。
          # 服务端允许客户端创建连接
          self.accept()
  
          # 获取url参数中的group
          group = self.scope['url_route']['kwargs'].get('group')
  
          # 将客户端连接对象加入到channel-layer
          # 将异步的channel-layer转成同步方法
          if group:
              async_to_sync(self.channel_layer.group_add)(group, self.channel_name)
  
      def websocket_receive(self, message):
          # 服务器也可以主动断开连接
          if message['text'] == 'exit':
              self.close()
              # 主动引发断开异常，将不再调用websocket_disconnect
              raise StopConsumer
  
          # 获取url参数中的group
          group = self.scope['url_route']['kwargs'].get('group')
  
          # 客户端基于websocket向服务器发送数据时，自动触发本方法。
          if group:
              async_to_sync(self.channel_layer.group_send)(group, {"type": "call", "msg": message})
  
      def call(self, event):
          """回调函数，实现向客户端发送消息"""
          text = event['msg']['text']
          self.send(text)
  
      def websocket_disconnect(self, message):
          # 获取url参数中的group
          group = self.scope['url_route']['kwargs'].get('group')
  
          # 某个客户端断开连接时，将其从group中删除
          async_to_sync(self.channel_layer.group_discard)(group, self.channel_name)
  
          # 客户端与服务器断开连接时，自动触发。
          raise StopConsumer
  ```

  