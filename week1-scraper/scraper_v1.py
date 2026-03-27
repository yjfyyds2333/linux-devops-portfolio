import requests
from bs4 import BeautifulSoup
import pymysql
import os 


def run():
    db = pymysql.connect(
        host=os.environ.get("DB_HOST","192.168.88.129"),
        user=os.environ.get("DB_USER","root"),
        password=os.environ.get("DB_PASSWORD","123456"),
        database=os.environ.get("DB_NAME","app_db"),
        port=3306,
        charset="utf8mb4"
    )
    cursor = db.cursor()

    sql = "CREATE TABLE IF NOT EXISTS books ( \
        id INT AUTO_INCREMENT PRIMARY KEY, \
        title VARCHAR(200) NOT NULL, \
        price VARCHAR(20), \
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, \
        UNIQUE KEY unique_title (title) \
    );"

    cursor.execute(sql)

    url = "https://books.toscrape.com"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    books = soup.find_all("article",class_="product_pod")

    for book in books[:10]:
        title = book.find("h3").find("a")["title"]
        price = book.find("p",class_="price_color").text
        cursor.execute(
            "INSERT IGNORE INTO books(title,price) VALUES (%s,%s);",(title,price)
	    )     

    db.commit()
    cursor.close()

