import sys
import os
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from lib.lib import all_links, process_link, normalize_link, is_relative

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


def main():

    argv = dict(enumerate(sys.argv))
    replace_env = os.getenv('DOWNLOAD_WEBPAGE_URL')
    download_url = replace_env if replace_env is not None else argv.get(1)

    if download_url is None:
        print("provide a URL to download (cmd argument or ENV variable)")
        return
    params["download_url"] = download_url

    replace_env = os.getenv('REPLACE_WEBPAGE_URL')
    replace_url = replace_env if replace_env is not None else argv.get(2)
    if replace_url:
        params["replace_url"] = replace_url

    runner = all_links(download_url,
                       process_link(
                           'text/html', process_html_content, process_html_file))

    runner()


main()
