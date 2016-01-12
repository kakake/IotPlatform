# IotPlatform
物联网平台，通过访问www.efwplus.cn网站来控制raspberryPI主机，操作相关设备，如：遥控器、温度湿度传感器、摄像头等


![](https://raw.githubusercontent.com/kakake/IotPlatform/master/docs/demo.png) 


功能列表：
--
* 1.控制GPIO服务端
* 2.Web控制
* 3.App控制
* 4.tft彩屏显示
* 5.串口通信
* 6.红外接收发送
* 7.人体红外感应
* 8.各类感应器

命令列表：
--
* GPIO操作命令
<br/>
{"cmdname":"getgpios"}
<br/>
{"cmdname":"getgpio","pins":[0,1,2,3,4,5,6,7,8,14,15]}
<br/>
{"cmdname":"replygpio","setup":{"1":"out","4":"out"},"loop":[{"pinval":[1,0]},{"sleep":1},{"pinval":[1,1]}],"reply":[1,4]}
<br/>
{"cmdname":"setgpio","setup":{"4":"out","17":"out","22":"out"},"loop":[
{"pinval":[4,0]},{"pinval":[17,0]},{"pinval":[22,0]},
{"sleep":1},
{"pinval":[4,1]},
{"sleep":1},
{"pinval":[17,1]},
{"sleep":1},
{"pinval":[22,1]}
]}
<br/>
* LCD屏幕输出文字命令
<br/>
{"cmdname":"charlcd","displaytext":"hello"}

