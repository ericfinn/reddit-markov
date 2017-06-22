import urllib.request
import json
import traceback

def get_all_posts(user):
    count = 0;
    result = [];

    print('Requesting iteration %d' % count);
    response = get_posts(user);
    result = result + response['posts'];
    count+=1;

    while(response['next']):
        print('Requesting iteration %d, next value %s' % (count, response['next']));
        response = get_posts(user, response['next']);
        result = result + response['posts'];
        count+=1;
    
    print('Got %d results' % len(result));
    return result;

def get_posts(user, after=''):
    try:
        request = urllib.request.Request('https://www.reddit.com/user/%s/comments/.json?limit=100&after=%s' % (user, after));
        request.add_header('User-Agent', 'chalcedon-data-gatherer');
        raw = urllib.request.urlopen(request).read().decode('utf-8');
        response = json.loads(raw)['data'];
        return { 'posts': streamline_posts(response['children']), 'next': response['after'] };
    except:
        traceback.print_exc();

def streamline_posts(posts):
    return [ { 'text': post['data']['body'], 'timestamp': post['data']['created'] } for post in posts ];

