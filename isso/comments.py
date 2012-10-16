
import time
import json

from werkzeug.wrappers import Response
from werkzeug.exceptions import abort


class Comment(object):
    """This class represents a regular comment. It needs at least a text
    field, all other fields are optional (or automatically set by the
    database driver.

    The field `mode` has a special meaning:

    0: normal
    1: in moderation queue
    2: deleted
    """

    protected = ['id', 'mode', 'created', 'modified']
    fields = ['text', 'author', 'email', 'website', 'parent']

    def __init__(self, **kw):

        for field in self.protected + self.fields:
            self.__dict__[field] = kw.get(field)

    def iteritems(self, protected=False):
        for field in self.fields:
            yield field, getattr(self, field)
        if protected:
            for field in self.protected:
                yield field, getattr(self, field)

    @classmethod
    def fromjson(self, data):

        try:
            data = json.loads(data)
        except ValueError:
            abort(400)

        comment = Comment(created=time.time())

        for field in self.fields:
            if field == 'text' and field not in data:
                raise ValueError('Comment needs at least text, but no text was provided.')
            comment.__dict__[field] = data.get(field)

        return comment

    @property
    def json(self):
        return ''

    @property
    def pending(self):
        return self.mode == 1

    @property
    def deleted(self):
        return self.mode == 2


def comment(app, environ, request, path, id=None):
    return Response('', 200)
