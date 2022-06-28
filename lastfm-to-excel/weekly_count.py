#!/usr/bin/env python3
"""
Show 20 last played tracks
"""
import argparse
import pylast

from mylast import lastfm_network, lastfm_username, track_and_timestamp

import datetime
from datetime import timezone
from zoneinfo import ZoneInfo
import time

from last_fm_python import print_to_excel

track_count ={}

def get_recent_tracks(username, number, begin, end):   
    recent_tracks = lastfm_network.get_user(username).get_recent_tracks(limit=number,time_from=begin, time_to=end)
    for i, track in enumerate(recent_tracks):
        printable = track_and_timestamp(track)
        print(str(i + 1) + " " + str(printable))
    return recent_tracks

#returns as a named tuple with entries track, album, playback_date, and timestamp
#acess by doing var.album
def get_track_count(username, begin, end):  
    recent_tracks = lastfm_network.get_user(username).get_recent_tracks(limit=500,time_from=begin, time_to=end)
    for i, track in enumerate(recent_tracks):
        #print(str(i + 1) + " " + track.track + " - " + track.playback_date + " - " + track.timestamp)
        
        if track.track in track_count:
            track_count[track.track] = track_count[track.track] + 1
        else:
            track_count[track.track] = 1
        #print(str(track.track) + " - " + str(track_count[track.track]))
    return track_count

#returns a tuple of each track played in a week, but only once
def get_weekly_chart(username, begin, end):
    chart = lastfm_network.get_user(username).get_weekly_track_charts(from_date=begin, to_date=end)
    count = 0
    for i, track in enumerate(chart):
        count = count + 1
        printable = track
        print(str(count) + " " + str(track))
    return printable


if __name__ == "__main__":

    ### creates a starting and ending date in UNIX timestamp integer form
    dt_start = datetime.datetime(2022, 4, 1)
    dt_start.replace(tzinfo=ZoneInfo("US/Central"))    
    timestamp_start = int(time.mktime(dt_start.timetuple()))

    dt_end = datetime.datetime(2022, 4, 29)
    dt_end.replace(tzinfo=ZoneInfo("US/Central"))  
    timestamp_end = int(time.mktime(dt_end.timetuple()))
    ###
    
    parser = argparse.ArgumentParser(
        description="Show 20 last played tracks",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-u", "--username", help="Last.fm username")
    parser.add_argument(
        "-n",
        "--number",
        default=2000,
        type=int,
        help="Number of tracks to show (when no artist given)",
    )
    args = parser.parse_args()

    if not args.username:
        args.username = lastfm_username

    print(args.username + " last played:")

    
    for i in range(29):
        ### creates a starting and ending date in UNIX timestamp integer form
        dt_start = datetime.datetime(2022, 4, i+1)
        dt_start.replace(tzinfo=ZoneInfo("US/Central"))    
        timestamp_start = int(time.mktime(dt_start.timetuple()))
    
        dt_end = datetime.datetime(2022, 4, i+2)
        dt_end.replace(tzinfo=ZoneInfo("US/Central"))  
        timestamp_end = int(time.mktime(dt_end.timetuple()))
        ###
        try:
            #get_recent_tracks(args.username, args.number, timestamp_start, timestamp_end)
            #get_weekly_chart(args.username, timestamp_start, timestamp_end)

            #returns a named tuple of artists and song count
            get_track_count(args.username, timestamp_start, timestamp_end)
            
        except pylast.WSError as e:
            print("Error: " + str(e))


sorted_tracks = {}
sorted_keys = sorted(track_count, key=track_count.get)

for w in sorted_keys:
    sorted_tracks[w] = track_count[w]

j = -1
for key, value in reversed(sorted_tracks.items()):
    j = j + 1
    print_to_excel(j, key, value)
    print(key, ' : ', value)
# End of file
