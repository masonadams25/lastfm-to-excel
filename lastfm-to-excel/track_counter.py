import argparse
import pylast

from mylast import lastfm_network, lastfm_username, track_and_timestamp

import datetime
from datetime import timezone, date
from zoneinfo import ZoneInfo
import time

from write_to_excel import print_to_excel

track_count ={}
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

def track_counter(start_year, start_mon, start_day, end_year, end_mon, end_day):
    
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

        #create start and end dates, and date range
        start = datetime.datetime(start_year, start_mon,start_day)
        end = datetime.datetime(end_year, end_mon, end_day)
        date_range = int( str( (end - start))[:2] )
        dt_start = datetime.datetime(start_year, start_mon, start_day)

        for i in range(date_range):

            ### creates a starting and ending date in UNIX timestamp integer form
            if(i > 0):
                dt_start = dt_start + datetime.timedelta(days=1)
            dt_start.replace(tzinfo=ZoneInfo("US/Central"))    
            timestamp_start = int(time.mktime(dt_start.timetuple()))
        
            #dt_end = datetime.datetime(2022, 4, i+2)
            dt_end = dt_start + datetime.timedelta(days=1)
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

        #sorts by number of songs
        sorted_tracks = {}
        sorted_keys = sorted(track_count, key=track_count.get)

        for w in sorted_keys:
            sorted_tracks[w] = track_count[w]

        #prints out pairs of song and count
        k = 0
        for key, value in reversed(sorted_tracks.items()):
            k = k+1
            #print(key, ' : ', value)
            print_to_excel(k,key,value)