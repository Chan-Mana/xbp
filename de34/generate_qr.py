import serial
import qrcode
from PIL import Image

# あなたのArduinoポートに変更！
ser = serial.Serial('/dev/cu.usbmodem101', 9600, timeout=1)

# GitHub Pagesのスコア表示ページ（URLにスコアを付ける）
BASE_URL = "https://chan-mana.github.io/dart-score-viewer/"

print("スコアを受信中...")

while True:
    line = ser.readline().decode().strip()
    if line.isdigit():
        score = int(line)
        url = BASE_URL + str(score)
        print(f"スコア {score} をQRコード化: {url}")

        # QRコード生成・表示
        qr = qrcode.make(url)
        qr.show()
        break  # 終了