import os
from random import randint, random

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CommentingSystem.settings")
django.setup()

from comments.models import Comment

NUMBER_OF_COMMENTS = 1000

CONTENT = ['Hi all!', 'Lorem ipsum', 'Bug', 'Thanks a lot!']


def generate_comments(n=NUMBER_OF_COMMENTS):
    c = Comment(content=CONTENT[0])
    c.save()
    c.path = str(c.id)
    c.save()
    result = [c]
    for i in xrange(1, n):
        #  choice - decides whether to add new comment with depth = 0 or reply to another comment
        choice = randint(0, 1)
        content_choice = randint(0, len(CONTENT) - 1)
        lb = round(random(), 2)
        #  some of the comments should be hidden
        c = Comment(_lower_bound=lb, visible=random() > 0.2, content=CONTENT[content_choice])
        if choice == 0:
            idx = randint(0, len(result) - 1)
            c.depth = result[idx].depth + 1
            c.parent = result[idx].id
            c.save()
            c.path = result[idx].path + ' ' + str(c.id)
            c.save()
        else:
            c.depth = 0
            c.save()
            c.path = str(c.id)
            c.save()
        result.append(c)


generate_comments()
