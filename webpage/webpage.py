import sys
import os
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from lib.lib import all_links, process_link, normalize_link, is_relative
import shutil

out_dir = './out'

params = {}

def process_html_content(url, content, encoding):
    download_url = params["download_url"]
    replace_url = params['replace_url'] if params.get('replace_url') is not None else ''

    wp = BeautifulSoup(content, 'html.parser')
    links = set()
    for link_elem in wp.find_all('a'):
        link_str = link_elem.get('href')
        # print(orig_link)
        n = urlparse(normalize_link(url, link_str))

        # only grap same origin htmls:
        print(n, url)
        if n.netloc == url.netloc:
            links.add(n.geturl())

            # change urls
            if not is_relative(link_str):
                link_elem['href'] = n._replace(netloc=replace_url)

    # remove "powered by" script
    powered_script = wp.find("script", string=re.compile("poweredByHTML"))
    if powered_script:
        powered_script.decompose()

    str_out = str(wp)

    if replace_url != '':
        # change meta and link tags
        for meta_elem in wp.find_all('meta',content=download_url):
            meta_elem['content'] = replace_url

        for meta_elem in wp.find_all('link',href=download_url):
            meta_elem['href'] = replace_url

        # replace other occurrences of the download URL
        str_out = str_out.replace(download_url,replace_url)

    return (str_out, list(links))


def process_html_file(link):
    file = link.path

    if file == '' or file[-1] == '/':
        file = '/index.html'

    p = file.split('.')
    if p[-1] != 'html':
        file = '.'.join(p) + '.html'

    return out_dir+'/'+link.netloc+file
    
def copy_directory_contents(source_dir, target_dir):
    """
    Copy all files from source_dir to target_dir.
    Both directories should already exist.
    
    Args:
        source_dir (str): Path to the source directory
        target_dir (str): Path to the target directory
    """
    if not os.path.exists(source_dir):
        print(f"Source directory {source_dir} does not exist.")
        return False
    
    if not os.path.exists(target_dir):
        print(f"Target directory {target_dir} does not exist.")
        return False
    
    try:
        # Walk through the source directory
        for root, dirs, files in os.walk(source_dir):
            # Calculate the relative path from source_dir
            rel_path = os.path.relpath(root, source_dir)
            # Create the corresponding directory in target_dir if it doesn't exist
            if rel_path != '.':
                target_subdir = os.path.join(target_dir, rel_path)
                os.makedirs(target_subdir, exist_ok=True)
            
            # Copy all files in the current directory
            for file in files:
                source_file = os.path.join(root, file)
                if rel_path == '.':
                    target_file = os.path.join(target_dir, file)
                else:
                    target_file = os.path.join(target_dir, rel_path, file)
                shutil.copy2(source_file, target_file)
        
        return True
    except Exception as e:
        print(f"Error copying files: {e}")
        return False

def download_webpage(download_url, replace_url):

    params["download_url"] = download_url

    if replace_url:
        params["replace_url"] = replace_url

    download_page_runner = all_links(download_url,
                       process_link(
                           'text/html', process_html_content, process_html_file))

    download_page_runner()
    copy_directory_contents('./public', './out')
    
    
def download_webpage_cmd():
    argv = dict(enumerate(sys.argv))
    replace_env = os.getenv('DOWNLOAD_WEBPAGE_URL')
    download_url = replace_env if replace_env is not None else argv.get(1)

    replace_env = os.getenv('REPLACE_WEBPAGE_URL')
    replace_url = replace_env if replace_env is not None else argv.get(2)
    
    if download_url is None:
        print("provide a URL to download (cmd argument or ENV variable)")
        return
    
    return download_webpage(download_url, replace_url)