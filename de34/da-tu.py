import serial
import qrcode

# 設定
SERIAL_PORT = '/dev/cu.usbmodem101'  # ← あなたのArduinoポートに合わせて
BAUD_RATE = 9600
SAVE_PATH = 'score_qr.png'

def fsr_to_score(fsr_value):
    return int(fsr_value / 1023 * 50)

def generate_qr(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data)  # ← ここに数字だけを入れる
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    return img

def main():
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
        print("Arduinoからのスコアを待機中...")

        while True:
            line = ser.readline().decode('utf-8').strip()
            if line.isdigit():
                fsr_value = int(line)
                score = fsr_to_score(fsr_value)

                qr_data = str(score)  # ← ここでスコアそのまま入れる
                print(f"スコア: {score}")
                print(f"QRコードに埋め込むデータ: {qr_data}")

                img = generate_qr(qr_data)
                img.save(SAVE_PATH)
                print(f"QRコード画像を保存しました: {SAVE_PATH}")
                break

if __name__ == '__main__':
    main()