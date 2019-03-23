import requests


def get_pewds_subs_count():
    try:
        response = requests.get('https://www.googleapis.com/youtube/v3/channels',
                                params={'part': 'statistics', 'id': 'UC-lHJZR3Gqxm24_Vd_AJ5Yw',
                                        'key': 'AIzaSyDOi4pJwTjAQw4xQ3G0CAH_zpht6-ajVkQ'})
        subs = int(response.json().get('items')[0].get('statistics').get('subscriberCount'))
    except:
        subs = 0
    finally:
        return subs


def get_tseries_subs_count():
    try:
        response = requests.get('https://www.googleapis.com/youtube/v3/channels',
                                params={'part': 'statistics', 'id': 'UCq-Fj5jknLsUf-MWSy4_brA',
                                        'key': 'AIzaSyDOi4pJwTjAQw4xQ3G0CAH_zpht6-ajVkQ'})
        subs = int(response.json().get('items')[0].get('statistics').get('subscriberCount'))
    except:
        subs = 0
    finally:
        return subs
