from boxsdk import Client, OAuth2
from flask import flash
from threedeposit.database import db_session, Config
import json
import sys

# with open('threedeposit/admin/box/box_cfg.json') as f:
#     data = json.load(f)

# CLIENT_ID = data['client_id']
# CLIENT_SECRET = data['client_secret']

# save token to a file
def save_tokens(access_token, refresh_token):
    # with open('threedeposit/admin/box/box_tokens.json', 'w') as f:
    #     tokens = {}
    #     tokens['access_token'] = access_token
    #     tokens['refresh_token'] = refresh_token
    #     json.dump(tokens, f)
    at = Config.query.filter_by(key='boxaccesstoken')
    rt = Config.query.filter_by(key='boxrefreshtoken')
    at = access_token
    rt = refresh_token
    db_session.commit()



# reads tokens
def read_tokens():
#     try:
#         with open('threedeposit/admin/box/box_tokens.json', 'r') as f:
#             data = json.load(f)
#         return data
#     except Exception as e:
#         print("Read token error: {}".format(e) + sys.exc_info())
#         return "null", "null"
    data = {}
    try:
        data['access_token'] = Config.query.filter_by(key='boxaccesstoken').value(Config.value)
        data['refresh_token'] = Config.query.filter_by(key='boxrefreshtoken').value(Config.value)
    except Exception as e:
        print("Read token error: {}".format(e))
    return data


def push_to_box(folderid, file_path):
    CLIENT_ID = Config.query.filter_by(key='boxclientid').value(Config.value)
    CLIENT_SECRET = Config.query.filter_by(key='boxclientsecret').value(Config.value)

    oauth = OAuth2(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        store_tokens=save_tokens
    )
    tokens = read_tokens()
    at = tokens['access_token']
    rt = tokens['refresh_token']
    oauth._access_token = at
    oauth._refresh_token = rt
    client = Client(oauth)
    archive = client.folder(folder_id=folderid)
    try:
        upload_file = archive.upload(file_path)
        try:
            file_url = upload_file.get_shared_link_download_url(access='open')
            return file_url
        except Exception as e:
            flash('Error getting shared link from Box: '.format(Exception),
                  category='danger')
            return False
    except Exception as e:
        flash('Error uploading to Box: '.format(Exception), category='danger')
        return False
