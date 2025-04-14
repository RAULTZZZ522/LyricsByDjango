import os
import pymysql

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "chen103601 `",
    "database": "lyrics_db",
    "charset": "utf8mb4"
}

def insert_lyrics_to_mysql(data_path="./getLyrics/data"):
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()

    for artist_name in os.listdir(data_path):
        artist_folder = os.path.join(data_path, artist_name)
        if not os.path.isdir(artist_folder):
            continue

        # 插入 artist（若不存在）
        cursor.execute("SELECT id FROM lyrics_artist WHERE name = %s", (artist_name,))
        artist = cursor.fetchone()
        if artist:
            artist_id = artist[0]
        else:
            cursor.execute("INSERT INTO lyrics_artist (name) VALUES (%s)", (artist_name,))
            artist_id = cursor.lastrowid
            print(f"✅ 插入歌手：{artist_name}（id={artist_id}）")

        for filename in os.listdir(artist_folder):
            if not filename.endswith(".txt"):
                continue

            song_title = os.path.splitext(filename)[0]
            file_path = os.path.join(artist_folder, filename)

            # 读取歌词内容
            with open(file_path, "r", encoding="utf-8") as f:
                lyric_text = f.read()

            # 插入 song
            cursor.execute("""
                INSERT INTO lyrics_song (title, album, release_date, genre, artist_id)
                VALUES (%s, %s, %s, %s, %s)
            """, (song_title, None, None, None, artist_id))
            song_id = cursor.lastrowid
            print(f"🎵 插入歌曲：{song_title}（id={song_id}）")

            # 插入 lyric
            cursor.execute("""
                INSERT INTO lyrics_lyric (content, song_id)
                VALUES (%s, %s)
            """, (lyric_text, song_id))
            print(f"📝 插入歌词：{artist_name} - {song_title}")

    conn.commit()
    conn.close()
    print("🎉 所有歌词成功写入数据库！")

if __name__ == "__main__":
    insert_lyrics_to_mysql()
