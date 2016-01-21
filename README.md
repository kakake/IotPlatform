# IotPlatform
物联网平台，通过访问www.efwplus.cn网站来控制raspberryPI主机，操作相关设备，如：遥控器、温度湿度传感器、摄像头等

![](https://raw.githubusercontent.com/kakake/IotPlatform/master/docs/IotPlatform.png) 
![](https://raw.githubusercontent.com/kakake/IotPlatform/master/docs/demo.png) 

![](https://raw.githubusercontent.com/kakake/IotPlatform/master/docs/app2.png) 


功能列表：
--
* 1.Web界面来操控
* 2.APP手机来操控
* 3.raspberryPi服务端命令解析
* 4.屏幕显示
* 5.与arduino连接
* 6.操作摄像头
* 7.操作智能小车
* 8.各类感应器

命令列表：
--
* GPIO操作命令
```json
#获取所有GPIO状态
{"cmdname":"getgpios"}
#获取指定GPIO状态
{"cmdname":"getgpio","pins":[0,1,2,3,4,5,6,7,8,14,15]}
#应答
{"cmdname":"replygpio","setup":{"1":"out","4":"out"},"loop":[{"pinval":[1,0]},{"sleep":1},{"pinval":[1,1]}],"reply":[1,4]}
#设置GPIO，setup：in、out，loop：循环执行
{"cmdname":"setgpio","setup":{"4":"out","17":"out","22":"out"},"loop":[
{"pinval":[4,0]},{"pinval":[17,0]},{"pinval":[22,0]},
{"sleep":1},
{"pinval":[4,1]},
{"sleep":1},
{"pinval":[17,1]},
{"sleep":1},
{"pinval":[22,1]}
]}

```
* LCD屏幕输出文字命令
```json
#输出hello
{"cmdname":"charlcd","displaytext":"hello"}

```
