import requests
from bs4 import BeautifulSoup
import json
import os

if not os.path.exists("output"):
    os.makedirs("output")

test = open("test.txt", "w", encoding='UTF-8')

# Select Section
board = "dressup"

p = requests.Session()
url = requests.get(f"https://www.dcard.tw/f/{board}")
soup = BeautifulSoup(url.text, "html.parser")
sel = soup.select("div.sc-1azsmde-0")
a = []
for s in sel:
    a.append(s.find('a').get('href'))
url = "https://www.dcard.tw" + a[0]

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

num = 0

for url_index, i in enumerate(a):
    url = "https://www.dcard.tw"+i
    print(f"Page {url_index}'s URL: {url}")
    test.write(f"Page {url_index}'s URL: {url}")
    url = requests.get(url)
    soup = BeautifulSoup(url.text, "html.parser")
    sel_jpg = soup.find_all('img')
    for j in sel_jpg:
        if('https' in j['src']):
            num += 1
            print(f"Picture {num} :", j["src"])
            test.write(f"Picture {num} :" + j["src"])
            pic = j['src'].replace(".webp","")
            img = requests.get(pic).content
            pic_out = open("output/"+str(num)+".jpg", 'wb')
            pic_out.write(img)
            pic_out.close()

test.close()
print(f"Total {num} pictures")
print("Done")
