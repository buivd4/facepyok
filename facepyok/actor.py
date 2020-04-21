from facepyok.data import FriendList
from facepyok.stream import Stream


class Actor(object):
    """Actor is User or Page, who can access data
                    attributes
        api         (API):  api to crawl data
        id          (str):  actor id
                    methods
        id()          (User): return all friends of the user if available
        feed()        (str):  return stream of user
    """

    def __init__(self, aid, api):
        super(Actor, self).__init__()
        self.id = aid
        self.api = api

    def id(self):
        return self.id

    def feed(self):
        return Stream(sid=self.id, api=self.api)


class User(Actor):
    """ Facebook User
                    attributes
        api         (API):  api to crawl data
        username    (str):  username
        id         (str):  id of user
                    methods
        friends()     (User): return all friends of the user if available
        fulname(),... (str):  return basic infomation of user
    """

    def __init__(self, api, username=4, uid=None):
        if uid is None:
            try:
                response = fql.get(token=token, table='user', fields='uid', conditions="username='%s'" % username)
                uid = response[0]['uid']
            except IndexError as err:
                print("PyFB: " + response['error']['message'])
                exit(-1)
            super(User, self).__init__(uid, api)
            self.username = username
        else:
            super(User, self).__init__(uid, api)
            self.username = self.username()

    def __info(self, fields):
        return self.api.get(table='user', fields=fields, conditions="uid='%s'" % self.id)

    def friends(self):
        friends = []
        flids = self.api.get(table='friendlist', fields=['flid'], conditions='owner=%s' % self.id)
        for flid in flids:
            friends.extend(FriendList(id=flid, api=self.api).all())
        return friends

    def fullname(self):
        return self.__info(['first_name', 'middle_name', 'last_name'])[0]

    def avatar(self):
        return self.__info('pic')[0]['pic']

    def religion(self):
        return self.__info('religion')[0]['religion']

    def birthday(self):
        return self.__info('birthday')[0]['birthday']

    def sex(self):
        return self.__info('sex')[0]['sex']

    def current_location(self):
        return self.__info('current_location')[0]['current_location']

    def online_presence(self):
        return self.__info('online_presence')[0]['online_presence']

    def locale(self):
        return self.__info('locale')[0]['locale']

    def email(self):
        return self.__info('email')[0]['email']

    def username(self):
        return self.__info('username')[0]['username']
