from facepyok.data import Post


class Stream(object):
    """ user's stream or the user's profile """

    def __init__(self, id, api, vtype='source_id'):
        super(Stream, self).__init__()
        self.id = id
        self.type = vtype
        self.api = api
        self.api.use_table('Stream')

    def permalink(self):
        return self.api.get(fields='permalink', id=self.id)['permalink']

    def posts(self, post_fields=['message', 'created_time', 'actor_id']):
        results = []
        response = self.api.get(fields='post_id', id=self.id)
        for post in response:
            results.append(Post(id=post['post_id'], api=self.api))
        return results

    def contents_by_actor(self, actor_id, post_fields=['message', 'created_time', 'actor_id']):
        results = []
        for post in self.posts(post_fields):
            if post.by_actor(actor_id):
                results.append(post)
        return results

    def contents_has_keywords(self, keywords, contain_all=True, post_fields=['message', 'created_time', 'actor_id']):
        results = []
        for post in self.posts(post_fields):
            if post.has_keywords(keywords, contain_all):
                results.append(post)
        return results
