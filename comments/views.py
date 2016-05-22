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
    pass


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

        context['comments'] = [(c.path, c.lower_bound, c.depth, c.visible, c.content, c.date, c.id) for c in
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
