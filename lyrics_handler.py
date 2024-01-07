import json


def simplify_lyrics(req):
    lyrics = {
        "TimesArray": [],
        "TimedLines": {},
        "Sync": False
    }
    if req.status_code == 200:
        requested_lyric = json.loads(req.text)['lyrics']
        if requested_lyric['syncType'] == "UNSYNCED":
            return None
        for line in requested_lyric['lines']:
            lyrics['TimesArray'].append(line['startTimeMs'])
            lyrics['TimedLines'][line['startTimeMs']] = line['words']
            lyrics['Sync'] = True
        return lyrics
    else:
        return None


def get_by_timestamp_id(timestamp_id, lirics, response="line"):
    """
    response types:
    "line", "timestamp"
    """
    if len(lirics['TimesArray']) < timestamp_id or timestamp_id < 0:
        return "♪"
    if lirics['TimesArray'][timestamp_id] not in lirics['TimedLines']:
        return "♪"
    if response == "line":
        return lirics['TimedLines'][lirics['TimesArray'][timestamp_id]]
    elif response == "timestamp":
        return lirics['TimesArray'][timestamp_id]


def get_by_time(time_ms, lirics, response="line"):
    """
    response types:
    "line", "timestamp",'id"
    """
    for i in range(len(lirics['TimesArray']) - 1):
        if int(lirics['TimesArray'][i]) <= time_ms < int(lirics['TimesArray'][i + 1]):
            if response == "line":
                return lirics['TimedLines'][lirics['TimesArray'][i]]
            elif response == "id":
                return i
            elif response == "timestamp":
                return lirics['TimesArray'][i]
    if int(lirics['TimesArray'][0]) > time_ms:
        if response == "line":
            return "♪"
        elif response == "id":
            return -3
        elif response == "timestamp":
            return "0"
    if int(lirics['TimesArray'][len(lirics['TimesArray']) - 1]) < time_ms:
        if response == "line":
            return "♪"
        elif response == "id":
            return -4
        elif response == "timestamp":
            return "0"
