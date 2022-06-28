import pylast
import subprocess

API_KEY = "9a2db7f32f13e05f0a1e3e60b3b0afad"
API_SECRET = "a19cef4f9ebbdd80bd33860ef2324719"

username = "Masonrules9"
password_hash = pylast.md5("Masonadams9!")

network = pylast.LastFMNetwork(
    api_key=API_KEY,
    api_secret=API_SECRET,
    username=username,
    password_hash=password_hash,
)

result = subprocess.run(['python3', 'nowplaying.py'], stdout=subprocess.PIPE)
result.stdout

