import serial
import qrcode
from PIL import Image
import time

# Arduinoのシリアルポートと通信速度（ポート名は環境による）
ser = serial.Serial('/dev/cu.usbmodem101', 9600, timeout=1)  # Macの場合: '/dev/tty.usbmodemxxxx'

last_score = None

while True:
    try:
        line = ser.readline().decode('utf-8').strip()
        if "Score:" in line:
            score = line.split("Score: ")[1]
            if score != last_score:
                last_score = score
                print(f"新しいスコア: {score}")

                # QRコード生成
                qr = qrcode.make(f"Your score is: {score}")
                qr.save("score_qr.png")

                # 表示
                img = Image.open("score_qr.png")
                img.show()
    except Exception as e:
        print("エラー:", e)
        break