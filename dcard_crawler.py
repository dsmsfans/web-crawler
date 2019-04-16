import requests
from bs4 import BeautifulSoup
import json

test = open("test.txt","w",encoding='UTF-8')

#版的url
board = "dressup"

p = requests.Session()
url=requests.get(f"https://www.dcard.tw/f/{board}")
soup = BeautifulSoup(url.text,"html.parser")
sel = soup.select("div.PostList_entry_1rq5Lf")
a=[]
for s in sel:
    a.append(s.find('a').get('href'))
url = "https://www.dcard.tw"+ a[2]

for k in range(0,10):
        post_data={
            "before":a[-1][6 + len(board):15 + len(board)],
            "limit":"30",
            "popular":"true"
        }
        r = p.get(f"https://www.dcard.tw/_api/forums/{board}/posts", params = post_data ,headers = { "Referer": "https://www.dcard.tw/", "User-Agent": "Mozilla/5.0" })
        data2 = json.loads(r.text)
        for u in range(len(data2)):
            Temporary_url = f"/f/{board}/p/"+ str(data2[u]["id"]) + "-" + str(data2[u]["title"].replace(" ","-"))
            a.append(Temporary_url)
j=0 #為了印頁數
q=0 #為了印張數
for i in a[2:]:
    url = "https://www.dcard.tw"+i
    j+=1
    print ("第",j,"頁的URL為:"+url)
    #file.write("temperature is {} wet is {}%\n".format(temperature, humidity))
    test.write("第 {} 頁的URL為: {} \n".format(j,url))
    url=requests.get(url)
    soup = BeautifulSoup(url.text,"html.parser")
    sel_jpg = soup.select("div.Post_content_NKEl9d div div div img")
    for c in sel_jpg:
        q+=1
        print("第",q,"張:",c["src"])
        test.write("%\n""第 {} 張: {} \n".format(q,c["src"])) 
        pic=requests.get(c["src"])
        img2 = pic.content
        pic_out = open("output/"+str(q)+".jpg",'wb')
        pic_out.write(img2)
        pic_out.close()

test.close()
print("爬蟲結束")

