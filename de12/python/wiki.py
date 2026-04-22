import requests
from googletrans import Translator

# Genius APIから歌詞を取得
def get_song_lyrics(song_title, api_key):
    # Genius APIエンドポイント
    search_url = "https://api.genius.com/search"
    headers = {'Authorization': f'Bearer {api_key}'}

    # 曲名を検索
    response = requests.get(search_url, params={'q': song_title}, headers=headers)
    data = response.json()

    # 歌詞のURLを取得
    song_path = data['response']['hits'][0]['result']['path']
    song_url = f'https://genius.com{song_path}'

    # 歌詞のページをスクレイピングして歌詞を取得
    lyrics_response = requests.get(song_url)
    page_html = lyrics_response.text

    # Geniusの歌詞ページから歌詞部分を抽出
    start_index = page_html.find('<div class="lyrics">')
    end_index = page_html.find('<div class="footer">')

    lyrics = page_html[start_index:end_index]
    lyrics = lyrics.replace('<p>', '').replace('</p>', '\n').strip()

    return lyrics

# 翻訳を実行
def translate_lyrics(lyrics, target_language='ja'):
    translator = Translator()
    translated = translator.translate(lyrics, dest=target_language)
    return translated.text

# 使用例
genius_api_key = 'XnoT6oh7kp6cX9hEvVVt8nX91PoyccufLf85IpVk9owOj5Z2M3xkzoVYgYW-LRIskyY2wof4ujPix6JIewNyEA'  # Genius APIキーをここに入力
song_title = 'Shape of You'  # 翻訳したい曲のタイトル

# 歌詞を取得
song_lyrics = get_song_lyrics(song_title, genius_api_key)

# 歌詞を表示
print("原文の歌詞:")
print(song_lyrics)

# 翻訳
translated_lyrics = translate_lyrics(song_lyrics, target_language='ja')

# 翻訳後の歌詞を表示
print("\n翻訳後の歌詞:")
print(translated_lyrics)