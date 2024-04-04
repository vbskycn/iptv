

<h1 align="center"> ✯ 这是一个国内可直连的直播源分享项目 ✯ </h1>

<h3 align="center">🔕 永久免费 直连访问 完整开源 不含广告 完善的台标 直播源支持IPv4/IPv6双栈访问 🔕</h3>

<p align="center">
<img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/vbskycn/iptv">
<img alt="GitHub forks" src="https://img.shields.io/github/forks/vbskycn/iptv">
<img alt="GitHub issues" src="https://img.shields.io/github/issues/vbskycn/iptv">
<img alt="GitHub watchers" src="https://img.shields.io/github/watchers/vbskycn/iptv">
<img alt="GitHub contributors" src="https://img.shields.io/github/contributors/vbskycn/iptv">
<img alt="GitHub" src="https://img.shields.io/github/license/vbskycn/iptv">
</p>



---

## 🤹‍♂️直播源:

<table>
  <thead>
    <tr>
      <th>名称</th>
      <th>直播源地址</th>
      <th>完善源</th>
      <th>频道数</th>
      <th>更新时间</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>📺IPTV(江西电信测试)</td>
      <td><a href="https://live.proton218.top/dsyy/hd.txt">https://live.proton218.top/dsyy/hd.txt</a></td>
      <td><a href="https://github.com/vbskycn/iptv/edit/master/dsyy/hd.txt">编辑该源</a></td>
      <td>约120个</td>
      <td>每天6:00自动更新</td>
    </tr>
    <tr>
      <td>📺IPTV(IPV6专用)</td>
      <td><a href="https://live.fanmingming.com/tv/m3u/ipv6.m3u">https://live.fanmingming.com/tv/m3u/ipv6.m3u</a></td>
      <td><a href="https://github.com/fanmingming/live/edit/main/tv/m3u/ipv6.m3u">编辑该源</a></td>
      <td>120个</td>
      <td>2024.3.31</td>
    </tr>
    <tr>
      <td>📻Radio直播源</td>
      <td><a href="https://live.fanmingming.com/radio/m3u/index.m3u">https://live.fanmingming.com/radio/m3u/index.m3u</a></td>
      <td><a href="https://github.com/fanmingming/live/edit/main/radio/m3u/index.m3u">编辑该源</a></td>
      <td>317个</td>
      <td>2023.5.3</td>
    </tr>
  </tbody>
</table>



## 新增酒店直播源：

只保留1080的，速度排序是以江西电信的网络测试为准，每天早上6点左右自动测试更新。

使用cdn调用：

```
https://live.proton218.top/jdtv/itvlist.txt

https://live.proton218.top/jdtv/itvlist.m3u

```



### 新增网络自动扫描更新源：

部署在github上面的程序自动化扫描而来，每12小时更新一次。

```
https://live.proton218.top/dsyy/mylist.txt

https://live.proton218.top/dsyy/mylist.m3u
```





### 电视/广播图标库：

| 📺电视台图标库   | [https://live.proton218.top/taibiao/{频道名称}.png](https://github.com/vbskycn/iptv/tree/master/taibiao) | 958个 | 2023.11.25 |
| --------------- | ------------------------------------------------------------ | ----- | ---------- |
| 📻广播电台图标库 | [https://live.proton218.top/taibiao/radio/{频道名称}.png](https://github.com/vbskycn/iptv/tree/master/taibiao/radio) | 465个 | 2023.8.27  |




## 🛠️工具
- 🆕EPG接口地址：
  -  [http://epg.51zmt.top:8000/](http://epg.51zmt.top:8000/)
- 📄M3U To TXT：
  - Demo🔗 [https://zhuan.dnwx.vip/z.php?url=https://live.proton218.top/dsyy/hd.m3u](https://zhuan.dnwx.vip/z.php?url=https://live.proton218.top/dsyy/hd.m3u)
- 📄TXT To M3U：

  - Demo🔗 [https://zhuan.dnwx.vip/z.php?url=https://live.proton218.top/dsyy/hd.txt](https://zhuan.dnwx.vip/z.php?url=https://live.proton218.top/dsyy/hd.txt)
- 🌐直播源转换工具
  
  - [https://zhuan.dnwx.vip](https://zhuan.dnwx.vip/)

##    

##  如果你不愿意折腾，这里有折腾好的直播点播软件

- [https://zbds.lanzoui.com/b0b36hyqd](https://zbds.lanzoui.com/b0b36hyqd)



## 📖说明

- 本项目业源于大佬 https://github.com/fanmingming/live
- 所有播放源均收集于互联网，仅供测试研究使用，不得商用。
- 通过M3U8 Web Player测试直播源需使用https协议的直播源链接。
- 部分广播电台节目播出具有一定的时效性，需要在指定时段进行收听。
- 本项目不存储任何的流媒体内容，所有的法律责任与后果应由使用者自行承担。
- 您可以Fork本项目，但引用本项目内容到其他仓库的情况，务必要遵守开源协议。
- 本项目不保证直播频道的有效性，直播内容可能受直播服务提供商因素影响而失效。
- 所有文件均托管在[GitHub](https://github.com/vbskycn/iptv)且自动构建，由项目发起人公益维护，欢迎Star本项目或点击[Issues](https://github.com/vbskycn/iptv/issues/new/choose)反馈您的问题。
- 您可以编辑本项目的m3u文件或上传缺失的频道Logo到`tv`或`radio`目录下并发起拉取请求，收到请求后我们会对您提交的内容进行验证，审核通过后会自动发布。



## 📔更新

- 2023.8.23
  
  - 增加了txt to m3u 在线工具
  
  - 修复现有一些的问题
  
    

### 欢迎请我喝杯饮料

![](https://cdn.jsdelivr.net/gh/vbskycn/tu@main/img/ds.jpg)
