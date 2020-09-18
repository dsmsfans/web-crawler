import requests
from bs4 import BeautifulSoup
import json
import os
import time


# Create file
now = time.strftime("%Y-%m-%d", time.localtime())
if not os.path.exists(f"{now}_output"):
    os.makedirs(f"{now}_output")


def catch_url(board):
    p = requests.Session()
    url = requests.get(f"https://www.dcard.tw/f/{board}")
    soup = BeautifulSoup(url.text, "html.parser")
    sel = soup.select("article")
    a = []
    title = []
    for s in sel:
        a.append(s.find('a').get('href'))
    url = "https://www.dcard.tw/f/" + a[0]

    for k in range(0, 10):
        post_data = {
            "before": a[-1][6 + len(board):15 + len(board)],
            "limit": "30",
            "popular": "true"
        }
        r = p.get(f"https://www.dcard.tw/_api/forums/{board}/posts", params=post_data, headers={
            "Referer": "https://www.dcard.tw/", "User-Agent": "Mozilla/5.0"})
        data2 = json.loads(r.text)
        for u in range(len(data2)):
            Temporary_url = f"/f/{board}/p/" + \
                str(data2[u]["id"]) + "-" + \
                str(data2[u]["title"].replace(" ", "-"))
            a.append(Temporary_url)
    fetch_picture(a)


def fetch_picture(a):
    log = open(f"{now}_log.txt", "w", encoding='UTF-8')
    num = 0
    for url_index, i in enumerate(a):
        url = "https://www.dcard.tw"+i
        print(f"Page {url_index}'s URL: {url}")
        log.write(f"Page {url_index}'s URL: {url}\n")
        url = requests.get(url)
        soup = BeautifulSoup(url.text, "html.parser")
        soup.select('picture')
        sel_jpg = soup.find_all('img')

        for j in sel_jpg:
            if('https' in j['src'] and 'assets' not in j['src'] and 'scorecardresearch' not in j['src']):
                num += 1
                if(num > 15):
                    print(f"Picture {num - 15} :", j["src"])
                    log.write(f"Picture {num - 15} :" + j["src"] + "\n")
                    pic = j['src'].replace(".webp", "")
                    img = requests.get(pic).content
                    pic_out = open(f"{now}_output/"+str(num - 15)+".jpg", 'wb')
                    pic_out.write(img)
                    pic_out.close()
    log.close()
    print(f"Total {num - 15} pictures")
    print("Done")


if __name__ == "__main__":
    board = "sex"  # Select Section
    catch_url(board)
