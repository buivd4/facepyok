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
        return Stream(id=self.id, api=self.api)


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

    def __init__(self, api, username=4, id=None):
        api.use_table('User')
        if id is None:
            response = api.get(fields='uid', id=username)
            id = response['uid']
            super(User, self).__init__(id, api)
            self.username = username
        else:
            super(User, self).__init__(id, api)
            self.username = self.username()

    def __info(self, fields):
        return self.api.get(fields=fields, id=self.id)

    def friends(self):
        friends = []
        flids = self.api.get(fields='flid', id=self.id)
        for flid in flids:
            friends.extend(FriendList(id=flid, api=self.api).all())
        return friends

    def fullname(self):
        return self.__info(['first_name', 'middle_name', 'last_name'])

    def avatar(self):
        return self.__info('pic')['pic']

    def religion(self):
        return self.__info('religion')['religion']

    def birthday(self):
        return self.__info('birthday')['birthday']

    def sex(self):
        return self.__info('sex')['sex']

    def current_location(self):
        return self.__info('current_location')['current_location']

    def online_presence(self):
        return self.__info('online_presence')['online_presence']

    def locale(self):
        return self.__info('locale')['locale']

    def email(self):
        return self.__info('email')['email']

    def username(self):
        return self.__info('username')['username']
