# -*- coding: utf-8 -*-
import os
import numpy as np
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.errors import HttpError
import pandas as pd
import json
import socket
import socks
import requests

##headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}
##socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 1080)
##socket.socket = socks.socksocket

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"
    # Get credentials and create an API client
    #flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
    #credentials = flow.run_console()
    DEVELOPER_KEY = "AIzaSyCd1-vpcxnEAZiuQSg53-zaaobhZ785W1c"
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=DEVELOPER_KEY)
    #youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)
    videoId = 'A7vcLYIxJvk'
    request = youtube.commentThreads().list(
        part="snippet,replies",
        videoId=videoId,
        maxResults = 100
    )
    response = request.execute()
    #print(response)

    #totalResults = 0
    totalResults = int(response['pageInfo']['totalResults'])

    count = 0
    nextPageToken = ''
    comments = []
    first = True
    further = True
    while further:
        halt = False
        if first == False:
            print('..')
            try:
                response = youtube.commentThreads().list(
                    part="snippet,replies",
                    videoId=videoId,
                    maxResults = 100,
                    textFormat='plainText',
                    pageToken=nextPageToken
                            ).execute()
                totalResults = int(response['pageInfo']['totalResults'])
            except HttpError as e:
                print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
                halt = True

        if halt == False:
            count += totalResults
            for item in response["items"]:
                #VideoDislikeCount = item["snippet"]["text"]
                #VideoLikeCount = item["snippet"]['likeCount']
                comment = item["snippet"]["topLevelComment"]
                #author = comment["snippet"]["authorDisplayName"]
                text = comment["snippet"]["textDisplay"]
                #likeCount = comment["snippet"]['likeCount']
                #publishtime = comment['snippet']['publishedAt']
                #comments.append([author, publishtime, likeCount, text])
                comments.append([text])
            if totalResults < 100:
                further = False
                first = False
            else:
                further = True
                first = False
                try:
                    nextPageToken = response["nextPageToken"]
                except KeyError as e:
                    print("An KeyError error occurred: %s" % (e))
                    further = False
    print('get data count: ', str(count))

    ### write to csv file
    data = np.array(comments)
    df = pd.DataFrame(data, columns=['comment'])
    df.to_csv('She Escaped North Korea to Live in South Korea.csv', index=0, encoding='utf-16')

    result = []
    for comment in comments:
        temp = {}
        temp['comment'] = comment
        result.append(temp)
    print('result: ', len(result))

    json_str = json.dumps(result, indent=4)
    with open('She Escaped North Korea to Live in South Korea.json', 'w', encoding='utf-8') as f:
        f.write(json_str)
    f.close()

if __name__ == "__main__":
    main()

