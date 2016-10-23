# encoding: utf-8

import sys
from workflow import Workflow
import requests

API_KEY = 'your-pinboard-api-key'


def main(wf):
    url = 'https://www.v2ex.com/api/topics/hot.json'

    posts = requests.get(url).json()
    for post in posts:
        wf.add_item(title=post['title'],
                    subtitle=post['url'],
                    icon='http:' + post['member']['avatar_normal'],
                    arg=post['url'],
                    valid=True,
                    )

    # Send the results to Alfred as XML
    wf.send_feedback()


if __name__ == u"__main__":
    wf = Workflow()
    sys.exit(wf.run(main))
