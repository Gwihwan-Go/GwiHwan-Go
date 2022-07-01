## This code is made for github actions
## It is responsible for parsing blog's latest posts and writing in README.md file.

import feedparser

MAX_POST_NUM=5
blog_rss = "https://rss.blog.naver.com/ie1914" ##rss adress of blog
rss_feed = feedparser.parse(blog_rss)

post_list = ""

for idx, feed in enumerate(rss_feed['entries']) :
    if idx > MAX_POST_NUM :
        break
    feed_date = feed['published_parsed']
    post_list += f"- [{feed_date.tm_year}/{feed_date.tm_mon}/{feed_date.tm_mday} - {feed['title']}]({feed['link']}) <br>\n"


readme_text = ""
with open("README.md", 'r', encoding='utf-8') as f:
    readme_list = f.readlines()
f.close()
upper_bound = readme_list.index('Section 4\n') ##upper bound before Section4
down_bound = len(readme_list) - readme_list[::-1].index('Section 4\n')-1 ##down bound before Section4

upper_text = ''.join(readme_list[:upper_bound+2])
down_text = ''.join(readme_list[down_bound-1:])

readme_text = f"{upper_text}{post_list}{down_text}"
with open("README.md", 'w', encoding='utf-8') as f:
    f.write(readme_text)
f.close()
