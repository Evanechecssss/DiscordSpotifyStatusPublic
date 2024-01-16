import asyncio
import json
import time

import dispatcher
import lyrics_handler
import tracks_methods
import exceptions

DISCORD_SYNC_DELAY = 3
DATA = dict()
TRACKS = dict()


async def main():
    allow_sync = True
    tracks_data = {k: v for k, v in TRACKS.items()}
    last_sync_time = 0
    a_ = await dispatcher.get_access_token(DATA['sp_dc'])
    access_token = a_['token']
    client_token = await dispatcher.get_client_token(a_['id'])
    old_url = None
    previous_id = -1
    waiting_for_id = -1
    lyrics = None
    while True:
        if allow_sync:
            song = None
            try:
                song = await dispatcher.get_current_playing_track(access_token)
            except (ConnectionError, exceptions.AccessTokenExpired) as e:
                await asyncio.sleep(5)
                a = await dispatcher.get_access_token(DATA['sp_dc'])
                access_token = a['token']
                client_token = await dispatcher.get_client_token(a['id'])
                print(e)

            if song is not None:
                song = song.json()
                url = await tracks_methods.get_song_url(song)
                if url is None:
                    lyrics = None
                    continue
                if old_url is None:
                    lyrics = None
                    old_url = url
                if old_url != url:
                    lyrics = None
                    previous_id = -1
                    waiting_for_id = -1
                    last_sync_time = time.perf_counter()
                    old_url = url

                if lyrics is None:
                    try:
                        req = await dispatcher.get_lyric_request(access_token, client_token, url)
                    except (ConnectionError, exceptions.AccessTokenExpired) as e:
                        await asyncio.sleep(5)
                        a = (await dispatcher.get_access_token(DATA['sp_dc']))
                        access_token = a['token']
                        client_token = await dispatcher.get_client_token(a['id'])
                        req = await dispatcher.get_lyric_request(access_token, client_token, url)
                        print(e)

                    lyrics = lyrics_handler.simplify_lyrics(req)
                    if not lyrics:
                        last_sync_time = time.perf_counter()
                        allow_sync = False
                        continue

                progress = song['progress_ms']
                current_time_id = lyrics_handler.get_by_time(progress, lyrics, response="id")
                if abs(previous_id - current_time_id) > 3:
                    waiting_for_id = current_time_id
                previous_id = current_time_id
                if current_time_id == -3:
                    waiting_for_id = -1
                if current_time_id == -4:
                    waiting_for_id = 0

                if current_time_id >= waiting_for_id or waiting_for_id == -1 and current_time_id != -3:
                    waiting_for_id = lyrics_handler.get_by_time(progress + 3000, lyrics, response="id") + 1
                    delta_id = waiting_for_id - current_time_id
                    line_for_print = lyrics_handler.get_by_timestamp_id(current_time_id, lyrics)
                    for i in range(1, delta_id):
                        line_for_print = line_for_print + " " + lyrics_handler.get_by_timestamp_id(current_time_id + i,
                                                                                                   lyrics,
                                                                                                   response="line")
                    last_sync_time = time.perf_counter()
                    allow_sync = False
                    album_id = await tracks_methods.get_album_url(song)
                    if album_id in tracks_data:
                        song_status = tracks_data[album_id]
                        await dispatcher.send_status(text=line_for_print, emoji=song_status[1],discord_token=DATA['discord_token'])
                    else:
                        await dispatcher.send_status(text=line_for_print, emoji=DATA['base_emoji'],discord_token=DATA['discord_token'])
        else:
            if time.perf_counter() - last_sync_time > DISCORD_SYNC_DELAY:
                allow_sync = True
                last_sync_time = 0


if __name__ == "__main__":
    DATA = json.load(open("data.json", encoding='utf-8'))
    TRACKS = json.load(open("tracks.json", encoding="utf-8"))
    print("Starting...")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
    print("Ending...")
