#!/usr/bin/env python
# -*- coding: utf-8 -*-
# check
gist_id = "eb5d0abf02532775199f267397dc1b3d"

def load_gists(gist_id):
    """translate Gist ID to URL"""
    from json import loads
    from urllib import request

    gist_api = request.urlopen("https://api.github.com/gists/" + gist_id)
    jsons = loads(gist_api.read())
    # print(jsons.items())
    return jsons


def get_created_at(gist_id):
    """import from Gist"""
    files_json=load_gists(gist_id)
    content = files_json['updated_at']
    # print(content.items())

    return content

def get_url(gist_id):
    """import from Gist"""
    files_json=load_gists(gist_id)
    content = files_json['url']
    # print(content.items())

    return content

def unify_time_format(time_info, location='Asia/Seoul') :
    """
    input time format : 2022-09-04T00:01:07Z
    output time format : Sunday, 04 Sep, 09:01 KST
    
    """
    import datetime
    from pytz import timezone

    currdate = datetime.datetime.strptime(time_info, '%Y-%m-%dT%H:%M:%SZ')
    currdate=currdate.replace(tzinfo=timezone(location))

    return currdate.strftime("%A, %d %b, %H:%M")

def last_updated_time(script, index_pars) :

    import datetime
    with open(script, 'r', encoding='utf-8') as f:
        readme_list = f.readlines()
    f.close()

    upper_list, down_list = return_upper_down_text(index_pars, script)
    target = [i for i in readme_list if ((i not in upper_list) and (i not in down_list))]
    time_info = target[0].split('|')[0].strip()

    currdate = datetime.datetime.strptime(time_info, 'Last updated : %A, %d %b, %H:%M KST')
    currdate = currdate.replace(year = 2022)
    
    return currdate

def return_upper_down_text(index_pars, file_name) :
    """
    <--
    index_pars
    -->
    """
    with open(file_name, 'r', encoding='utf-8') as f:
        readme_list = f.readlines()
    f.close()
    bounds = [i for i, x in enumerate(readme_list) if x == index_pars]
    if len(bounds) !=2 :
        raise Exception(f"the number of bounds should be 2, here-{len(bounds)}")
    upper_bound = readme_list[:bounds[0]+2]
    down_bound = readme_list[bounds[1]-1:]
    return upper_bound, down_bound

def update_script(load_path, save_path, index_pars) :

    upper_list, down_list = return_upper_down_text(index_pars, load_path)
    upper_text, down_text = "".join(upper_list), "".join(down_list)

    time_info = unify_time_format(get_created_at(gist_id))
    url_markdown = f"[project]({get_url(gist_id)})"
    target_text = f"Last updated : {time_info} KST | {url_markdown} \n"
    readme_text = f"{upper_text}{target_text}{down_text}"

    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(readme_text)
    
    print("updated")
    print(target_text)

if __name__ == "__main__" :
    load_path = "README.md"
    save_path = "README.md"

    section_to_write = 'Footer\n'
    former = last_updated_time(load_path, section_to_write)
    new = get_created_at(gist_id)

    if former != new :
        update_script(load_path, save_path, section_to_write)

