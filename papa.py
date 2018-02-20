# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import os
import time
web_add="http://www.4*k.com"
headers1 = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
           'refer': 'http://www.dengnihuilai.com/'}
r_o=requests.get(web_add+"/html/part/28.html",headers=headers1).content.decode("gbk",'ignore')
soup_o=BeautifulSoup(r_o,"html.parser")
a_sum_str=soup_o.body.find("a",text="尾页").get('href')
page_sum=int(re.compile(r"\d{3,}").findall(a_sum_str)[0])
update_count=0
update_list=[]
for i in range(1,page_sum+1):
    if i==1:
        page_add_part="/html/part/28.html"
    else:
        page_add_part="/html/part/28_"+str(i)+".html"
    r_l=requests.get(web_add+page_add_part,headers=headers1).content.decode("gbk",'ignore').encode('utf-8','ignore')
    soup_l=BeautifulSoup(r_l,"html.parser")
    for one_art in soup_l.body.find_all("a",href=re.compile(r"^/html/article/")):
        a_link=web_add+one_art.get('href')#某篇小说的地址
        r_a=requests.get(a_link,headers=headers1)
        if r_a.status_code>=400:
            print("连接失败---"+a_link+"--"+one_art.get_text())
            continue
        r_a=(r_a.content).decode("gbk",'ignore').encode('utf-8','ignore')
        soup_a=BeautifulSoup(r_a,"html.parser")
        a_content=soup_a.body.find("div",class_="n_bd").get_text()
        if os.path.isfile(one_art.get_text()+".txt"):
            print(one_art.get_text()+"----已存在")
            time.sleep(1)
        else:
            with open(one_art.get_text()+'.txt','a',encoding='utf-8') as f:
                # a_content=a_content.replace('\xa0', ' ')
                # a_content=a_content.replace('\u22ef', ' ')
                # a_content=a_content.replace('\n', '\r\n')
                f.write(a_content)
                update_count+=1
                update_list.append(one_art.get_text())
                print("下载："+str(update_count)+"."+one_art.get_text())
print("跟新完毕！本次更新数目："+update_count+"\n----------")
print("清单："+update_list)
input()