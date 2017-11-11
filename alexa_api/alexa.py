"""
Contains functionality to use the Amazon Alexa Web Information Service API. This API provides several endpoints
to get information on a URL such as site visit volume, site owner(s), external sites linking to the page and more.

Information about the API can be found here:
http://docs.aws.amazon.com/AlexaWebInfoService/latest/index.html?IntroductionArticle.html

Information on the awis Python library wrapping the API can be found here:
https://pypi.python.org/pypi/python-awis/1.2.1


"""

__author__ = "Ruby Chu - github: rubesc, Vito Colano - github: vcolano"
__email__ = "ruby.w.chu@gmail.com, vcolano@gmail.com"

import awis
import getpass
import pprint

class Alexa():

    ACCESS_ID = "AKIAJ7RW7AUZHPYNGWAA"
    URL_INFO_RESPONSE_PARAMETERS = ['RelatedLinks', 'Categories', 'Rank', 'RankByCountry', 'UsageStats', 'AdultContent',
                                    'Speed', 'Language', 'OwnedDomains', 'LinksInCount', 'SiteData']

    def __init__(self):
        self.secret = getpass.getpass()
        self.api = awis.AwisApi(Alexa.ACCESS_ID, self.secret)

    def url_info(self):
        return self.api.url_info("vdare.com", *Alexa.URL_INFO_RESPONSE_PARAMETERS)

a = Alexa()
pprint.pprint(a.url_info())