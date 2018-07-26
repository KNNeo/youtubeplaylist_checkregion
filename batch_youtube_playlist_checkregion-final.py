import urllib.request, json, sys, datetime, time
import numpy as np

API_KEY = "INSERT API KEY HERE (YOUTUBE APIv3)"
non_bmp = dict.fromkeys(range(0x1000,sys.maxunicode+1),0xfffd)
maxResult = 50
playlistId = "PL_jWj0Wl8TG-UlSmo4HG3kDtTJYBO4UgB"
video_list = []

#copy paste url
playlistURL = str(input('Input YouTube playlist URL here: '))
#input is "https://www.youtube.com/playlist?list="
playlistId = playlistURL[playlistURL.find('list=')+5:]

#forming query url
playlist_url = "https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&playlistId="+playlistId+"&maxResults="+str(maxResult)+"&key="+API_KEY

#get playlist items ie. video id
with urllib.request.urlopen(playlist_url) as url:
    data = json.loads(url.read().decode().translate(non_bmp))
    totalResults = data['pageInfo']['totalResults']
    #print(totalResults)
    try:
        pageToken = data['nextPageToken']
        #print(data['items'][0])
        for i in range(0,50):
            #print(i)
            latestVideo = data['items'][i]['contentDetails']['videoId']
            video_list.append(latestVideo)
        totalResults -= 50
        #print(totalResults)
    except:
        pageToken = 1
    #print(len(video_list))
#now has total results = 303

while pageToken != 1:
    playlist_url = "https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&playlistId="+playlistId+"&pageToken="+pageToken+"&maxResults="+str(maxResult)+"&key="+API_KEY
    #print(playlist_url)
    with urllib.request.urlopen(playlist_url) as url:
        data = json.loads(url.read().decode().translate(non_bmp))
        try:
            pageToken = data['nextPageToken']
        except:
            pageToken = 1
            
        #print(data['items'][0])
        try:
            for i in range(0,50):
                #print(i)
                latestVideo = data['items'][i]['contentDetails']['videoId']
                video_list.append(latestVideo)
        except:
            print("Done.")
            totalResults -= 50
            #print(totalResults)
        #print(len(video_list))


#print(video_list)
print("Videos found: "+str(len(video_list)))
#create list of video id to loop on
#this can be done for full video_list of ids
counter = 0
for i in video_list:
    query_url = "https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails&id=" + i + "&key=" + API_KEY

    with urllib.request.urlopen(query_url) as url:
        data = json.loads(url.read().decode().translate(non_bmp))
        #print(data['items'][0])
        try:
            allowed_r = len(data['items'][0]['contentDetails']['regionRestriction']['allowed'])
            #print("a: "+str(allowed_r))
        except:
            allowed_r = 0
            
        try:
            blocked_r = len(data['items'][0]['contentDetails']['regionRestriction']['blocked'])
            #print("b: "+str(blocked_r))
        except:
            blocked_r = 0
            
        #if regions == 0:
        #    print("[REGION FREE] "+data['items'][0]['snippet']['title'])
        #else:
        #    print(query_url)
        #    print("***REGION LOCKED***\n\t"+data['items'][0]['snippet']['title'])
        if allowed_r > 0 or blocked_r > 0:
            print("***REGION LOCKED***\n\t"+data['items'][0]['snippet']['title'])
            #print(query_url)
            print(i+"\n")
            counter+=1

print(str(counter)+" may be region locked. Use the videoId provided for details.")
