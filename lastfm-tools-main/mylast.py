import os
import sys

import pylast

# You have to have your own unique two values for API_KEY and API_SECRET
# Obtain yours from https://www.last.fm/api/account for Last.fm

try:
    API_KEY = os.environ["LASTFM_API_KEY"]
    API_SECRET = os.environ["LASTFM_API_SECRET"]
except KeyError:
    API_KEY = "9a2db7f32f13e05f0a1e3e60b3b0afad"
    API_SECRET = "a19cef4f9ebbdd80bd33860ef2324719"

try:
    lastfm_username = os.environ["LASTFM_USERNAME"]
    lastfm_password_hash = os.environ["LASTFM_PASSWORD_HASH"]
except KeyError:
    # In order to perform a write operation you need to authenticate yourself
    lastfm_username = "Masonrules9"
    # You can use either use the password, or find the hash once and use that
    lastfm_password_hash = pylast.md5("Masonadams9!")
    print(lastfm_password_hash)
    # lastfm_password_hash = "my_password_hash"


lastfm_network = pylast.LastFMNetwork(
    api_key=API_KEY,
    api_secret=API_SECRET,
    username=lastfm_username,
    password_hash=lastfm_password_hash,
)


def track_and_timestamp(track):
    return f"{track.playback_date}\t{track.track}"


def print_track(track):
    print(track_and_timestamp(track))


TRACK_SEPARATOR = " - "


def split_artist_track(artist_track):
    artist_track = artist_track.replace(" – ", " - ")
    artist_track = artist_track.replace("“", '"')
    artist_track = artist_track.replace("”", '"')

    (artist, track) = artist_track.split(TRACK_SEPARATOR)
    artist = artist.strip()
    track = track.strip()
    print("Artist:\t\t'" + artist + "'")
    print("Track:\t\t'" + track + "'")

    # Validate
    if len(artist) == 0 and len(track) == 0:
        sys.exit("Error: Artist and track are blank")
    if len(artist) == 0:
        sys.exit("Error: Artist is blank")
    if len(track) == 0:
        sys.exit("Error: Track is blank")

    return (artist, track)


# End of file
