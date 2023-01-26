import spotipy
import confidential
import logging
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope='playlist-modify-public', client_id=confidential.client_id, client_secret=confidential.client_secret, redirect_uri=confidential.redirect))

async def AddPlaylist(song):
    sp.playlist_add_items('https://open.spotify.com/playlist/667KuHtbjh3no4HSuQXaGp?si=1ab7fd487c834ae2', items = [song])
