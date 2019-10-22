import os.path
import sys
import re

from mastodon import Mastodon
import requests

if len(sys.argv) < 4:
    print("Usage: python3 toot_spam.py mastodon_login mastodon_passwd mastodon_instance text [pic_url]")  # noqa
    sys.exit(1)

pic = None
if len(sys.argv) > 4:
    pic = sys.argv[5]

mastodon = sys.argv[1]
passwd = sys.argv[2]
instance = sys.argv[3]
text = sys.argv[4]

mastodon_api = None

if mastodon_api is None:
    # Create application if it does not exist
    if not os.path.isfile(instance+'.secret'):
        if Mastodon.create_app('toot_spam', api_base_url='https://'+instance, to_file=instance+'.secret'):
            print('toot_spam app created on instance '+instance)
        else:
            print('failed to create app on instance '+instance)
            sys.exit(1)

    try:
        mastodon_api = Mastodon(client_id=instance+'.secret', api_base_url='https://'+instance)
        mastodon_api.log_in(username=mastodon, password=passwd, scopes=['read', 'write'], to_file=mastodon+".secret")
    except:
        print("ERROR: First Login Failed!")
        sys.exit(1)

    toot_media = []
    # get the pictures...
    if pic is not None:
        media = requests.get(pic)
        media_posted = mastodon_api.media_post(media.content, mime_type=media.headers.get('content-type'))
        toot_media.append(media_posted['id'])

    if toot_media is not None:
        toot = mastodon_api.status_post(text, in_reply_to_id=None, media_ids=toot_media, sensitive=False, visibility='unlisted', spoiler_text=None)
