import os
from urllib.parse import urlparse

import requests


def save_file(res, path):
    (dir, name) = os.path.split(path)
    os.makedirs(dir, exist_ok=True)
    with open(path, 'wb') as fout:
        for chunk in res:
            fout.write(chunk)


def normalize_link(base, linkstr):
    n = urlparse(linkstr)
    if n.netloc == '':
        return base.scheme + '://'+base.netloc + base.path + n.path
    else:
        return linkstr


def _normalize_links(base, links):
    out = []
    for link in links:
        out.append(normalize_link(base, link))
    return out


def process_link(content_types, process_content, process_file):

    def res(base, req):
        links = []
        # print(req.headers)
        if req.headers['content-type'] in content_types:
            if process_content:
                encoding = req.encoding
                links = process_content(base, req.content, encoding)
            out_file = process_file(base)
            print("out: ", out_file)
            save_file(req, out_file)

        return _normalize_links(base, links)
        # return links

    return res


def add_links(stack, new_links):
    for nl in new_links:
        if stack.get(nl):
            pass
        else:
            stack[nl] = False


def all_links(root, *args):
    links_stack_processed = {}
    links_stack_processed[root] = False

    def run():
        while True:
            _link = next(
                (key for key in links_stack_processed if not links_stack_processed[key]), False)
            if not _link:
                break
            print("link: ", _link)
            req = requests.get(_link)
            print("code: ", req.status_code)
            if req.status_code == 404:
                links_stack_processed[_link] = True
                continue
            for handler in args:
                link = urlparse(_link)
                new_links = handler(link, req)
                print("new links: ", new_links)
                add_links(links_stack_processed, new_links)
                links_stack_processed[_link] = True

    return run
