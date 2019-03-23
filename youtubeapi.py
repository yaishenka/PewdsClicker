import requests
response = requests.get('https://www.googleapis.com/youtube/v3/channels', params={'part':'statistics', 'id':'UC-lHJZR3Gqxm24_Vd_AJ5Yw', 'key':'AIzaSyAdBSlGXv0RPGPeTY-kvSgahamGE5zyW8g'})
print(response.json().get('items')[0].get('statistics').get('subscriberCount'))