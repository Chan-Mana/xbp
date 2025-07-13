import serial
import qrcode
from PIL import Image
import time
import sys

ARDUINO_PORT = '/dev/cu.usbmodem101'
BAUD_RATE = 9600

try:
    ser = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)
    print(f"シリアルポート {ARDUINO_PORT} に接続しました。")
except serial.SerialException as e:
    print(f"エラー: シリアルポート {ARDUINO_PORT} に接続できません。詳細: {e}")
    sys.exit(1)

def run_game():
    while True:
        cmd = input("開始するには「start」と入力してください: ")
        if cmd.lower() == "start":
            print("ゲームスタート！60秒間でスコアを記録します。")

            DURATION = 60
            INTERVAL = 0.2  # 感知間隔（秒）
            total_score = 0
            start_time = time.time()

            while time.time() - start_time < DURATION:
                interval_start = time.time()
                max_score_in_window = 0

                # INTERVAL 秒間に来たスコアを比較して最大値だけ保持
                while time.time() - interval_start < INTERVAL:
                    if ser.in_waiting:
                        try:
                            line = ser.readline().decode('utf-8').strip()
                            if line.startswith("score:"):
                                current = int(line.split(":")[1])
                                max_score_in_window = max(max_score_in_window, current)
                        except:
                            continue

                # INTERVAL の中で最も大きかった値をスコアに追加
                if max_score_in_window > 0:
                    total_score += max_score_in_window
                    print(f"感知：+{max_score_in_window}点 → 合計: {total_score}")

            print(f"\n⌛ 終了！あなたの合計スコアは {total_score} 点です。")

            # QRコード生成（URLにスコアを含める）
            url = f"https://chan-mana.github.io/dart-score-viewer/index.html?score={total_score}"
            print(f"生成されたURL: {url}")

            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            img.save("score_qr.png")
            img.show()

            break
        else:
            print("「start」と入力してください。")

if __name__ == "__main__":
    run_game()
    ser.close()
    print("プログラムを終了します。")