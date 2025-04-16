import requests
import time

def get_song_ids(song_names, delay=0.5):
    url = "https://music.163.com/api/search/get"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://music.163.com"
    }

    result_dict = {}

    for idx, name in enumerate(song_names, start=1):
        print(f"正在获取第 {idx}/{len(song_names)} 首歌的ID：{name} ...")

        data = {
            "s": name,
            "type": 1,
            "offset": 0,
            "limit": 1
        }

        try:
            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status()
            json_data = response.json()

            songs = json_data.get("result", {}).get("songs", [])
            if songs:
                song_id = songs[0]["id"]
                result_dict[name] = song_id
            else:
                result_dict[name] = None
        except Exception as e:
            print(f"获取『{name}』失败：{e}\n")
            result_dict[name] = None

        time.sleep(delay)

    return result_dict


