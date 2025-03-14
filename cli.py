#!/usr/bin/env python3

from models import Playlist, Song , session

def main_menu() :
    while True :
        print("\n Spotify Playlist Manager")
        print("1. Create your playlist")
        print("2. Add songs to your playlist")
        print("3. View all playlists")
        print("4. Find a playlist")
        print("5. View songs in a playlist")
        print("6. Delete a playlist")
        print("7. Remove a song from a playlist")
        print("8. Find a song")
        print("9. View all songs")
        print("10. EXIT")

        choice = input("Select an option: ")

        if choice == "1" :
            create_playlist()
        elif choice == "2" :
            add_song()
        elif choice == "3" :
            view_all_playlists()
        elif choice == "4":
            search_playlist()
        elif choice == "5":
            view_songs_in_playlists()
        elif choice == "6":
            delete_playlist()  
        elif choice == "7":
            delete_song()
        elif choice == "8":
            search_song()
        elif choice == "9":
            view_all_songs()
        elif choice == "10":
            print("Leaving? So soon? Hope to see you again!")
            break
        else :
            print("Invalid Option. Select a number from 1 to 10")

def create_playlist():
    name = input("Enter playlist name: ")
    playlist = Playlist.create_playlist(name)
    print(f"Playlist {name} has been successfully created. Enjoy the vibes!") 
    

def add_song():
    playlists = Playlist.get_all_playlists()
    if not playlists:
        print("No Playlist Available. Your jams need a home, create a playlist for your songs first")
        return
    print("Available Playlists:")
    for playlist in playlists:
        print(f"Playlist {playlist.id} : {playlist.name}")

    playlist_id = int(input("Enter playlist ID: "))  
    title = input("Enter the song's title: ")
    artist = input("Enter the song's artist: ")
    album = input("Enter the song's album: ")
    
    song = Song.create_song(title, artist, album, playlist_id)
    print(f"{song.title} added to Playlist {song.playlist_id} successfully!")

def view_all_playlists():
    playlists = Playlist.get_all_playlists()
    if not playlists:
        print("No playlist found")
        return
    for playlist in playlists:
        print(playlist)

def search_playlist():
    name = input("Enter playlist name: ")
    results = Playlist.find_by_name(name)
    if results :
        for playlist in results:
            print(playlist)
    else:
        print("No matching playlists found!")

def view_songs_in_playlists():
    playlist_id = int(input("Enter playlist ID: "))
    playlist = session.get(Playlist, playlist_id)
    if playlist :
        songs = playlist.get_songs()
        if songs:
            for song in songs :
                print(song)
        else :
            print("Playlist is empty!")
    else :
            print("Playlist not found.") 

def delete_playlist():
    playlist_id = int(input("Enter playlist ID: "))
    playlist = session.get(Playlist, playlist_id)
    if playlist :
        playlist.delete_playlist()
        print(f"{playlist.name} deleted successfully!")
    else :
        print("Playlist not found")

def delete_song():
    song_id = int(input("Enter song ID: "))
    song = Song.find_by_id(song_id)
    if song :
        song.delete_song()
        print("Song deleted successfully!") 
    else :
        print("Song not found")

def search_song():
    query = input("Enter song title,album or artist to search: ")
    results = Song.search_song(query)
    if results:
        for song in results:
            print(song)
    else :
        print("No match found!")

def view_all_songs():
    songs = Song.get_all_songs()
    if not songs:
        print("No songs found")
        return
    for song in songs:
            print(song)    

if __name__ == "__main__" :
    main_menu()                       









