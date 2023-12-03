import json
from utils import gen_gist_info, get_News_from_githubio_blogs

def load_readme(file_name) :
    with open(file_name, 'r', encoding='utf-8') as f:
        readme_list = [l.strip() for l in f.readlines()]
    return readme_list
def save_readme(contents, file_name) :
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write('\n'.join(contents))
    f.close()


def load_section_info(file_name) :
    with open(file_name, 'r', encoding='utf-8') as f:
        sections_info = json.load(f)
    return sections_info

def flag_fixer(section_name) :
    return f"<!--{section_name}-->"

def get_new_contents(section_name) :

    if section_name == "Blog_Post" :
        return get_News_from_githubio_blogs()
    elif section_name == "Footer" : 
        return gen_gist_info()
    else :
        raise Exception(f"section name should be one of [Blog_Post, Footer], here-{section_name}")

def find_next_section(current_readme, upper_bound) :
    for idx, line in enumerate(current_readme[upper_bound:]) :
        if line.startswith("<!--") :
            return upper_bound + idx

def revise_section(new_contents : str, current_readme, section_name) :
    section_flag = flag_fixer(section_name)
    upper_bound = current_readme.index(section_flag)+1
    down_bound = find_next_section(current_readme, upper_bound)
    merged = current_readme[:upper_bound] + [new_contents] + current_readme[down_bound:]
    return merged

if __name__ == "__main__" :
    readmd_file_name = "README.md"
    section_names_file = "sections.json"

    current_readme = load_readme(readmd_file_name)
    section_info = load_section_info(section_names_file)
    for section_name, need_update in section_info.items() :
        if need_update :
            print(f"update {section_name}")
            new_contents = get_new_contents(section_name)
            current_readme = revise_section(new_contents, current_readme, section_name)
    
    save_readme(current_readme, readmd_file_name)
    ## load current README.md
    ## load workload and check if there is any update
    ## write the readmd.md file and upload 