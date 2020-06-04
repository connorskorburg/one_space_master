from django.shortcuts import render, redirect
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import sys
import requests
import base64
import datetime

# Create your views here.
def index(request):

    return render(request,'home.html')

def sign_in(request):
    client_id = '93d03c51a99146ed992ca0175f68674b'
    client_secret = '92a2119255fb489bbfe6e2a054f8c4b5'
    return redirect(f'https://accounts.spotify.com/authorize?response_type=code&client_id={client_id}&scope=playlist-modify-public&redirect_uri=http://localhost:8000/callback')

def callback(request):
    client_id = '93d03c51a99146ed992ca0175f68674b'
    client_secret = '92a2119255fb489bbfe6e2a054f8c4b5'
    # print("REQUEST",request.GET['code'])
    code = request.GET['code']
    token_url =  'https://accounts.spotify.com/api/token'
    client_creds = f"{client_id}:{client_secret}"
    client_creds_b64 = base64.b64encode(client_creds.encode())
    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        'redirect_uri': 'http://localhost:8000/callback',
    }
    token_headers = {
        "Authorization": f"Basic {client_creds_b64.decode()}"
    }
    r = requests.post(token_url, data=token_data, headers=token_headers)
    # print(r.json())
    # print("TOKEN IS HERE:", r.json()['access_token'])
    valid_request = r.status_code in range(200, 299)
    if valid_request:
        token_response_data = r.json()
        now = datetime.datetime.now()
        access_token = token_response_data['access_token']
        request.session['access_token'] = access_token
        expires_in = token_response_data['expires_in']
        request.session['expires_in'] = expires_in
        expires = now + datetime.timedelta(seconds=expires_in)
        did_expire = expires < now
        print('successfully signed in')
    return redirect('/')


def genre_result(request):

    cid = '507b63501e804f87bd8538c0c6f395ed'
    secret = 'b14546bedc8844c8be95486386500f50'
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager,requests_timeout=100)

    results = sp.categories(country='US', limit=50, offset=0)
    genre_mood_list=[]

    for i in results['categories']['items']:
        genre_mood_list.append(
            {
                "category_link" : i['href'],
                "category_name" : i['name'],
                "category_image" : i['icons'][0]['url']
            }
        )
    request.session['category_list'] = genre_mood_list

    return redirect('/genremoods')

def genremoods(request):

    genre_list = request.session['category_list']

    context = {
        "genre_list" : genre_list
    }
    return render(request, 'genreandmood.html',context)

def new_playlist(request):
    return render(request, 'new_playlist.html')

def get_playlists(request):
    if 'access_token' in request.session:
        token = request.session['access_token']
        sp = spotipy.Spotify(auth=token)
        username = sp.current_user()['id']
        playlists = sp.user_playlists(username)
        playlists_list = []
        for i in playlists['items']:
            playlists_list.append(
                {
                    'name': i['name'],
                    'description': i['description'],
                    'playlist_id': i['id'],
                }
            )
        context = {
            'playlists_list': playlists_list
        }
        return render(request, 'playlists.html', context)

    else:
        return redirect('/')

def create_playlist(request):
    if 'access_token' in request.session:
        title = request.POST['playlist_title']
        desc = request.POST['playlist_desc']
        token = request.session['access_token']
        sp = spotipy.Spotify(auth=token)
        username = sp.current_user()['id']
        sp.user_playlist_create(user=username, name=title, public=True, description=desc)
        return redirect('/get_playlists')
    else:
        return redirect('/')

def add_song_to_playlist(request, track_id):
    if 'access_token' in request.session:
        token = request.session['access_token']
        sp = spotipy.Spotify(auth=token)
        username = sp.current_user()['id']
        playlists = sp.user_playlists(username)
        playlists_list = []
        for i in playlists['items']:
            playlists_list.append(
                {
                    'name': i['name'],
                    'description': i['description'],
                    'playlist_id': i['id'],
                }
            )
        context = {
            'track_id': track_id,
            'playlists_list': playlists_list,
        }
        return render(request, 'add_song.html', context)
    else:
        return redirect('/')

def new_song_in_playlist(request):
    # print(request.POST)
    if 'access_token' in request.session:
        track_id = request.POST['track_id']
        track_list = [track_id]
        playlist_id = request.POST['playlist_id']
        token = request.session['access_token']
        sp = spotipy.Spotify(auth=token)
        username = sp.current_user()['id']
        sp.user_playlist_add_tracks(user=username, playlist_id=playlist_id, tracks=track_list)
        return redirect('/get_playlists')
    else:
        return redirect('/')


def new_releases(request):
    cid = 'fcabf1c8ee3d4bbc81275366fd4bfacf'
    secret = '39c9ebdb80bb41d89de106bb59e4e205'
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    results = sp.new_releases(country=None, limit=20, offset=0)
    new_realeases_list = []
    for i in results['albums']['items']:
        new_realeases_list.append(
            {
                "artist": i['artists'][0]['name'],
                "album_id": i['id'],
                "album": i['name'],
                "image_url": i['images'][0]['url'],
            }
        )
    context = {
        'new_releases_list': new_realeases_list
    }
    return render(request, 'new_releases.html', context)


def newreleases (request):
    return render(request,'newreleases.html')

def charts(request):

    return render(request,'charts.html')

def concerts(request):

    return render(request,'concerts.html')


def track_results(request):
    track_info_length = len(request.session['track_info_list'])
    context = {
        'track_info_list': request.session['track_info_list'],
        'track_searched': request.session['track_searched'],
        'track_info_length': track_info_length,
    }
    return render(request, 'track_results.html', context)

def search_track(request):
    track = request.POST['track']
    if track == '':
        return redirect('/')
    cid = '93d03c51a99146ed992ca0175f68674b'
    secret = '92a2119255fb489bbfe6e2a054f8c4b5'
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    track_results = sp.search(q=track, type='track', limit=15)
    track_info_list = []
    for i in track_results['tracks']['items']:
        track_info_list.append(
            {
                'image': i['album']['images'][0]['url'],
                'artist': i['artists'][0]['name'],
                'track': i['name'],
                'track_id': i['id'],
                'explicit': i['explicit'],
            }
        )
    # print("TRACK INFO", track_info_list)
    request.session['track_info_list'] = track_info_list
    request.session['track_searched'] = track

    return redirect('/track_results')
