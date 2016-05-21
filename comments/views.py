import json
import pickle

import simplejson
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from comments.models import Comment


def home(request):
    context = dict()
    request.session['idx'] = 0
    comment_tree, new_idx = sort_comments2(request)
    context['comment_tree'] = comment_tree[:5]
    # request.session['result'] = serializers.serialize('json', comment_tree,
    #                                                   fields=('path', 'depth', 'content', 'visible'))
    request.session['result'] = pickle.dumps(comment_tree)
    request.session['idx'] = new_idx
    request.session['page'] = 0
    return render(request, 'comments/index.html', context)


def list_comments(request):
    context = dict()
    data = pickle.loads(request.session['result']) + ['gugug']
    # context['comments'] = [(d.path, d.depth) for d in data]
    context['comments'] = [data[-1]]

    if request.method == 'GET':
        data = pickle.loads(request.session['result'])[:2]
        context['comments'] = [(d.path, d.depth) for d in data]
        return JsonResponse(context)

    if request.POST['move'] == 'next':
        request.session['page'] += 1
        page = request.session['page']
        if len(request.session['result']) < page * 5 + 5:
            request.session['idx'] += 1
            new_comments, new_idx = sort_comments2(request)
            request.session['result'] += new_comments
            request.session['idx'] = new_idx
    elif request.POST['move'] == 'previous':
        request.session['page'] -= 1
        page = request.session['page']
        # return JsonResponse({'comments': request.session['result'][page*5: page*5 + 5]})
        context['comments'] = simplejson.loads(request.session['result'])[page * 5: page * 5 + 5]
    return JsonResponse(context)


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


def sort_comments2(request):
    idx = request.session['idx']
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
        if c.depth == 0 and len(result) >= 5:
            return i
