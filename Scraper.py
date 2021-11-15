import RbxAPI
import requests

id_range = range(100012094, 200000000) #You can change the Universe ID Range from here. "range(start, end)"
cookie = 'ROBLOX Cookie Here'
headers = requests.utils.default_headers()
headers.update(
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
    }
)


def chunker(seq, size):
    return [seq[pos:pos + size] for pos in range(0, len(seq), size)]


def get_batch_universeID(ids):
    universeIDs = []
    chunks = chunker(ids, 50)
    with RbxAPI.api.BaseAuth(cookie) as auth:
        for batch in chunks:
            univURI = 'https://games.roblox.com/v1/games/multiget-place-details?placeIds=' + \
                '&placeIds='.join(batch)
            try:
                resp = auth.get(univURI, headers=headers).json()
                universeIDs.extend([data['universeId'] for data in resp])
                if len(universeIDs) >= 200:
                    yield universeIDs
                    universeIDs = []
            except (ConnectionError) as e:
                print(f"ERROR: " + e)

    yield universeIDs


def get_batch_details(universeIDs):
    results = []
    chunks = chunker(universeIDs, 100)
    with RbxAPI.api.BaseAuth(cookie) as auth:
        for batch in chunks:
            univURI = 'https://games.roblox.com/v1/games?universeIds=' + \
                ','.join(batch)
            try:
                resp = auth.get(univURI, headers=headers).json()['data']
                results.extend([data for data in resp])
            except (UnicodeEncodeError, KeyError, UnboundLocalError) as e:
                pass

    return results


for batch in get_batch_universeID(list(map(str, id_range))):
    for game in get_batch_details(list(map(str, batch))):
        file1 = open("GamesWithCopyingEnabled.txt", "a+")
        print(f'Game Name: {game["name"]}')
        print(f'Visits: {game["visits"]}')
        print(f'Game ID: {game["id"]}')
        print(f'Copying Enabled: {game["copyingAllowed"]}')
        print('-------------------------')
        try:
            if game["copyingAllowed"] == True and game["visits"] >= 10:
                file1.write(
                    f'\n\n\n[----------({game["rootPlaceId"]})----------]\nGame Name: {game["name"]}\nVisits: {game["visits"]}\nCreated: {game["created"]}\nUpdated: {game["updated"]}\n[--------------------------]')
        except (UnicodeEncodeError, KeyError) as e:
            pass
