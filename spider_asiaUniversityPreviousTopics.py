import WordListDemo
import requests
import csv
import time
from requests import urllib3

# 取網址list
def generate_urls(start_page, end_page):
    urls = []
    domain = "https://csie.asia.edu.tw{0}"
    urllib3.disable_warnings()
    # 取得該網址回應參數
    r = requests.get(domain.format("/project"), verify = False)

    if r.status_code == requests.codes.ok:
        # 解析資料
        soup = WordListDemo.parse_html(r.text)

        # 要爬蟲的頁面數
        for year in range(start_page, end_page + 1):
            
            # 從soup(已解析資料)中找到每個class_為"nav-pills"數據下所有的"li"標籤內容 存入item
            for item in soup.find(class_ = "nav-pills").find_all("li"):
                # 從item中超連結函式(.a)下的.get函式取得其參數下內容 並儲存為urlf變數
                # PS.從原始碼中可以得知 我們要的網址內容存在a下的href中
                url = item.a.get("href")

                if url.find(str(year)) > -1:
                    urls.append(domain.format(url))
                    break

    else:
        print("Error!!")

    return urls

def get_projects(soup, count):
    projects = []

    for div in soup.find_all("div", class_ = "table-responsive"):

        for tr in div.table.find_all("tr"):
            rowData = []

            if count > 1:

                # .isnumeric用來判斷運算結果是否為數字並回傳 Boolean 值。在此用replace整理數據後用來判斷是否為數字『編號』
                if tr.td != None and tr.td.text.replace('\t', '').replace('\n', '').isnumeric():
                    
                    # 依上述判斷如為儲存編號之td則存入rowData中
                    for cell in tr.find_all('td'):
                        rowData.append(cell.text.replace('\t', '').replace('\n', ''))

                # 同上 th版        
                elif tr.th != None and tr.th.text.replace('\t', '').replace('\n', '').isnumeric():
                    
                    for cell in tr.find_all('th'):
                        rowData.append(cell.text.replace('\t', '').replace('\n', ''))
            
            else:
                # 以下為非編號（數字）所做的處理 同上整理後加入rowData
                if tr.td != None:

                    for cell in tr.find_all('td'):
                        rowData.append(cell.text.replace('\t', '').replace('\n', ''))

                elif tr.th != None:

                    for cell in tr.find_all('th'):
                        rowData.append(cell.text.replace('\t', '').replace('\n', ''))
                
                count += 1

            projects.append(rowData)
            
    return projects

def web_scraping_bot(urls):
    projects_list = []
    count = 1
    for url in urls:
        file = url.split('/')[-1]
        print('catching ', file, ' web data...')
        r = WordListDemo.get_resource(url)
        if r.status_code == requests.codes.ok:
            soup = WordListDemo.parse_html(r.text)
            projects = get_projects(soup, count)
            projects_list = projects_list + projects
            print('waiting 5 seconds...')
            time.sleep(1)
        else:
            print('HTTP requests error!!')
        count += 1
    return projects_list

def save_to_csv(projects, file):
    # csv檔在mac可讀編碼為utf16
    with open(file, 'w+', newline='', encoding='utf-8') as fp:
        writer = csv.writer(fp)
        for project in projects:
            writer.writerow(project)
        

if __name__ == '__main__':
    print(generate_urls(100, 108))
    urlx = generate_urls(100, 108)
    projects_list = web_scraping_bot(urlx)
    save_to_csv(projects_list, "spider_asiaUniversityPreviousTopics16.csv")