import requests
import parsel
import re
import os
import subprocess
import ftp

# 链接
# a = input("请输入链接：")
url = requests.get('https://madou.club/hongkongdoll-%e6%a3%ae%e6%9e%97-%e7%ac%ac%e9%9b%b6%e9%9b%86-%e5%89%8d%e5%a5%8f%e5%92%8c%e5%89%8d%e6%88%8f.html').text
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

aaa = video_url.replace('https://dash.madou.club/share/', '')
print(aaa)

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

os.mkdir(aaa)

# 保存key
key2 = requests.get(key + '/ts.key').text
fd = open(aaa + '/' + 'ts.key', "w", encoding='utf-8')
fd.write(key2)

# 保存m3u8文件
fd = open(aaa+ "/" + title + '.m3u8', "w", encoding='utf-8') # 文件创建111文件
fd = open(aaa + '/' + 'index.m3u8', "w", encoding='utf-8') # 文件创建111文件
key11 = video_url.replace('share', 'videos').replace('dash.madou.club', 'dash.madou.club/')
fd.write(m3u8_url.replace(key11, '').replace('/ts.key', 'ts.key'))

# 下载ts
fd = open('down.sh', "w", encoding='utf-8')
fd.write(m3u8_url.replace('index','wget -P ./'+ aaa + ' ' + key + '/index'))
fd.close()

print("-------------")
# print(os.system("chmod 777 down.sh"))
# print(os.system("./down.sh"))
print(subprocess.getoutput('chmod 777 down.sh'))
print(subprocess.getoutput('./down.sh'))
jpg = str(re.findall(u"shareimage      (.+?)',".encode('utf8'),url.encode('utf8'))).replace('[b": ', '').replace('"]', '').replace("'", '')
print(subprocess.getoutput('wget -P '+ aaa + ' ' + jpg))
print("-------------")

print(ftp.ftp(aaa))
