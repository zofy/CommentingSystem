from django.shortcuts import render

from comments.forms import CommentForm
from comments.models import Comment


def home(request):
    form = CommentForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            temp = form.save(commit=False)
            parent = form['parent'].value()

            if parent == '':
                # Set a blank path then save it to get an ID
                temp.path = []
                temp.save()
                temp.path = str(temp.id)
            else:
                # Get the parent node
                node = Comment.objects.get(id=parent)
                temp.depth = node.depth + 1
                temp.path = node.path

                # Store parents path then apply comment ID
                temp.save()
                temp.path += ' ' + str(temp.id)

            # Final save for parents and children
            temp.save()

    # Retrieve all comments and sort them by path
    # data = serializers.serialize('json', Comment.objects.filter(depth=0).order_by('-_lower_bound'))
    # request.session['result'] = data
    # request.session['r'] = []

    # comment_tree = sort_comments2(request)[:10]

    # return render(request, 'comments/index.html', locals())


def home(request):
    # request.session['result'] = Comment.objects.filter(depth=0).order_by('-_lower_bound')
    # request.session['r'] = []
    context = dict()
    comment_tree = sort_comments2(request, 0)[:10]
    context['comment_tree'] = comment_tree
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


def rec(comment, result, max):
    d = comment.depth
    path = comment.path
    l = Comment.objects.filter(depth=d + 1, path__startswith=path).order_by('-_lower_bound')

    if not l or len(result) >= max:
        return comment

    result.append(comment)

    for c in l:
        com = rec(c, result, max)
        if com:
            result.append(com)
        if len(result) >= max:
            return com


def sort_comments2(request, idx, max):
    result = Comment.objects.filter(depth=0).order_by('-_lower_bound')
    r = []
    for i, c in enumerate(result[idx:idx + 10]):
        rec(c, r, max)
        if len(r) >= max:
            return r, i
    return r
