from bs4 import BeautifulSoup as bs
import requests 

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