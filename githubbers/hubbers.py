#!/usr/bin/env python

import httplib2
import yaml

__all__ = ['GitHubber', 'get_hubbers', 'GitHubberError']

_DEFAULT_ATTRS = ['type', 'location', 'blog', 'gravatar_id', 'company', 
        'login', 'contributions', 'name', 'email']

class GitHubber(object):
    def __init__(self, hubber, repo_uri=None):
        for k in _DEFAULT_ATTRS:
            setattr(self, k, None)
        for k,v in hubber.iteritems():
            if k and k[0] == ':':
                k = k[1:]
            if k:
                setattr(self, k, v)
        if self.login:
            self.github_uri = 'http://github.com/' + self.login
            if repo_uri:
                self.commits_uri = '%s/commits/master?author=%s' % (repo_uri, self.login)
            else:
                repo_uri = None
        else:
            self.github_uri = None

    def gravatar_uri(self, default='mm', size=80, rating='g'):
        if not self.gravatar_id:
            return None

        uri = 'http://gravatar.com/avatar/' + self.gravatar_id
        if default or size or rating:
            uri += '?'
            if default:
                uri += 'd=' + default + '&'
            if size:
                uri += 's=' + str(size) + '&'
            if rating:
                uri += 'r=' + rating
        return uri

def get_hubbers(user, repo):
    uri = 'http://github.com/api/v2/yaml/repos/show/%s/%s/contributors' % (user, repo)

    http = httplib2.Http()
    response, body = http.request(uri)
    if response.status != 200:
        if body:
            try:
                yaml.load(body)
                raise GitHubberError('Github error response: ' + body['error'])
            except:
                pass
        raise GitHubberError('Failed to query contributors from github')
    try:
        hubbers = yaml.load(body)
    except:
        raise GitHubberError('Failed to parse github response: \'%s\'' % body)

    repo_uri = 'http://github.com/%s/%s' % (user, repo)
    
    return [GitHubber(h, repo_uri) for h in hubbers['contributors']]


class GitHubberError(Exception):
    pass
