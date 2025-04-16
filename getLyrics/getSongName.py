import os
import json
import requests
import time

# 创建保存数据的文件夹
save_dir = os.path.join(os.getcwd(), 'getLyrics', 'data')
os.makedirs(save_dir, exist_ok=True)

# 设置请求头
headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://music.163.com/",
}

# 获取歌手热门歌曲
def get_song_names(artist_name, limit=50):
    print(f"正在搜索歌手：{artist_name}")
    url = "https://music.163.com/api/search/get"
    params = {
        "s": artist_name,
        "type": 100,
        "limit": 1,
        "offset": 0,
    }
    resp = requests.post(url, headers=headers, data=params)
    data = resp.json()
    try:
        artist_id = data['result']['artists'][0]['id']
    except:
        print(f"未找到歌手：{artist_name}")
        return []

    print(f"获取到 {artist_name} 的ID：{artist_id}，正在抓取歌曲...")
    song_url = f"https://music.163.com/api/artist/{artist_id}"
    resp = requests.get(song_url, headers=headers)
    data = resp.json()
    song_names = [song['name'] for song in data.get('hotSongs', [])]
    print(f"🎵 {artist_name} 的歌曲抓取完成，共 {len(song_names)} 首。\n")
    return song_names

# 中文流行歌手列表（20位）
singers = [
    "林俊杰", "邓紫棋", "张学友", "王菲",
    "张杰", "李荣浩", "薛之谦", "华晨宇", "张靓颖",
    "孙燕姿", "陶喆", "李克勤", "陈奕迅", "杨丞琳",
    "张惠妹", "蔡依林", "林宥嘉", "汪峰", "许嵩"
]

all_songs = {}

# 依次抓取所有歌手的歌曲
for singer in singers:
    songs = get_song_names(singer)
    all_songs[singer] = songs
    time.sleep(1)  # 延迟，防止反爬虫

# 保存为 JSON 文件
save_path = os.path.join(save_dir, '华语歌手.json')
with open(save_path, 'w', encoding='utf-8') as f:
    json.dump(all_songs, f, ensure_ascii=False, indent=2)

