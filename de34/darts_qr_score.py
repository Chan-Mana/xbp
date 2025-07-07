import serial
import qrcode
from PIL import Image
import time

# Arduinoのポート（例：Mac）
ser = serial.Serial('/dev/cu.usbmodem1101', 9600)

while True:
    cmd = input("開始するには「start」と入力：")
    if cmd.lower() == "start":
        print("ゲームスタート！10秒間だけスコアを記録します。")

        start_time = time.time()
        total_score = 0

        while time.time() - start_time < 10:
            if ser.in_waiting:
                line = ser.readline().decode().strip()
                if line.isdigit():
                    total_score += int(line)
                    print(f"得点を加算：{line} → 合計：{total_score}")

        print(f"\n制限時間終了！あなたの合計点は：{total_score} 点")

        # ✅ GitHub Pages上のスコアURLをQR化
        url = f"https://chan-mana.github.io/dart-score-viewer/index.html?score={total_score}"

        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=4
        )
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save("score_qr.png")
        img.show()
        break