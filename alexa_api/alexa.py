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
import os
import xmltodict
from collections import defaultdict

class Alexa():

    ACCESS_ID = "AKIAIIKNPTNCGEICYBIQ"
    URL_INFO_RESPONSE_PARAMETERS = ['RelatedLinks', 'Categories', 'Rank', 'RankByCountry', 'UsageStats', 'AdultContent',
                                    'Speed', 'Language', 'OwnedDomains', 'LinksInCount', 'SiteData']
    NAMESPACES = {
        'http://alexa.amazonaws.com/doc/2005-10-05/': None,
        'http://awis.amazonaws.com/doc/2005-07-11': None
    }

    def __init__(self):
        self.secret = getpass.getpass(prompt='AWS Secret Key:')
        self.api = awis.AwisApi(Alexa.ACCESS_ID, self.secret)

    def url_info(self, url):
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
                if 'UsageStatistics' in traffic and traffic['UsageStatistics']['UsageStatistic']:
                    if 'PageViews' in traffic['UsageStatistics']['UsageStatistic'][0]:
                        pageviews = traffic['UsageStatistics']['UsageStatistic'][0]['PageViews']
                        if 'PerMillion' in pageviews:
                            flat_dict['PageViewsPerMillion'] = pageviews['PerMillion'].get('Value')
                        if 'PerUser' in pageviews:
                            flat_dict['PageViewsPerUser'] = pageviews['PerUser'].get('Value')
                if 'ContributingSubdomains' in traffic and traffic['ContributingSubdomains']['ContributingSubdomain']:
                    subdomains = ''
                    for subdomain in traffic['ContributingSubdomains']['ContributingSubdomain']:
                        subdomains += subdomain.get('DataUrl') + ', '
                    flat_dict['ContributingSubdomains'] = subdomains.strip(', ')
        return flat_dict

a = Alexa()
res = a.url_info("http://www.breitbart.com/")

f = open('/home/vito/projects/SPLC-SearchEngine/alexa_api/example_lxml_obj.txt', 'wb')
pickle.dump(res, f)
f.close()