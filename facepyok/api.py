import json
import requests


class Api(object):
    """ Api is crawler API, which used to get data out"""

    def __init__(self, token):
        super(Api, self).__init__()
        self.token = token

    def use_table(self, table_name):
        self.table = table_name

    def map_function(self, table):
        map = {
            'user': '__get_user',
            'page': '__get_page',
            'group': '__get_group'
        }
        return map[table]

    def get(self, id, fields=None):
        return getattr(self, self.map_function(self.table))(id, fields)


class Fql(Api):
    """FQL: Facebook Query Language"""

    def __init__(self, token):
        super(Fql, self).__init__(token)

    URL = 'https://graph.facebook.com/fql?'

    def map_function(self, table):
        map = {
            'User': 'get_user',
            'Stream': 'get_stream',
            'Post': 'get_post',
            'FriendList': 'get_friendlist'
        }
        return map[table]

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

    def __url_builder(self, table, fields, conditions, **kargs):
        return Fql.URL + 'access_token=%s&q=%s' % (
        self.token, self.__query_builder(table=table, fields=fields, conditions=conditions, **kargs))

    def __get(self, table, fields, conditions):
        try:
            response = json.loads(
                requests.get(self.__url_builder(table=table, fields=fields, conditions=conditions)).content)
            return response['data']
        except KeyError:
            raise KeyError(response['error']['message'])

    def raw_query(self, query):
        try:
            response = json.loads(requests.get(Fql.URL + 'access_token=%s&q=%s' % (self.token, query)).content)
            return response['data']
        except KeyError:
            raise KeyError(response['error']['message'])

    def get_stream(self, id, fields):
        return self.__get(table='stream', fields=fields, conditions="source_id='%s'" % id)

    def get_user(self, id, fields):
        if fields == 'flid':
            return self.__get(table='friendlist', fields='flid', conditions="owner='%s'" % id)
        try:
            return self.__get(table='user', fields=fields, conditions="uid='%s'" % int(id))[0]
        except ValueError:
            return self.__get(table='user', fields=fields, conditions="username='%s'" % id)[0]

    def get_post(self, id, fields):
        if fields == 'comments':
            return self.__get(table='comment', fields=['text', 'time', 'fromid'], conditions="post_id='%s'" % id)
        return self.__get(table='stream', fields=fields, conditions="post_id='%s'" % id)[0]

    def get_friendlist(self, id, fields):
        return self.__get(table='friendlist_member', fields=fields, conditions="flid='%s'" % id)
