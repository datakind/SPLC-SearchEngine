"""
Contains functionality to use the Amazon Alexa Web Information Service API. This API provides several endpoints
to get information on a URL such as site visit volume, site owner(s), external sites linking to the page and more.

Information about the API can be found here:
http://docs.aws.amazon.com/AlexaWebInfoService/latest/index.html?IntroductionArticle.html

Information about obtaining an access_id/secret pair for AWIS can be found here:
https://aws.amazon.com/awis/faqs/#general_5

Information on the awis Python library wrapping the API can be found here:
https://pypi.python.org/pypi/python-awis/1.2.1


"""

__author__ = "Ruby Chu - github: rubesc, Vito Colano - github: vcolano"
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

    ACCESS_ID = "AKIAIIKNPTNCGEICYBIQ"

    # the features to request from the url_info endpoint
    URL_INFO_RESPONSE_PARAMETERS = ['RelatedLinks', 'Categories', 'Rank', 'RankByCountry', 'UsageStats', 'AdultContent',
                                    'Speed', 'Language', 'OwnedDomains', 'LinksInCount', 'SiteData']

    # the features that will be added from the url_info endpoint
    URL_INFO_FEATURE_NAMES = ['ExternalLinksToSite', 'OwnersOtherDomains', 'SiteDescription', 'OnlineSince',
                              'SiteTitle', 'ThreeMonthAvgUSRank', 'PageViewsPerMillion', 'PageViewsPerUser',
                              'ContributingSubdomains']
    URLS_DATASET_PATH = '..' + os.sep + 'preDive' + os.sep + 'hatesitesDB.csv'
    NAMESPACES = {
        'http://alexa.amazonaws.com/doc/2005-10-05/': None,
        'http://awis.amazonaws.com/doc/2005-07-11': None
    }

    def __init__(self):
        self.secret = getpass.getpass(prompt='AWS Secret Key:')
        self.api = awis.AwisApi(Alexa.ACCESS_ID, self.secret)
        self.urls_df = pd.read_csv(Alexa.URLS_DATASET_PATH)

    def create_url_info_dataset(self):
        expanded_df = self.urls_df.copy()
        #expanded_df.index = expanded_df.Website.copy()
        for col in Alexa.URL_INFO_FEATURE_NAMES:
            expanded_df[col] = np.NAN

        count = 0
        for site in self.urls_df['Website']:
            features = self.url_info(site)
            if not features:
                continue
            for col_name in Alexa.URL_INFO_FEATURE_NAMES:
                expanded_df.iloc[count, expanded_df.columns.get_loc(col_name)] = features.get(col_name)
            count += 1

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
        res_dict = loads(dumps(xmltodict.parse(xml_response, process_namespaces=True, namespaces=Alexa.NAMESPACES)))
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
                if 'UsageStatistics' in traffic and traffic['UsageStatistics'] \
                    and 'UsageStatistic' in traffic['UsageStatistics'] and\
                    traffic['UsageStatistics']['UsageStatistic']:
                    if traffic['UsageStatistics']['UsageStatistic'][0] and \
                                    'PageViews' in traffic['UsageStatistics']['UsageStatistic'][0]:
                        pageviews = traffic['UsageStatistics']['UsageStatistic'][0]['PageViews']
                        if 'PerMillion' in pageviews:
                            flat_dict['PageViewsPerMillion'] = pageviews['PerMillion'].get('Value')
                        if 'PerUser' in pageviews:
                            flat_dict['PageViewsPerUser'] = pageviews['PerUser'].get('Value')
                if 'ContributingSubdomains' in traffic and traffic['ContributingSubdomains'] and \
                        traffic['ContributingSubdomains']['ContributingSubdomain']:
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