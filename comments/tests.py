from random import randint, random

from django.test import TestCase

from comments.models import Comment
from comments.views import sort_comments2


class CommentTestCase(TestCase):
    def create_comment(self):
        return Comment.objects.create(path=self.id())

    def test_generate_comments(self):
        c = Comment(depth=0, _lower_bound=0)
        c.path = '0'
        c.save()
        result = [c]
        for i in xrange(1, 1000):
            ch = randint(0, 1)
            lb = round(random(), 2)
            c = Comment(_lower_bound=lb, visible=random() > 0.2)
            if ch > 0.35:
                idx = randint(0, len(result) - 1)
                c.path = result[idx].path + ' ' + str(i)
                c.depth = result[idx].depth + 1
                c.parent = result[idx].id
                c.save()
            else:
                c.depth = 0
                c.path = str(i)
                c.save()
            result.append(c)
            # return result
            # self.assertEqual(len(result), 11)

    def test_sort_comments(self):
        self.test_generate_comments()
        l = sort_comments2(0, 20)
        print len(l)
        for c in l[:10]:
            print c
