#!/usr/bin/env python3

import argparse
import json
import sys
import os
from InstagramAPI import InstagramAPI
import numpy as np
import time
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import operator
from tqdm import tqdm
from pprint import pprint



# Secure Secret Key Logic

# JSON-based secrets module
with open("secrets.json") as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    """Get the secret variable or return explicit exception."""
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {0} environment variable".format(setting)
        raise Exception(error_msg)

username = 'j_driscoll98'
pwd = get_secret('password')


def report(args):
    API = InstagramAPI(username, pwd)
    API.login()
    time.sleep(2)
    API.getProfileData()
    API.LastJson.keys()
    pprint(API.LastJson['user'])
    my_id = API.LastJson['user']['pk']
    API.getUsernameInfo(my_id)
    n_media = API.LastJson['user']['media_count']
    media_ids = []
    max_id = ''
    for i in range(int(n_media/18+1)):
        API.getUserFeed(usernameId=my_id, maxid=max_id)
        media_ids += API.LastJson['items']
        if not API.LastJson['more_available']:
            print("no more avaliable")
            break
        max_id = API.LastJson['next_max_id']
        print(i, "   next media id = ", max_id, "  ", len(media_ids))
        time.sleep(3)
    likers = []
    m_id = 0
    print("wait %.1f minutes" % (n_media*2/60.))
    for i in tqdm(range(len(media_ids))):
        m_id = media_ids[i]['id']
        API.getMediaLikers(m_id)
        likers += [API.LastJson]
        time.sleep(2)
    print("done!")
    users = []
    for i in likers:
        users += map(lambda x: i['users'][x]['username'],
                     range(len(i['users'])))
    users_set = set(users)

    print("all users = ", len(users), " uniqum users = ", len(users_set))
    l_dict = {}
    for user in users_set:
        # l_dict structure - {username:number_of_liked_posts}
        l_dict[user] = users.count(user)
    all_pairs = sorted(l_dict.items(), key=operator.itemgetter(1))
    n_users = 10  # top 10 users
    pairs = all_pairs[-n_users:]
    y = list(map(lambda y: pairs[y][1], range(len(pairs))))
    x = list(map(lambda y: pairs[y][0], range(len(pairs))))
    fig = plt.figure()
    plt.xkcd()
    plt.xticks(range(len(pairs)), x, rotation='vertical')
    plt.ylim([80, 160])
    plt.bar(range(len(pairs)), y)
    plt.xlabel('USERS')
    plt.ylabel('number of liked posts')
    plt.show()
    sys.exit()



def main(arguments):
    report(arguments)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
