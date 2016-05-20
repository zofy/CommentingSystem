from django.shortcuts import render

from comments.models import Comment


def home(request):
    context = dict()
    comment_tree = sort_comments2(request, 0)[0]
    context['comment_tree'] = comment_tree[:10]
    return render(request, 'comments/index.html', context)


def sort_comments():
    if not Comment.objects.all():
        return []
    max_depth = Comment.objects.order_by('-depth')[0].depth
    result = Comment.objects.filter(depth=0).order_by('-_lower_bound')
    for i in xrange(1, max_depth + 1):
        # tu spravit dict
        l = Comment.objects.filter(depth=i).order_by('_lower_bound')
        for comment in l:
            path_list = comment.path.split()
            # do dict vkladat do listov commenty
            for idx, c in enumerate(result):
                rc_list = c.path.split()
                if len(rc_list) < i:
                    continue
                if rc_list[i - 1] == path_list[i - 1]:
                    result = result[:idx + 1] + [comment] + result[idx + 1:]
                    break
                    # a tu vlozit do resultu tie listy
    return result


def sort_comments2(request, idx):
    result = Comment.objects.filter(depth=0).order_by('-_lower_bound')
    r = []
    idx = rec(result[idx:], r)
    return r, idx


def rec(list, result):
    if not list:
        return

    for i, c in enumerate(list):
        result.append(c)
        d = c.depth
        path = c.path
        l = Comment.objects.filter(depth=d + 1, path__startswith=path).order_by('-_lower_bound')
        rec(l, result)
        if c.depth == 0 and len(result) >= 10:
            return i
