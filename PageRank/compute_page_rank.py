"""
usage: `compute_page_rank.py url_list_path path_to_data`

`path_to_data` needs to be a path to a directory that contains the
scraped results of from wget.
`url_list_path`: a text file of the urls we're looking at.

requires python3
"""


from urllib.parse import urlparse
import sys
from os import walk
from os.path import expanduser
import glob


import networkx
import pandas as pd
from bs4 import BeautifulSoup


def pagerank_to_csv(data_path, raw_url_path):
    page_rank = calculate_pagerank(data_path, raw_url_path)
    page_rank.to_csv('page_rank.csv')


def calculate_pagerank(data_path, raw_url_path):
    url_df = url_dataframe(raw_url_path)
    url_df = add_hosts(url_df, 0)
    page_graph = initialize_graph(url_df)
    edge_pairs = generate_edge_pairs(data_path, url_df)
    return add_pagerank(url_df, edge_pairs, page_graph)


def add_pagerank(urldf, edge_tups, page_graph):
    page_graph.add_edges_from(edge_tups)
    ser = pd.Series(networkx.pagerank(page_graph))
    ser.name = "pagerank"
    return urldf.join(ser)


def url_dataframe(raw_url_path):
    return pd.read_csv(raw_url_path, header=None)


def get_datapath_len(data_path):
    return len(data_path.strip("/").split("/"))


def get_all_netlocs(soup):
    return get_netlocs(get_all_links(soup))


def get_all_links(soup):
    a_s = soup.find_all('a')
    hrefs = (a.attrs['href'] for a in a_s if 'href' in a.attrs.keys())
    return hrefs


def get_hostname(x): return urlparse(x).hostname


def get_netlocs(hrefs):
    return (get_hostname(href) for href in hrefs if href is not None)


def get_netlocs_file_list(base, none, file_list):
    soups = [BeautifulSoup(open(base + "/" + file), 'lxml')
             for file in file_list if file.split(".")[-1] == "html"]
    netloc_list_o_lists = [set(get_all_netlocs(soup)) for soup in soups]
    if len(netloc_list_o_lists) > 0:
        return netloc_list_o_lists[0].union(*netloc_list_o_lists[1:])


def get_origin_site(base, none, file_list, datapath_len=7):
    return base.split("/")[datapath_len]


def generate_edge_pairs(data_path, url_df):
    all_urls = glob.glob(data_path)
    datapath_len = get_datapath_len(data_path)
    l = []
    for i in all_urls:
        for j in walk(i):
            try:
                l.append(((get_origin_site(*j, datapath_len=datapath_len),
                           get_netlocs_file_list(*j))))
            except UnicodeError:
                pass
    tups = [target_urls_to_tuple_list(*tup, url_df=url_df)
            for tup in l if tup[1] is not None]
    flattened = flatten_list(tups)
    return [(a, b) for a, b in flattened if b is not None]


def add_hosts(url_dataframe, url_column):
    hosts = url_dataframe[url_column].apply(get_hostname)
    url_dataframe['hosts'] = hosts
    return url_dataframe


def initialize_graph(url_data_frame):
    node_indeces = url_data_frame.index.tolist()
    page_graph = networkx.Graph()
    page_graph.add_nodes_from(node_indeces)
    return page_graph


def url_index(netloc, urls):
    if netloc is not None:
        try:
            return urls[urls['hosts'] == netloc].index[0]
        except IndexError:
            return None


def target_urls_to_tuple_list(origin_page, target_list, url_df=None):
    target_ids = (url_index(url, url_df) for url in target_list)
    origin_id = url_index(origin_page, url_df)
    return [(origin_id, target_id) for target_id in target_ids
            if target_id is not None]


def flatten_list(li):
    return [item for sublist in li for item in sublist]


def _main():
    data_path = expanduser(sys.argv[2])
    raw_url_path = expanduser(sys.argv[1])
    pagerank_to_csv(data_path, raw_url_path)


if __name__ == "__main__":
    _main()
