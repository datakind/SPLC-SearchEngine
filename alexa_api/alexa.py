__author__ = "Ruby Chu - github: rubesc, Vito A. Colano - github: vcolano"
__email__ = "ruby.w.chu@gmail.com, vcolano@gmail.com"

import awis
import getpass
import lxml
from json import loads, dumps
import pprint
import pickle
import pandas as pd
import numpy as np
import os
import xmltodict
from collections import defaultdict

class Alexa():
    """
    A wrapper for theAmazon Alexa Web Information Service API with functionality to expand a dataset of website urls.

    Information about the API can be found here:
    http://docs.aws.amazon.com/AlexaWebInfoService/latest/index.html?IntroductionArticle.html

    Information about obtaining an access_id/secret pair for AWIS can be found here:
    https://aws.amazon.com/awis/faqs/#general_5

    Information on the awis Python library wrapping the API can be found here:
    https://pypi.python.org/pypi/python-awis/1.2.1
    """

    # the AWS access id, a root user's access_id/secret pair must be used, an IAM user's pair cannot be used
    ACCESS_ID = "AKIAIIKNPTNCGEICYBIQ"

    # the features to request from the url_info endpoint
    URL_INFO_RESPONSE_PARAMETERS = ['RelatedLinks', 'Categories', 'Rank', 'RankByCountry', 'UsageStats', 'AdultContent',
                                    'Speed', 'Language', 'OwnedDomains', 'LinksInCount', 'SiteData']

    # the features that will be added from the url_info endpoint
    URL_INFO_FEATURE_NAMES = ['ExternalLinksToSite', 'OwnersOtherDomains', 'SiteDescription', 'OnlineSince',
                              'SiteTitle', 'ThreeMonthAvgUSRank', 'PageViewsPerMillion', 'PageViewsPerUser',
                              'ContributingSubdomains']

    # path to the source dataset of websites
    URLS_DATASET_PATH = '..' + os.sep + 'preDive' + os.sep + 'hatesitesDB.csv'

    # namespaces to filter out when parsing the xml response payload from the url info AWIS endpoint
    URL_INFO_NAMESPACES = {
        'http://alexa.amazonaws.com/doc/2005-10-05/': None,
        'http://awis.amazonaws.com/doc/2005-07-11': None
    }

    def __init__(self):
        """Initializes the AWIS API connection and loads the source dataset of websites"""
        self.secret = getpass.getpass(prompt='AWS Secret Key:')
        self.api = awis.AwisApi(Alexa.ACCESS_ID, self.secret)
        self.urls_df = pd.read_csv(Alexa.URLS_DATASET_PATH)

    def create_url_info_dataset(self):
        """
        Iterates over all of the website urls in URL_DATASET_PATH and generates supplementary features on the websites
        using the URL_INFO AWIS api.

        :return: a pandas DataFrame with the original features and supplementary features
        """
        all_cols = list(self.urls_df.columns.get_values()) + Alexa.URL_INFO_FEATURE_NAMES
        features_dict = dict((col, []) for col in all_cols)
        for _, row in self.urls_df.iterrows():
            features = self.url_info(row['Website'])
            if not features:
                continue
            for col_name in Alexa.URL_INFO_FEATURE_NAMES:
                if col_name in Alexa.URL_INFO_FEATURE_NAMES:
                    features_dict[col_name].append(features.get(col_name))
                else:
                    features_dict[col_name].append(row[col_name])

        with open('/home/vito/projects/SPLC-SearchEngine/alexa_api/features_dict_serialized.txt', 'wb') as f:
            ser = pickle.dump(features_dict, f)

        expanded_df = pd.DataFrame.from_dict(features_dict)
        return expanded_df

    def url_info(self, url):
        """
        Uses the AWIS url_info endpoint to obtain a set of features on a URL. Note that the endpoint extacts and
        returns a subset of all of the available features.

        TODO: A subject matter expert should evaluate the list of available features that the endpoint returns and
        update the dictionary returned by this function accordingly. For more information on all features returned, see:
        http://docs.aws.amazon.com/AlexaWebInfoService/latest/index.html?IntroductionArticle.html

        :param url: the url to request features on
        :return: a dictionary of useful features pulled from the response
        """
        xml_response = self.api.url_info(url, *Alexa.URL_INFO_RESPONSE_PARAMETERS, as_xml=False)
        res_dict = loads(dumps(xmltodict.parse(xml_response, process_namespaces=True, namespaces=Alexa.URL_INFO_NAMESPACES)))
        flat_dict = {}
        if not res_dict['UrlInfoResponse']['Response']['ResponseStatus']['StatusCode'] == 'Success':
            print("Error, unsuccessful response from api for the following url:\t" + url)
            return None
        elif 'Alexa' in res_dict['UrlInfoResponse']['Response']['UrlInfoResult']:
            if 'ContentData' in res_dict['UrlInfoResponse']['Response']['UrlInfoResult']['Alexa']:
                content = res_dict['UrlInfoResponse']['Response']['UrlInfoResult']['Alexa']['ContentData']
                flat_dict['ExternalLinksToSite'] = content.get('LinksInCount')
                flat_dict['OwnersOtherDomains'] = content.get('OwnedDomains')
                if 'SiteData' in content:
                    flat_dict['SiteDescription'] = content['SiteData'].get('Description')
                    flat_dict['OnlineSince'] = content['SiteData'].get('OnlineSince')
                    flat_dict['SiteTitle'] = content['SiteData'].get('Title')
            if 'TrafficData' in res_dict['UrlInfoResponse']['Response']['UrlInfoResult']['Alexa']:
                traffic = res_dict['UrlInfoResponse']['Response']['UrlInfoResult']['Alexa']['TrafficData']
                flat_dict['ThreeMonthAvgUSRank'] = traffic.get('Rank')
                if traffic.get('UsageStatistics') and traffic['UsageStatistics'].get('UsageStatistic'):
                    try:
                        if isinstance(traffic['UsageStatistics']['UsageStatistic'], dict):
                            usage_stat = traffic['UsageStatistics']['UsageStatistic']
                        else:
                            usage_stat = traffic['UsageStatistics']['UsageStatistic'][0]
                        if 'PageViews' in usage_stat:
                            pageviews = usage_stat['PageViews']
                            if 'PerMillion' in pageviews:
                                flat_dict['PageViewsPerMillion'] = pageviews['PerMillion'].get('Value')
                            if 'PerUser' in pageviews:
                                flat_dict['PageViewsPerUser'] = pageviews['PerUser'].get('Value')
                    except KeyError as e:
                        pass
                if traffic.get('ContributingSubdomains') and \
                        traffic['ContributingSubdomains'].get('ContributingSubdomain'):
                    subdomains = ''
                    for subdomain in traffic['ContributingSubdomains']['ContributingSubdomain']:
                        if isinstance(subdomain, dict):
                            subdomains += subdomain.get('DataUrl') + ', '
                        else:
                            subdomains = subdomain
                    flat_dict['ContributingSubdomains'] = subdomains.strip(', ')
        return flat_dict

a = Alexa()
df = a.create_url_info_dataset()