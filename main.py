# encoding: utf-8

import sys
from workflow import Workflow
import requests

API_KEY = 'your-pinboard-api-key'


def get_icons(posts):
    for post in posts:
        avatar = post['member']['avatar_normal']

        path = get_path(post)

        import os
        try_mkdir(os.path.dirname(path))
        try:
            os.stat(path)
            continue
        except:
            open(path, 'w').write(requests.get('http:' + avatar).content)


def try_mkdir(path):
    paths = [path]
    import os
    for i in range(3):
        paths += [os.path.dirname(path)]
        path = os.path.dirname(path)

    paths.sort()
    for path in paths:
        try:
            os.mkdir(path)
        except:
            pass


def get_path(post):
    member_id = post['member']['id']
    member_id = str(member_id)
    return '/tmp/alfred-cache/' + member_id[:2] + '/' + member_id + '.png'


def main(wf):
    if wf.args[0] == 'hot':

        url = 'https://www.v2ex.com/api/topics/hot.json'
        posts = requests.get(url).json()

        get_icons(posts)
        for post in posts:
            wf.add_item(title=post['title'],
                        subtitle=post['url'],
                        icon=get_path(post),
                        arg=post['url'],
                        valid=True,
                        )
    else:
        args = " ".join(wf.args)
        wf.add_item(title='input <hot>'
                    , subtitle='not valid input:' + args)

    # Send the results to Alfred as XML
    wf.send_feedback()


if __name__ == u"__main__":
    wf = Workflow()

    sys.exit(wf.run(main))
