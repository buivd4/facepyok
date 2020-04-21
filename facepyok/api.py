import json

import requests


class Api(object):
    """ Api is crawler API, which uses to get data out"""

    def __init__(self, token):
        super(Api, self).__init__()
        self.token = token

    def get(table, fields, conditions, **kwargs):
        pass


class Fql(Api):
    """FQL: Facebook Query Language"""

    def __init__(self, token):
        super(Fql, self).__init__(token)

    URL = 'https://graph.facebook.com/fql?'

    def __query_builder(self, table, fields, conditions, parenthese=False, limit=1000000):
        try:
            if type(fields) is str:
                fields = [fields]
            if not parenthese:
                return "SELECT %s FROM %s WHERE %s LIMIT %d" % (','.join(fields), table, conditions, limit)
            else:
                return "(SELECT %s FROM %s WHERE %s LIMIT %d)" % (','.join(fields), table, conditions, limit)
        except TypeError as err:
            print(err)

    def url_builder(self, table, fields, conditions, **kargs):
        return Fql.URL + 'access_token=%s&q=%s' % (
            self.token, self.__query_builder(table=table, fields=fields, conditions=conditions, **kargs))

    def url2id(self, url):
        return get(table='object_url', fields='id', conditions="url='%s'" % url)

    def id2url(self, oid):
        return get(table='object_url', fields='url', conditions="id='%s'" % oid)

    def get(self, table, fields, **kwargs):
        try:
            response = json.loads(
                requests.get(self.url_builder(table=table, fields=fields, conditions=kwargs['conditions'])).content)
            return response['data']
        except KeyError:
            raise KeyError(response['error']['message'])
