import requests

def search_track(query):
    url = f'https://api.deezer.com/search?q={query}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        tracks = data['data']

        if tracks:
            for track in tracks[:5]:
                print(f"Track: {track['title']}\nArtist: {track['artist']['name']}\nAlbum: {track['album']['title']}\nURL: {track['link']}\n")
        else:
            print("No tracks found.")
    else:
        print(f"Error: Unable to fetch track data. (Status code: {response.status_code})")

if __name__ == '__main__':
    query = input("Enter a track or artist name: ")
    search_track(query)

