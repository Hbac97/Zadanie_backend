from bs4 import BeautifulSoup as bs
import requests 
import psycopg2
import time

def scraper():
    site = requests.get("https://teonite.com/blog/")
    src = site.content
    content = bs(src,'lxml')

    list_titles=[]
    list_authors=[]
    list_content=[]
    list_posts=[]

    content_posts = content.find(class_="post-cards")

    for articles in content_posts.find_all(class_="post-card"):
        a = articles.find('a')
        author = articles.find(class_="author")
        link = a.attrs['href']
        title = articles.find(class_="title")
        list_authors.append(author.text)
        list_titles.append(title.text)

        site2 = requests.get(f"https://teonite.com/{link}")
        src2 = site2.content
        content2 = bs(src2,'lxml')

        for post in content2.find_all("article"):
            p0 = post.find('h3')
            p1 = post.find_all('p')
            for p in p0:
                list_content.append(p.text)
            for p in p1:
                list_content.append(p.text)
            list_posts[len(list_posts):] = [''.join(list_content[:])]
            list_content=[]

    list_combined = list(zip(list_authors,list_titles,list_posts))
    sql(list_combined)

def sql(list_combined):
    try: 
        conn= psycopg2.connect(
            user="postgres",
            password="test123",
            host="db",
            port="5432",
            database="database")

        curs=conn.cursor()

        curs.execute("""SELECT EXISTS(SELECT * FROM posts WHERE authors LIKE '%Gryczka%' LIMIT 1);""")
        if not curs.fetchone()[0]:

            postgres_insert= """INSERT INTO posts (AUTHORS,TITLES,CONTENT) VALUES (%s,%s,%s);"""
            record_to_insert = (list_combined)
            curs.executemany(postgres_insert,record_to_insert)

            conn.commit()
            count = curs.rowcount
            print(count, "Authors, Titles and Content inserted successfully")
        else:
            print ("Rows already exist")

    except(Exception, psycopg2.Error) as err:
        print("Failed to insert",err)
        print("Trying again in 5 seconds...")
        time.sleep(5)
        scraper()

    finally:
        if conn:
            curs.close()
            conn.close()
            print("connection closed")

scraper()
