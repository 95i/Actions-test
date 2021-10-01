import requests
import parsel
import re

# 链接
# a = input("请输入链接：")
url = requests.get('https://madou.club/msd021-%e7%bb%9d%e6%9c%9b%e7%9a%84%e8%82%89%e5%81%bf%e5%80%ba%e6%ac%be-%e5%bc%ba%e8%a1%8c%e6%8a%bd%e6%8f%92%e9%ab%98%e6%bd%ae%e9%a2%a4%e6%8a%96.html').text
# url = requests.get(a).text
# print(url)


# xpath提取视频title
paers = parsel.Selector(url)
title = str(paers.xpath('//title/text()')).replace("[<Selector xpath='//title/text()' data='", '').replace("'>]", '').replace('/', '') # xpath选择
print(title)


# xpath提取视频url
paers = parsel.Selector(url)
video_url = str(paers.xpath('.//article[@class="article-content"]//p/iframe/@src').extract()).replace("['", "").replace("']", "") # xpath选择
print(video_url)

# 获取token
token = requests.get(video_url).text
# print(token)

# 提取token
token_01 = str(re.findall(u'token(.+?)";'.encode('utf8'),token.encode('utf8'))).replace("[b' = ", '').replace("']", '').replace('"', '')# 正则表达式获取关键字字段
# print(c)

# 访问m3u8文件
m3u8 = video_url.replace('share', 'videos') + '/index.m3u8?token=' + token_01
m3u8_url = requests.get(m3u8).text
# print(m3u8_url)

# 提取key
key = video_url.replace('share', 'videos')
print(key)

# 保存key
key2 = requests.get(key + '/ts.key').text
fd = open('ts.key', "w", encoding='utf-8')
fd.write(key2)

# 保存m3u8文件
fd = open('index.m3u8', "w", encoding='utf-8') # 文件创建111文件
key11 = video_url.replace('share', 'videos').replace('dash.madou.club', 'dash.madou.club/')
fd.write(m3u8_url.replace(key11, '').replace('/ts.key', 'ts.key'))

# 下载ts
fd = open('down.sh', "w", encoding='utf-8')
fd.write(m3u8_url.replace('index','wget ' + key + '/index'))



