class Data(object):
    """ Data belong to an Actor
                attributes
        id      (str):  id of data
        api     (API):  api for crawl data
    """

    def __init__(self, id, api, **kargs):
        super(object, self).__init__()
        self.id = id
        self.api = api


class FilterInterface():
    """Filter Interface implement all filter on specific data
                        methods
            has_keywords()      (bool): return True if data has message which contains keywords. When contain_all==True
                                        the message must contain all words in keywords.
            in_time()           (bool): return True if data has created_time in range in_time. If in_time is single value
                                        the method will return True if created_time==in_time.
            by_actor()          (bool): return True if data was created by actor who has specific id.
    """

    def has_keywords(self, keywords, contain_all=True):
        if type(keywords) is not list:
            keywords = [keywords]
        keywords = list(set(keywords))  # each keyword must exist once
        key_in = list(filter(lambda x: x in self.message, keywords))
        if (len(key_in) == len(keywords)) ^ contain_all == False:  # if contain_all and key_in==keywords are the same
            return True
        return False

    def in_time(self, time_range):
        try:
            if self.time in range(time_range[0], time_range[1]):
                return True
            else:
                return False
        except IndexError:
            if self.time == time_range:
                return True
            else:
                return False
        except AttributeError:
            return False

    def by_actor(self, actor_id):
        try:
            if str(self.actor_id) == actor_id:
                return True
            else:
                return False
        except AttributeError:
            return False


class FriendList(Data):
    """FriendList is an list of friends, belong to a User
                    attributes
        id      (str):  id of friendlist
        name    (str):  name of friendlist
                    methods
        all     (list): return list of friends id
    """

    def __init__(self, id, api, name):
        super(FriendList, self).__init__(id, api)
        self.name = name
        self.api.use_table('FriendList')

    def all(self):
        members = self.api.get(fields='uid', id=self.id)
        results = list()
        for member in members:
            results.append(member['uid'])
        return results


class Post(Data, FilterInterface):
    """ Post is an Actor's post
                        attributes
            id          (str):  id of comment, maybe None if API not support
            message     (str):  message of comment
            actor_id    (str):  id of actor who created the comment
            create_time (int):  Linux time
                        methods
            Class FilterInterface  :  implement
    """

    def __init__(self, id, api, fields=['message', 'created_time', 'actor_id']):
        super(Post, self).__init__(id=id, api=api)
        self.api.use_table('Post')
        try:
            content = self.api.get(fields=fields, id=self.id)
        except IndexError:
            content = {}
            for field in fields:
                content.update({field: ''})
        finally:
            for field in fields:
                setattr(self, field, content[field])

    def comments(self):
        response = self.api.get(fields='comments', id=self.id)
        results = []
        for res in response:
            results.append(Comment(message=res['text'], created_time=res['time'], actor_id=res['fromid']))
        return results


class Comment(Data, FilterInterface):
    """ Comment is comment on an Object(Post,Photos,..)
                    attributes
        id          (str):  id of comment, maybe None if API not support
        message     (str):  message of comment
        actor_id    (str):  id of actor who created the comment
                    methods
        Class FilterInterface  :  implement
    """

    def __init__(self, message, created_time, actor_id, id=None):
        super(Comment, self).__init__(id=id, api=None)
        self.message = message
        self.time = created_time
        self.actor_id = actor_id


class Album(Data):
    """docstring for Album"""

    def __init__(self, arg):
        super(Album, self).__init__()
        self.arg = arg


class Photo(Data):
    """docstring for Photo"""

    def __init__(self, arg):
        super(Photo, self).__init__()
        self.arg = arg
