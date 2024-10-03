import requests
from json import loads
from urllib import request
gist_id = "eb5d0abf02532775199f267397dc1b3d"
EMPTY_LINE = '\n'
GITHUBIO_RAW_URL = "https://raw.githubusercontent.com/GwiHwan-Go/GwiHwan-Go.github.io/main/index.md"
GIT_URL = "https://gist.github.com/GwiHwan-Go"
BAST_GIST_URL = "https://api.github.com/gists"
LOCATION = 'Asia/Shanghai' # 'Asia/Seoul'
SHORT_LOCATION = 'CST' # 'KST'

def load_contents(url) :
    response = requests.get(url)

    if response.status_code == 200:
        content = response.text
        return content
    else:
        print("Failed to fetch the content. Status code:", response.status_code)
        return None 

def unify_time_format(time_info, location='Asia/Shanghai') :
    """
    input time format : datetime module
    output time format : Sunday, 04 Sep, 09:01 KST
    
    """
    from pytz import timezone

    time_info=time_info.replace(tzinfo=timezone(location))

    return time_info.strftime("%A, %d %b, %H:%M")

def get_News_from_githubio_blogs() :
    def is_contents_line(line) :
        return ':' in line
    full_contents = load_contents(GITHUBIO_RAW_URL)
    news_section = full_contents.split('---')[3]
    parsed_contents = [line.strip() for line in news_section.split('\n') if is_contents_line(line)]
    return EMPTY_LINE +'- ' + '\n- '.join(parsed_contents)

def refine_url(url) :

    adress = GIT_URL
    git_address = '/'.split(url)[-1]
    return f"{adress}/{git_address}"

def gen_gist_info() :

    time_info = unify_time_format(get_created_at(gist_id), location=LOCATION)
    raw_url = get_url(gist_id)

    url_markdown = f"[Script Link]({refine_url(raw_url)})"
    target_text = f"Last updated : {time_info} {SHORT_LOCATION} | {url_markdown} \n"
    return target_text


def load_gists(gist_id):
    """translate Gist ID to URL"""

    gist_api = request.urlopen(BAST_GIST_URL + '/' + gist_id)
    jsons = loads(gist_api.read())
    # print(jsons.items())
    return jsons


def get_created_at(gist_id):
    """import from Gist"""
    import datetime

    files_json=load_gists(gist_id)
    content = files_json['updated_at']

    #get cur time
    currdate = datetime.datetime.strptime(content, '%Y-%m-%dT%H:%M:%SZ')

    if currdate.hour+9 >= 24:
        timezone_time = currdate.hour+9-24
    else :
        timezone_time = currdate.hour+9

    currdate = currdate.replace(hour=timezone_time)
    currdate = currdate.replace(second=0)

    return currdate

def get_url(gist_id):
    """import from Gist"""
    files_json=load_gists(gist_id)
    content = files_json['url']

    return content
