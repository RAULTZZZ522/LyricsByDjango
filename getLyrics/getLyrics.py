import requests
import execjs
import re
import os
import time
import sys
import io
from getId import get_song_ids  # 你已有的函数

# 强制将标准输出改为 utf-8 编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 清洗歌词
def clean_lyric_text(raw_lyric):
    cleaned_lines = []
    for line in raw_lyric.splitlines():
        line = re.sub(r'\[\d{2}:\d{2}\.\d{2,3}\]', '', line)
        line = line.strip()
        if line:
            cleaned_lines.append(line)
    return '\n'.join(cleaned_lines)

# 爬取并保存歌词
def get_lyrics(song_name, song_id, save_folder): 
    # 加载加密js
    js_file = open('getLyrics/code.js', encoding='utf-8').read()
    js_code = execjs.compile(js_file)

    # 请求参数加密
    i5n = {
        "id": f"{song_id}", 
        "lv": -1,
        "kv": -1,
        "tv": -1
    }
    res = js_code.call('getData', i5n)

    # 请求头
    headers = {
        'user-agent': 'Mozilla/5.0',
        'referer': 'https://music.163.com/',
        'cookie': 'NMTID=00O4NH78_enEZFKbkwptnPtxvA9p68AAAGTASCxIw; _iuqxldmzr_=32; _ntes_nnid=83cfc90cc5a47c2c7daa5ba661cddf1e,1730890740743; _ntes_nuid=83cfc90cc5a47c2c7daa5ba661cddf1e; WEVNSM=1.0.0; WNMCID=fxlqvh.1730890740950.01.0; __snaker__id=4bW7loTk9ikdH1PB; ntes_utid=tid._.8%252BgtDYaRTEFAUlUEEVPGGxAHXQTwuyNV._.0; sDeviceId=YD-XbHaoMOPWHRFFkVFFBbHTlADCRG1u2MS; WM_TID=vJfeANy1l8lAAEUQBUbXTxETHBX2Tty%2B; ntes_kaola_ad=1; MUSIC_U=006597DEB90B637F268D2F2426D56243B18B5920649B2E0706BACA8DD0C36F85D67BB84224C314D3A63103927C0B41333CCA03BEF6112714A228E93BAA228CE9C1B5FF6789E28999A351B7E97A4DEB5D52B4998F9148F502C6902F3A693A1391B8B78DF487EE1F80D338C5B03003D8E4931553C4019008D8C8DFFC9E973D7B1693EECA0F502878ABAECF25DE8666A1D5C10FE38CC51B1370DD97A4CB2191344861D10E1B1AC2E2EEC68E927F56D7A745D489308A59CABA9761240E3F51A55C1F63449E56B36A21DB460038019DD9F193897DCEF212049B725CA8A02028B37ED30184FF905F6AFE6CB88750B3ED60574AE0245A085FBE3E02D297BEC865DA791F2EF902E4854A18E0BE683FD515ABD82199D8E7DCB2281E2863C389D50A1124082C8E1056A01EC8E569F6EC1E2BC7735B02BC03A1DC55E8742782A6298AA7C4DF83A37883F89E8C880F8330925D3FA2CBED; __remember_me=true; __csrf=2b2f1c795b0a71c432579562b27d7fc7; __csrf=2b2f1c795b0a71c432579562b27d7fc7; WM_NI=%2F03juGbQi7qIWUIhyB75mwY8zz7CIZV0mHn9rTwp7YaUC8ereE03aqHFu6Sl6uNPdiWaDb9xev7u9DZptdi5jXw9C2w%2FINuXZOKrSeX%2BW0otJGaqaspEkE%2BlJZfoPmNUejY%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eea6b26da592afb6c562b4a88ea3d85e878e8bacd26e83efaf8eb367939af78ffb2af0fea7c3b92aedf0fd8bf84da28fa7d8f443958b8789fc4af5eba398dc34baa6f9a4cc5296f0a3a9ed33b28cb991b653a38b8dd9e87aa79b00d4e47b8c9abbd7d268f6ab82b1e76395bf8c83bc74a7aaf996bc509ab0bc85ec3faa88b9dac23ab5f187aff8549a918593d26f9cf599d1ee808a99af92e479b49ba5a6aa688a86aa90d3678e8bab8bdc37e2a3; gdxidpyhxdE=iPiiWX3%2FOcRBZ8tr%2BwGsCTVCdbQ10EMXB%2FUdkJyVe%2FZNcB%2BiXIeQSg8PIHDdWlE9xrILuJxeRXgIdP8gGcZjvBu%5C8ACLmByDYLz7AkQxGzt%2B0DwLwOu4ZejB1iYcDUzmq5BZu99BCpcyAq4jw8zPB7yjVZeHHzxQdN3r4mEM%2FKgSvh1a%3A1744356900115; JSESSIONID-WYYY=Tm%2BTcvTlyuPNK9Nuzcdi9wYD%2BnDi8d7xykf9iGMwbUSQinMUMDKIwjyG57yQ%2B97R2NWUTlClAsOd01kH3auvspYyoE3sO4q79SkaQHBdJOsOqatC4gQ1VqDPHAgDodJdmNTJ0stui64ZuNdmFtAGYe6%2Fx0Sn2geJgslRRAXz5CF%2FvrAf%3A1744360188125' # ✅ 建议提取到 config.py 或环境变量中
    }

    url = 'https://music.163.com/weapi/song/lyric?csrf_token=2b2f1c795b0a71c432579562b27d7fc7'
    data = {
        "params": res['encText'],
        "encSecKey": res['encSecKey']
    }

    try:
        response = requests.post(url=url, headers=headers, data=data)
        response.encoding = 'utf-8'
        json_data = response.json()

        # 提取并清洗歌词
        lyric = clean_lyric_text(json_data['lrc']['lyric'])

        # 保存路径
        root_folder = os.path.join("getLyrics", "data", save_folder)
        os.makedirs(root_folder, exist_ok=True)
        filename = os.path.join(root_folder, f"{song_name}.txt")

        # 保存文件
        with open(filename, "w", encoding="utf-8") as f:
            f.write(lyric)
        print(f"✅ 已保存: {filename}")
    except Exception as e:
        print(f"❌ 获取失败：{song_name}（ID: {song_id}） 错误信息：{e}")

# 主函数
if __name__ == '__main__':
    singer_name = "许巍"
    song_list = [
    "蓝莲花",
    "曾经的你",
    "故乡",
    "旅行",
    "时光",
    "像风一样自由",
    "星空",
    "家",
    "完美生活",
    "天堂",
    "礼物",
    "故事",
    "温暖",
    "难忘的一天",
    "每一刻都是崭新的",
    "远航",
    "爱如少年",
    "悠远的天空",
    "方向",
    "风和日丽"
]


    # 获取歌曲名-歌曲ID字典
    song_dict = get_song_ids(song_list)

    # 创建文件夹并逐首获取歌词
    for name, sid in song_dict.items():
        if sid is not None:
            get_lyrics(song_name=name, song_id=sid, save_folder=singer_name)
            time.sleep(1)  # 防止请求太快被封
        else:
            print(f"⚠️ 未找到歌曲：{name}")
