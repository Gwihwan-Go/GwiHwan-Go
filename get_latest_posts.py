# This code is made for github actions
# It is responsible for parsing blog's latest posts and writing in README.md file.
import argparse
import feedparser

###########################Argspace ZONE######################################

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--where', type=str, default="velog",
                    help='which blog site that we will parse from')
parser.add_argument('--max', type=int, default=3,
                    help='The max number of parsing posts')

args = parser.parse_args()

MAX_POST_NUM=args.max
if args.where == "naver" :
    index_pars = 'Section 4\n' #Decide where to put -> in thiscase put in section 4
    blog_rss = "https://rss.blog.naver.com/ie1914" ##rss adress of blog
if args.where == "velog" :
    index_pars = 'Section 3\n' #Decide where to put -> in thiscase put in section 3
    blog_rss = "https://v2.velog.io/rss/return_go"

###########################Argspace ZONE######################################
rss_feed = feedparser.parse(blog_rss)
post_list = ""

for idx, feed in enumerate(rss_feed['entries']) :
    if idx > MAX_POST_NUM-1 :
        break
    feed_date = feed['published_parsed']
    post_list += f"- [{feed_date.tm_year}/{feed_date.tm_mon}/{feed_date.tm_mday} - {feed['title']}]({feed['link']}) <br>\n"

print(post_list)
readme_text = ""
with open("README.md", 'r', encoding='utf-8') as f:
    readme_list = f.readlines()
f.close()
upper_bound = readme_list.index(index_pars) ##upper bound before Section4
down_bound = len(readme_list) - readme_list[::-1].index(index_pars)-1 ##down bound before Section4

upper_text = ''.join(readme_list[:upper_bound+2])
down_text = ''.join(readme_list[down_bound-1:])

readme_text = f"{upper_text}{post_list}{down_text}"

with open("README.md", 'w', encoding='utf-8') as f:
    f.write(readme_text)
f.close()
