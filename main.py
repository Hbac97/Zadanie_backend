from bs4 import BeautifulSoup as bs
import requests 
import psycopg2

def scraper():
    site = requests.get("https://teonite.com/blog/")
    src = site.content
    content = bs(src,'lxml')

    list_links=[]
    list_authors=[]
    list_content=[]
    list_posts=[]
    for articles in content.find_all(class_="post-card"):
        a = articles.find('a')
        author = articles.find(class_="author")
        link = a.attrs['href']
        list_authors.append(author.text)
        list_links.append(link)

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
    

    print(list_authors)
    print(*list_posts, sep='\n',end='\n')
    print(len(list_authors))
    print(len(list_posts))
    list_combined = list(zip(list_authors,list_posts))
    sql(list_combined)

def sql(list_combined):
    try: 
        conn= psycopg2.connect(
            user="postgres",
            password="test123",
            host="localhost",
            port="5432",
            database="database")
        curs=conn.cursor()

        postgres_insert= """INSERT INTO posts (AUTHORS,CONTENT) VALUES (%s,%s);"""
        record_to_insert = (list_combined)
        curs.executemany(postgres_insert,record_to_insert)

        conn.commit()
        count = curs.rowcount
        print(count, "Authors Inserted successfully")

    except(Exception, psycopg2.Error) as err:
        print("Failed to insert",err)

    finally:
        if conn:
            curs.close()
            conn.close()
            print("connection closed")

scraper()
