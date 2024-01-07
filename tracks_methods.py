async def get_song_url(info):
    if info is None:
        return None
    if info['item'] is None:
        return None
    return info['item']['id']


async def get_album_url(info):
    if info is None:
        return None
    if info['item'] is None:
        return None
    return info['item']['album']['id']
