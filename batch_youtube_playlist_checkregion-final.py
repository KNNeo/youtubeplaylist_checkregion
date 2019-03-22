import urllib.request, json, sys, datetime, time
import numpy as np

API_KEY = "YOUR YOUTUBE API V3 KEY HERE"
non_bmp = dict.fromkeys(range(0x1000,sys.maxunicode+1),0xfffd)
maxResult = 50
playlistId = "PL_jWj0Wl8TG-UlSmo4HG3kDtTJYBO4UgB"
video_list = []

#copy paste url
playlistURL = str(input('Input full YouTube playlist URL here: '))
#input is playlistID only, not full URL

#find list of regions available for YouTube
regions_url = "https://www.googleapis.com/youtube/v3/i18nRegions?part=snippet&key="+API_KEY
#print(regions_url)
regions = {}
with urllib.request.urlopen(regions_url) as url:
    data = json.loads(url.read().decode().translate(non_bmp))
    #print(len(data['items']))
    for i in range(0,len(data['items'])-1):
        regions[data['items'][i]['id']] = data['items'][i]['snippet']['name']
    #print((regions))

#forming query url
playlist_url = "https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&playlistId="+playlistId+"&maxResults="+str(maxResult)+"&key="+API_KEY
#print(playlist_url)
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
            print("Read playlist done.")
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
    #print(query_url)
    with urllib.request.urlopen(query_url) as url:
        data = json.loads(url.read().decode('utf-8'))
        #print(data['items'][0])
        allowed_list = []
        blocked_list = []
        final_list = []
        final_set = set()
        
        try:
            allowed_list = data['items'][0]['contentDetails']['regionRestriction']['allowed']
        except:
            allowed_list = []
        try:
            blocked_list = data['items'][0]['contentDetails']['regionRestriction']['blocked']
        except:
            blocked_list = []

        #case: no lists, region free, ignore
        if blocked_list == [] and allowed_list == []:
            continue
        #case: when blocked list does not exist - take allowed list, check with all, exclude all allowed
        elif blocked_list == []:
            for a in allowed_list:
                for r in regions:
                    if a == r:
                        final_list.append(r) #checking if in official list?
            final_set = set(regions)-set(final_list)
        #case: when allowed list does not exist - copy paste blocked list
        elif allowed_list == []:
            final_set = set(blocked_list)
        #case: when both lists exist - do both, clear duplicates
        else:
            print("Undetermined")
            break

        #print region names instead: limitation - regions not complete set
        #for x in final_set:
        #    try:
        #        final_set.discard(x)
        #        final_set.add(regions[x])
        #    except:
        #        final_set.add(x)
        
        if len(final_set) > 0:
            print("BLOCKED IN: "+str(final_set))
            print("BLOCKED IN "+ str(len(final_set)) +" REGION(S): "+data['items'][0]['snippet']['title'])
            #print(query_url)
            print("*VideoID: "+i+"\n")
            counter+=1
        elif len(allowed_list) > 0:
            print("[Video may still be region locked in certain regions]")
            print("ALLOWED IN "+ str(len(allowed_list)) +" REGION(S): "+data['items'][0]['snippet']['title'])
            #print(query_url)
            print("*VideoID: "+i+"\n")
            counter+=1

print(str(counter)+" may be region locked. Use the videoId provided for details.")
