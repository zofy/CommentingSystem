from random import randint, random, choice

from django.test import TestCase

from comments.models import Comment
from comments.views import sort_comments, sort_comments2


class CommentTestCase(TestCase):
    def create_comment(self):
        return Comment.objects.create(path=self.id())

    def test_generate_comments(self):
        c = Comment(path='0', depth=0, _lower_bound=0)
        c.save()
        result = [c]
        for i in xrange(1, 10000):
            idx = randint(0, len(result))
            lb = round(random(), 2)
            if idx > len(result) - 1:
                c = Comment(depth=0, _lower_bound=lb)
                c.path = str(i)
                c.save()
            else:
                c = Comment(_lower_bound=lb)
                c.path = result[idx].path + ' ' + str(i)
                c.depth = result[idx].depth + 1
                c.save()
            result.append(c)
            # return result
            # self.assertEqual(len(result), 11)

    def test_sort_comments(self):
        self.test_generate_comments()
        l = sort_comments2(0, 0)
        idx = l[1]
        print idx
        print len(l[0])
        for c in l[0][:10]:
            print c
        # m = sort_comments2(0, idx + 1)
        # print len(m[0])
        # for c in m[0]:
        #     print c
        # print l[1]
        # print(l[1])
