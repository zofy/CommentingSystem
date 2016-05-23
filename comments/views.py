from random import randint, random

from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render

from comments.models import Comment

COMMENTS_PER_PAGE = 5


def home(request):
    context = dict()
    request.session['page'] = 1
    comment_tree = sort_comments2(request)
    context['comment_tree'] = comment_tree[:5]
    request.session.set_expiry(0)
    return render(request, 'comments/index.html', context)


def vote(request):
    if request.method == 'POST':
        id, vote = request.POST['id'], request.POST['vote']
        c = Comment.objects.get(pk=id)
        if vote == 'plus':
            c.up_votes += 1
        elif vote == 'minus':
            c.down_votes += 1
        c.set_lower_bound()


def list_comments(request):
    context = dict()

    if request.method == 'GET':
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        if request.POST['move'] == 'next':
            request.session['page'] += 1

        elif request.POST['move'] == 'previous':
            if request.session['page'] > 1:
                request.session['page'] -= 1

        page = request.session['page']
        comment_list = sort_comments2(request)
        if not comment_list[(page - 1) * 5: page * 5]:
            request.session['page'] -= 1
            page -= 1

        context['comments'] = [(c.path, c.lower_bound, c.depth, c.visible, c.content, c.date, c.id, str(c.visible)) for
                               c in
                               comment_list[(page - 1) * 5: page * 5]]
    return JsonResponse(context)


def sort_comments2(request):
    page = request.session['page']
    result = Comment.objects.filter(depth=0).order_by('-_lower_bound')
    r = []
    rec(result, r, page)
    return r


def rec(list, result, page):
    if not list:
        return

    for i, c in enumerate(list):
        result.append(c)
        d = c.depth
        l = Comment.objects.filter(depth=d + 1, parent=c.id).order_by('-_lower_bound')
        rec(l, result, page)
        if c.depth == 0 and len(result) >= page * 5:
            return


def generate_comments(n=1000):
    c = Comment()
    c.save()
    c.path = str(c.id)
    c.save()
    result = [c]
    for i in xrange(1, n):
        #  choice - decides whether to add new comment with depth = 0 or reply to another comment
        choice = randint(0, 1)
        lb = round(random(), 2)
        #  some of the comments should be hidden
        c = Comment(_lower_bound=lb, visible=random() > 0.2)
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
