import requests
#延遲套件
import time
import random
import csv
from bs4 import BeautifulSoup

URL = "https://www.majortests.com/word-lists/word-list-0{0}.html"

def generate_urls(url, start_page, end_page):
    urls = []

    for page in range(start_page, end_page):
        # 用format將URL的{}去替換成page索引值 URL的{}中請先放入起始頁索引值
        urls.append(url.format(page))

    return urls


# 置入假來源+爬蟲
def get_resource(url):
    #假來源
    headers = {
        "user-agent" : "Mozilla/5.0 (Windoes NT 10.0; Win64; x64) AppWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
        }
    #用requests.get函式爬蟲並回傳 更改headers參數給個假來源以在請求登入網站時假裝真人登入該網站
    return requests.get(url, headers = headers)

# 解析
def parse_html(html_str):
    return BeautifulSoup(html_str, "lxml")

# 開始爬蟲抓資料
def get_word(soup, file):
    words = []
    count = 0 

    # 抓soup物件中(class_ = "wordlist")底下的所有資料
    for wordlist_table in soup.find_all(class_ = "wordlist"):
        count += 1

        # [w]:entry事件
        # 抓每個wordlist_table物件中 底下的所有tr資料
        for word_entry in wordlist_table.find_all("tr"):
            new_word = []
            # 加入標示頁面位址
            new_word.append(file)
            # 加入標示第n個table的索引值
            new_word.append(str(count))
            # 加入th(單字)
            new_word.append(word_entry.th.text)
            # 加入td(解釋)
            new_word.append(word_entry.td.text)
            # 將上述陣列加入至words陣列
            words.append(new_word)            

    return words

# 仿真人以避免爬蟲被擋
def web_scraping_bot(urls):
    eng_words = []

    for url in urls:
        # [n]取該矩陣的第n個元素 [-1]為抓整串的最後一個
        file = url.split('/')[-1]
        print("catching: ", file, " web data...")

        # 仿真人登入網站 參數為替換為索引值之網頁
        r = get_resource(url)

        if r.status_code == requests.codes.ok:
            # BeautifulSoup解析資料 用.text函式將資料轉成字串
            soup = parse_html(r.text)
            words = get_word(soup, file)
            eng_words = eng_words + words

            # random.uniform(start, end)隨機浮點數
            ran = random.uniform(5, 8)
            print("Sleep {:.2f} second!!".format(ran))
            #()延遲秒數
            time.sleep(ran)
                    
        else:
            eng_words = "HTTP request error!!"

    return eng_words

# 開csv檔(excel)寫入
def save_to_csv(words, file):
    # w+ 為用append的方式寫入 否則直接覆蓋寫入
    # with as運行完會自動關閉
    with open(file, "w+", newline = "", encoding = "utf-8") as fp:
        writer = csv.writer(fp)

        for word in words:
            writer.writerow(word)


# __main__爬原始碼    
if __name__ == "__main__":
    urlx = generate_urls(URL, 1, 10)
    eng_words = web_scraping_bot(urlx)

    for item in eng_words:
        print(item)

    save_to_csv(eng_words, "WordListDemo.csv")





'''
# 僅印爬下來的網址
print(urlx)

# [or]:
print(*generate_urls(URL, 1, 10), step = "\n")
'''