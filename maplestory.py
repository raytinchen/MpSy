from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import subprocess

# 初始化一個 WebDriver
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=chrome_options)  # 或者使用其他的 WebDriver，比如 Firefox 或 Edge
driver.get("https://maplestory.beanfun.com/main")
#html = driver.page_source
soup = BeautifulSoup(driver.page_source, 'lxml')

domain="https://maplestory.beanfun.com/"

def ld():
    with open('/home/raytin/MpSy/MapleStory_new.json','r',encoding='utf-8') as f:
        dicts=json.load(f)
        return dicts


def ep(dicts):
    with open('/home/raytin/MpSy/MapleStory_new.json','w',encoding='utf-8') as f:
        json.dump(dicts,f)


def main():
    dicts=ld()
    for x in reversed(soup.findAll('a',{'class':'mBulletin-items-link'})):
        if x.get('bid') in list(dicts):
            pass
        else:
            dicts[x.get('bid')]={}
            if len(x.get('href'))<25:
                dicts[x.get('bid')]['url']=f"{domain}{x.get('href')}"
                try:
                    driver.get(dicts[x.get('bid')]['url'])
                    soup_Pagination = BeautifulSoup(driver.page_source, 'lxml')                   
                    dicts[x.get('bid')]['icon']=soup_Pagination.find('div',{'class':'mBulletin-content'}).p.img.get('src')
                except Exception as inner_exception:
                    pass
            else:
                dicts[x.get('bid')]['url']=x.get('href')
            dicts[x.get('bid')]['title']=x.find('div', class_='mBulletin-items-title').text.strip()
            dicts[x.get('bid')]['category'] =x.find('div', class_='mBulletin-items-cate').text.strip()
            dicts[x.get('bid')]['date']=x.find('div', class_='mBulletin-items-date').text.strip()
            print(f"{dicts[x.get('bid')]['date']} 【{dicts[x.get('bid')]['category']}】\n[{dicts[x.get('bid')]['title']}]({dicts[x.get('bid')]['url']})")
            try:
                print(f"{dicts[x.get('bid')]['icon']}")
            except Exception as inner_exception:
                driver.quit()
    driver.quit()
    ep(dicts)
    
def run_git_commands(directory, commit_message):
    try:
        # 執行 git add .
        subprocess.run(["git", "add", "."], cwd=directory, check=True)
        print("成功執行 git add .")

        # 執行 git commit
        subprocess.run(["git", "commit", "-m", commit_message], cwd=directory, check=True)
        print(f"成功執行 git commit: '{commit_message}'")

        # 執行 git push
        subprocess.run(["git", "push"], cwd=directory, check=True)
        print("成功執行 git push")
    
    except subprocess.CalledProcessError as e:
        print("執行 Git 命令時發生錯誤:", e)

directory = "/home/raytin/MpSy/"  # 替換為你的目錄路徑
commit_message = "update"  # 替換為你的提交訊息

main()
run_git_commands(directory, commit_message)







    
