# XshellScript

本项目为Xshell嵌入式自动化脚本，封装了Xshell官方提供的接口，使得脚本更加便于书写。

## 使用方法

![image-20230715124537899](C:\Users\10124\AppData\Roaming\Typora\typora-user-images\image-20230715124537899.png)

TestServer.py脚本用于模拟真实的服务器，会通过多线程方式在多个端口同时启动模拟服务器。1200端口只是回显收到的字符串；1201端口模拟一个linux服务器，支持cd/pwd/ls/cp命令；1202和1203端口模拟sftp服务器，支持cd和get/put命令；1204端口模拟一个升级服务器，只支持update升级命令。

运行样例脚本前应该先运行TestServer.py。

### 1、下载项目到本地

### 2、打开Xshell快速命令拦/窗格

![image-20230715125308528](C:\Users\10124\AppData\Roaming\Typora\typora-user-images\image-20230715125308528.png)

### 3、添加按钮并选择运行脚本

![image-20230715125811420](C:\Users\10124\AppData\Roaming\Typora\typora-user-images\image-20230715125811420.png)

### 4、Xshell打开单进程模式（不打开单进程，无法在多个会话之间切换）

![image-20230715125954678](C:\Users\10124\AppData\Roaming\Typora\typora-user-images\image-20230715125954678.png)

### 5、点击运行脚本

![image-20230715131010868](C:\Users\10124\AppData\Roaming\Typora\typora-user-images\image-20230715131010868.png)