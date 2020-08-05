#-*-coding:utf-8 -*-

#############################################
#              將所需函式庫加入             #
#############################################
import requests
from bs4 import BeautifulSoup
import os
import time
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib import cm
import numpy as np

#############################################
#                讀取PTT網頁                 #
#############################################
def get_web_page(url):
    time.sleep(0.1)  
    resp = requests.get(
        url=url,
        cookies={'over18': '1'}
    )
    if resp.status_code != 200:
        print('Invalid url:', resp.url)
        return None
    else:
        return resp.text

#############################################
#          對PTT網頁進行資料擷取              #
#############################################
def get_data(dom):
    soup = BeautifulSoup(dom , 'html.parser')
    article = soup.find(id='main-content')
    push_tag = soup.find_all('span', 'push-tag')
    return article, push_tag

#############################################
#         		計算推噓文數量               #
#############################################
def count_pnb(push_list):
    p, b, n = 0, 0, 0
    for index in push_list:
        if(index.getText()) == '推 ':
            p += 1
        elif(index.getText()) == '→ ':
            n += 1
        elif(index.getText()) == '噓 ':
            b += 1
    return(p, n, b)

#############################################
#          		讀取文章網址            	 #
##################a##########################
def get_article_url(text):
    url = []
    soup = BeautifulSoup(text, 'html.parser')
    divs = soup.find_all("div", "r-ent")
    for div in divs:
        try:
            href = div.find('a')['href']
            url.append('https://www.ptt.cc' + href)
        except:
            pass
    return url

#############################################
#    	讀取看板頁面(沒有加搜尋字眼時使用)     #
##################a##########################
def getNext(url):
    urls = get_web_page(url)
    soup = BeautifulSoup(urls, 'html.parser')
    div = soup.find_all('a','btn wide')
    for i in div:
        if i.getText() == '‹ 上頁':
            nextPage = 'https://www.ptt.cc' + i.get('href')
    return nextPage
    
#############################################
#          			畫圖				     #
##################a##########################
##################圓餅圖######################
def DrawPie(font, labels_list, percent_list, title):				#labels_list: 圓餅圖的字    #percent_list: 圓餅圖各項的比例
	labels, sizes = [], []											
	plt.title(title, fontproperties = font)
	for i in range(datazise):
		labels.append(str(labels_list[i]))
		sizes.append(str(percent_list[i]))
	colors = cm.rainbow(np.arange(len(sizes))/len(sizes))
	pictures,category_text,percent_text = plt.pie(sizes, labels=labels, colors=colors, autopct='%1.2f%%', shadow=True, startangle=140)
	for i in category_text:
		i.set_fontproperties(font)
	#plt.legend(loc = "upper right", prop = font)
	plt.axis('equal')

##################直方圖######################	
def DrawBar(font, sem_list, bar_list, title):						#sem_list: 直方圖的每條上的字   #bar_list: 直方圖的長度
	plt.title(title, fontproperties = font)
	y_pos = np.arange(4)
	plt.xticks(y_pos + .3/2, ('出現次數','推','箭頭','噓'), fontproperties = font)
	for i in range(len(sem_list)):
		plt.bar(y_pos + 0.25*i , bar_list[i], 0.2, alpha=.5, label = sem_list[i])
	plt.legend(loc = "upper right", prop = font)
	
#############################################
#           主程式:進行資料分析              #
#############################################
if __name__ == '__main__':
	KEY = 1																#有沒有加入搜尋字眼 1:有 0:沒有
	Board = 'dog'														#選取PTT看板	!!!!!!(凡是設有內容分級規定處理，即不能直接進入看板者，EX.八卦版...等會沒辦法爬)!!!!!
	Search = '['														#加入搜尋特定字眼的文章 EX.在Food版找尋標題有含'台南'的文章
	PTT_URL = 'https://www.ptt.cc/bbs/' if KEY == 1 else 'https://www.ptt.cc/bbs/' + Board + '/index.html'
	page_num = 5														#爬文的頁數，從最新頁數開始爬
	p_weight, n_weight, b_weight = 1, 0.5, -1 							#推、箭頭、噓文加權的比重

	############################################################
	datazise = eval(input("請輸入欲分析的詞彙個數  :  ")) 				
	############################################################
	#輸入關鍵字的喜好程度，代表最後加權的比重
	urls = []
	semantic_list = []			#存放輸入的關鍵字
	#weight_list = []			#存每項關鍵字的權重
	for i in range(datazise):											
		semantic_in = input("請輸入第"+str(i+1)+"個關鍵字  :  ")			#改變你想要找的關鍵字
		semantic_list.append(semantic_in)
		#weight_in = eval(input("喜好程度為  :  "))				#改變你想要找的關鍵字
		#weight_list.append(weight_in)
		
	############################################################
	articles, push_tags = [], []		#articles: ptt文章所有內容   #push_tags: 推噓文資訊
	for page in range(page_num):														#取得PTT頁面資訊
		url_key = PTT_URL + Board + '/search?page=' + str(page+1) + '&q=' + Search		
		url = url_key if KEY == 1 else PTT_URL if page == 0 else getNext(PTT_URL)
		response = requests.get(url)
		urls = get_article_url(response.text)
	############################################################
		for url in urls:
			print(url)
			text = get_web_page(url)
			if text is None:
				continue
			article, push_tag = get_data(text)
			articles.append(article)
			push_tags.append(push_tag)
	############################################################
	#計算關鍵字出現次數，以及關鍵字出現的文章其推噓文數量
	sum_sem_list = []			#該關鍵字出現總數
	sem_p, sem_n, sem_b = [], [], []	#關鍵字出現之文章其推噓文總數 p:推 n:箭頭 b:噓
	p, n, b = 0, 0, 0
	p_sum, n_sum, b_sum = 0, 0, 0
	for i in range(datazise):														
		sem_count = 0
		count = 0
		for index in articles:
			sem_count += str(index).count(semantic_list[i])
			if str(index).count(semantic_list[i]) !=0:
				p, n, b = count_pnb(push_tags[count])
				p_sum += p
				n_sum += n
				b_sum += b
			count += 1
		sem_p.append(p_sum)
		sem_n.append(n_sum)
		sem_b.append(b_sum)
		sum_sem_list.append(sem_count)
					
	############################################################
	#將所有找尋到的字彙個數相加，計算總合
	sum_all = sum(sum_sem_list)
	percent_list = []						#關鍵字佔比

	#sum_weight_list = []					#加權後的各關鍵字分數
	#計算單一詞彙佔全部字彙的百分比
	for i in range(datazise):
		if sum_all != 0:
			percent_list.append(round((sum_sem_list[i]*100)/sum_all,2))
		else:
			percent_list.append(0)
		
		#sum_weight_list.append(sum_sem_list[i]*weight_list[i])

'''	############################################################
	#計算加權權重後總和
	grade = sum(sum_weight_list)															#我的分數，以輸入權重為計算依據
	general_grade = sum(sem_p)*p_weight + sum(sem_n)*n_weight - sum(sem_b)*b_weight			#客觀的分數，以推噓文的數量計算
'''

	############################################################
	#把正向詞彙以及負向詞彙進行分類準備繪圖
pnb_list = []
for i in range(datazise):
    bar_pnb = (sum_sem_list[i], sem_p[i], sem_n[i], sem_b[i])
    pnb_list.append(bar_pnb)

print('\r\r')
	############################################################
print("總搜尋字彙出現個數為 : ", sum_all)
for i in range(datazise):
    print(semantic_list[i],"出現個數為:",sum_sem_list[i],"百分比為",percent_list[i],"%")
	############################################################
'''
	print('我的評分為:', grade, '大家的評分為:', general_grade)
	if (general_grade >= 0 and grade >= 0) or (general_grade < 0 and grade < 0):
		print("我的喜好和大家一樣")
	else:
		print("我的喜好和大家不同")
'''
	#######################################
	#				將結果繪圖			  #
	#######################################
myfont = FontProperties(fname=r'./GenYoGothicTW-Regular.ttf')							#字型檔，r'裡面放你的字型檔案路徑'
#圓餅圖	
title1 = '關鍵字出現比例'
plt.subplot(1,2,1)											#將圖表分割為2行2列，目前繪製的是第一格
DrawPie(myfont, semantic_list, percent_list, title1)
#長條圖
title2 = '關鍵字推文總數'
plt.subplot(1,2,2)											#將圖表分割為2行2列，目前繪製的是第二格
DrawBar(myfont, semantic_list, pnb_list, title2)
plt.show()
	#######################################
