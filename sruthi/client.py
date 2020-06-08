# -*- coding: utf-8 -*-

import requests
from . import errors
from . import xmlparse
from . import response


class Client(object):
    def __init__(self, url=None):
        self.url = url
        # get explain here to get supported version?
        # get number_of_records from explain as well

    def searchretrieve(self, query, start_record=1):
        params = {
            'operation': 'searchretrieve',
            'version': '1.2',
            'query': query,
            'startRecord': start_record,
        }
        data_loader = DataLoader(self.url, params) 
        return response.SearchRetrieveResponse(data_loader)

    def explain(self):
        params = {
            'operation': 'explain',
            'version': '1.2',
        }
        data_loader = DataLoader(self.url, params) 
        return response.ExplainResponse(data_loader)


class DataLoader(object):
    def __init__(self, url, params):
        self.session = requests.Session()
        self.url = url
        self.params = params
        self.response = None
        self.xmlparser = xmlparse.XMLParser()

    def load(self, **kwargs):
        self.params.update(kwargs)
        xml = self._get_content(self.url, self.params)
        self._check_errors(xml)
        return xml

    def _get_content(self, url, params):
        try:
            res = self.session.get(
                url,
                params=params
            )
            res.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise errors.SruthiError("HTTP error: %s" % e)
        except requests.exceptions.RequestException as e:
            raise errors.SruthiError("Request error: %s" % e)

        return self.xmlparser.parse(res.content)

    def _check_errors(self, xml):
        sru = '{http://www.loc.gov/zing/srw/}'
        diagnostics = self.xmlparser.find(
            xml,
            f'{sru}diagnostics/{sru}diagnostic'
        )
        if diagnostics:
            error_msg = " ".join([d.find('detail').text for d in diagnostics])
            raise errors.SruError(error_msg)
