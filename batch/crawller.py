import requests
import re
from bs4 import BeautifulSoup


res = requests.get("https://hanntaigo.main.jp/")
res.encoding = res.apparent_encoding
soup = BeautifulSoup(res.text, "html.parser")
print(res.text)

taigigofile = "./dataset/taigigo.csv"

total = 0
with open(taigigofile,mode="w") as f:
    f.write("org,rev\n")
    tables = soup.select("#content > table")
    for table in tables:
        tds = table.select("td")
        for td in tds:
            matches = re.findall(r'([^・]+⇔[^・]+)',td.get_text(strip=True))
            for target in matches:
                total+=1
                pare = target.split("⇔")
                f.write(pare[0]+","+pare[1]+"\n")

print("append " + str(total) + " sets")