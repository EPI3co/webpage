from pywebcopy.parsers import MultiParser
from urllib.parse import urlparse
from lib.lib import all_links, process_link, normalize_link

out_dir = './out'


def process_html_content(url, content, encoding):
    wp = MultiParser(content, encoding)
    links = set()
    for linkStr in wp.bs4.find_all('a'):
        n = urlparse(normalize_link(url, linkStr.get('href')))

        # only grap same origin htmls:
        if n.netloc == url.netloc:
            links.add(n.geturl())

    # print(list(links))
    return list(links)


def process_html_file(link):
    # print(link)
    file = link.path

    if file == '' or file[-1] == '/':
        file = '/index.html'

    p = file.split('.')
    if p[-1] != 'html':
        file = '.'.join(p) + '.html'

    return out_dir+'/'+link.netloc+file


def main():

    url = 'https://einv-site.webflow.io/'

    runner = all_links(url, process_link(
        'text/html', process_html_content, process_html_file))

    runner()


main()
