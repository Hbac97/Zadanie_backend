from bs4 import BeautifulSoup as bs
import requests 

site = requests.get("https://teonite.com/blog/")
src = site.content
content = bs(src,'lxml')

list_links=[]
list_authors=[]
list_content=[]
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
        for text in post:
            list_content.append(post)
            

print(len(list_links))
print(len(list_authors))


