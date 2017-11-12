"""
usage: `compute_page_rank.py url_list_path path_to_data`

`path_to_data` needs to be a path to a directory that contains the
scraped results of from wget.
`url_list_path`: a text file of the urls we're looking at.


Outputs to a csv named `page_rank.csv` in the directory in which the
program is run.

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


class PageRankComputerLocal():
    def __init__(self):
        pass

    def pagerank_to_csv(self, data_path, raw_url_path):
        page_rank = self.calculate_pagerank(data_path, raw_url_path)
        page_rank.to_csv('page_rank.csv')

    def calculate_pagerank(self, data_path, raw_url_path):
        url_df = self.url_dataframe(raw_url_path)
        url_df = self.add_hosts(url_df, 0)
        page_graph = self.initialize_graph(url_df)
        edge_pairs = self.generate_edge_pairs(data_path, url_df)
        return self.add_pagerank(url_df, edge_pairs, page_graph)

    def add_pagerank(self, urldf, edge_tups, page_graph):
        page_graph.add_edges_from(edge_tups)
        ser = pd.Series(networkx.pagerank(page_graph))
        ser.name = "pagerank"
        return urldf.join(ser)

    def url_dataframe(self, raw_url_path):
        return pd.read_csv(raw_url_path, header=None)

    def get_datapath_len(self, data_path):
        return len(data_path.strip("/").split("/"))

    def get_all_netlocs(self, soup):
        return self.get_netlocs(self.get_all_links(soup))

    def get_all_links(self, soup):
        a_s = soup.find_all('a')
        hrefs = (a.attrs['href'] for a in a_s if 'href' in a.attrs.keys())
        return hrefs

    def get_hostname(self, x):
        return urlparse(x).hostname

    def get_netlocs(self, hrefs):
        return (self.get_hostname(href) for href in hrefs if href is not None)

    def get_netlocs_file_list(self, base, none, file_list):
        soups = [BeautifulSoup(open(base + "/" + file), 'lxml')
                 for file in file_list if file.split(".")[-1] == "html"]
        netloc_list_o_lists = [set(self.get_all_netlocs(soup))
                               for soup in soups]
        if len(netloc_list_o_lists) > 0:
            return netloc_list_o_lists[0].union(*netloc_list_o_lists[1:])

    def get_origin_site(self, base, none, file_list, datapath_len=7):
        return base.split("/")[datapath_len]

    def generate_edge_pairs(self, data_path, url_df):
        all_urls = glob.glob(data_path)
        datapath_len = self.get_datapath_len(data_path)
        l = []
        for i in all_urls:
            for j in walk(i):
                try:
                    l.append(((self.get_origin_site(*j,
                                                    datapath_len=datapath_len),
                               self.get_netlocs_file_list(*j))))
                except UnicodeError:
                    pass
        tups = [self.target_urls_to_tuple_list(*tup, url_df=url_df)
                for tup in l if tup[1] is not None]
        flattened = self.flatten_list(tups)
        return [(a, b) for a, b in flattened if b is not None]

    def add_hosts(self, url_dataframe, url_column):
        hosts = url_dataframe[url_column].apply(self.get_hostname)
        url_dataframe['hosts'] = hosts
        return url_dataframe

    def initialize_graph(self, url_data_frame):
        node_indeces = url_data_frame.index.tolist()
        page_graph = networkx.Graph()
        page_graph.add_nodes_from(node_indeces)
        return page_graph

    def url_index(self, netloc, urls):
        if netloc is not None:
            try:
                return urls[urls['hosts'] == netloc].index[0]
            except IndexError:
                return None

    def target_urls_to_tuple_list(self, origin_page, target_list, url_df=None):
        target_ids = (self.url_index(url, url_df) for url in target_list)
        origin_id = self.url_index(origin_page, url_df)
        return [(origin_id, target_id) for target_id in target_ids
                if target_id is not None]

    def flatten_list(self, li):
        return [item for sublist in li for item in sublist]


class PageRankS3Bucket(PageRankComputerLocal):
    def __init__(self, boto_bucket):
        self.boto_bucket = boto_bucket

    def edges_from_bucket(self, boto_bucket):
        file_objects = boto_bucket.objects.all()
        html_files = (obj for obj in file_objects if self.is_html(obj.key))
        hostnames = [self.get_hostname(obj.key) for obj in html_files]
        link_hostnames = (self.get_all_link_hostnames(obj)
                          for obj in html_files)
        return [(origin, targets) for origin, targets
                in zip(hostnames, link_hostnames) if len(targets) > 0]

    def calculate_pagerank(self, boto_bucket, raw_url_path):
        url_df = self.url_dataframe(raw_url_path)
        url_df = self.add_hosts(url_df, 0)
        page_graph = self.initialize_graph(url_df)
        edge_pairs = self.generate_edge_pairs(boto_bucket, url_df)
        return self.add_pagerank(url_df, edge_pairs, page_graph)

    def is_html(self, boto_key):
        return boto_key.split(".")[-1] == 'html'

    def generate_edge_pairs(self, boto_bucket, url_df):
        url_edges = self.edges_from_bucket(boto_bucket)
        tups = [self.target_urls_to_tuple_list(*tup, url_df=url_df)
                for tup in url_edges if tup[1] is not None]
        flattened = self.flatten_list(tups)
        return [(a, b) for a, b in flattened if b is not None]

    def pagerank_to_csv(self, boto_bucket, raw_url_path):
        page_rank = self.calculate_pagerank(boto_bucket, raw_url_path)
        page_rank.to_csv('page_rank.csv')

    def get_all_link_hostnames(self, obj):
        body = obj.get()['Body'].read()
        soup = BeautifulSoup(body, 'lxml')
        return self.get_all_netlocs(soup)


def _main():
    ranker = PageRankComputerLocal()
    data_path = expanduser(sys.argv[2])
    raw_url_path = expanduser(sys.argv[1])
    ranker.pagerank_to_csv(data_path, raw_url_path)


if __name__ == "__main__":
    _main()
