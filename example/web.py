import json
from vers import web
from . import models


class Handler(web.BaseHandler):
    def before_request(self):
        super(Handler, self).before_request()
        self.db = self.app.Session()
        ''':type : sqlalchemy.orm.Session'''

    def after_request(self):
        super(Handler, self).after_request()
        self.db.close()


def serialize_post(post):
    return {'id': post.id, 'title': post.title}


def serialize_posts(query):
    data = []
    for obj in query:
        data.append(serialize_post(obj))
    return {'data': data}


def as_json(value):
    return web.Response(json.dumps(value), mimetype='application/json')


class PostsHandler(Handler):
    @web.query_arg('offset', default=0, type=int)
    @web.respond_with(serialize_posts, as_json)
    def get(self, offset):
        return (self.db.query(models.Post)
                .order_by(models.Post.id.desc())
                .offset(offset))

    @web.form_arg('title', required=True)
    @web.respond_with(serialize_post, as_json)
    def post(self, title):
        post = models.Post(title=title)
        self.db.add(post)
        self.db.commit()
        return post


class PostHandler(Handler):
    @web.path_arg('id')
    def before_request(self, id):
        super(PostHandler, self).before_request()
        self.post = self.db.query(models.Post).get(id)

    @web.respond_with(serialize_post, as_json)
    def get(self):
        return self.post

    @web.respond_with(as_json)
    def delete(self):
        self.db.delete(self.post)
        return {'ok': True}