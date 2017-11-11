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
import pprint
import pickle
import os

class Alexa():

    ACCESS_ID = "AKIAIIKNPTNCGEICYBIQ"
    URL_INFO_RESPONSE_PARAMETERS = ['RelatedLinks', 'Categories', 'Rank', 'RankByCountry', 'UsageStats', 'AdultContent',
                                    'Speed', 'Language', 'OwnedDomains', 'LinksInCount', 'SiteData']

    def __init__(self):
        self.secret = getpass.getpass()
        self.api = awis.AwisApi(Alexa.ACCESS_ID, self.secret)

    def url_info(self):
        return self.api.url_info("http://www.breitbart.com/", *Alexa.URL_INFO_RESPONSE_PARAMETERS)

    @staticmethod
    def etree_to_dict(t):
        d = {t.tag: map(Alexa.etree_to_dict, t.iterchildren())}
        d.update(('@' + k, v) for k, v in t.attrib.iteritems())
        d['text'] = t.text
        return d

a = Alexa()
res = a.url_info()
d = Alexa.etree_to_dict(res)

f = open('/home/vito/projects/SPLC-SearchEngine/alexa_api/example_lxml_obj.txt', 'wb')
pickle.dump(d, f)
f.close()