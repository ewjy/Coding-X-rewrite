from bs4 import BeautifulSoup
import re
import requests
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties
url = "https://www.dcard.tw"
BOARD = 'pet'  #要爬的dcard板名稱
LATEST = False  #True 找最新的 ， False 就沒有找最新的
ARTICLE_NUM = 30 #搜尋文章的數量
COMMENT_NUM = 3  #留言的數量
key=''
def Search_Board(): #搜尋板內關鍵字的函式
    key = input('關鍵字')
    url_search = url + '/search?query=' + key + '&forum=' + BOARD
    print(url_search)
    res = requests.get(url_search)

    soup = BeautifulSoup(res.text, 'html.parser')
    title_list, href_list, like_list = [], [], []

    for entry in soup.select('article a'):
        title_list.append(entry.text)
        href_list.append(entry['href'])

    for entry in soup.select('article div'):
        if entry.has_attr('class'):
            item = re.search('sc-1kuvyve-3',entry['class'][0])
            if item is not None:
                like_list.append(int(entry.text))

    return title_list[0:ARTICLE_NUM], href_list[0:ARTICLE_NUM], like_list[0:ARTICLE_NUM]

def DrawBar(x_list, y_list, title, font):
    plt.title(title, fontproperties = font)
    plt.bar(x_list, y_list)
    plt.xticks(x_list,x_list)
    return


if __name__ == '__main__':

    sum_like = [0]*5
    # name = [0]*5
    name = ['cat','dog','mouse','bird']
    myfont = FontProperties(fname=r'C:\\python\\github\\Coding-X-rewrite\\GenYoGothicTW-Regular.ttf')

    


    for i in range(1,5):
        title_list, href_list, like_list = Search_Board() # Search the board and get article titles and likes number of each article
        sum_like[i] = sum(like_list)


    ##############################################################################################################
    # Plot the like number of each article as histogram
    ##############################################################################################################

        title = '每篇文章讚數'
        DrawBar(list(range(1,ARTICLE_NUM + 1)), like_list, title, myfont)


    ##############################################################################################################
    # Sort the articles according to likes number
    ##############################################################################################################
        for i in range(ARTICLE_NUM):
            for j in range(ARTICLE_NUM - i - 1):
                if like_list[j] < like_list[j + 1]:
                    title_list[j], title_list[j + 1] = title_list[j + 1], title_list[j]
                    href_list[j], href_list[j + 1] = href_list[j + 1], href_list[j]
                    like_list[j], like_list[j + 1] = like_list[j + 1], like_list[j]

        for i in range(ARTICLE_NUM):
            print('(' + str(like_list[i]) + ')', end = ' ')
            print(title_list[i], end = ' ')
            print('(' + href_list[i] + ')')

        plt.show() # Show the figure
    
    
    tmp_sum_like = []
    for i in range(0,4):
        tmp_sum_like.append(sum_like[i])

    # 直方圖
    xlabels = name[0:4]
    fig,ax = plt.subplots()
    plt.bar(list(range(0,4)),tmp_sum_like)
    plt.xticks(list(range(0,4)),xlabels)
    plt.show()

    # 圓餅圖
    vol = tmp_sum_like
    exp = [0, 0, 0, 0]
    plt.pie(x = vol,labels = xlabels,autopct = '%.2f%%',explode = exp)
    plt.show()

    
