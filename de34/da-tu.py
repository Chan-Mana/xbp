import serial
import time
import qrcode # QRコードライブラリ
import os     # ファイル操作用
import subprocess # QRコード画像を自動で開くため

# Arduinoが接続されているシリアルポートを設定
arduino_port = '/dev/cu.usbmodem1101' # ***ご自身の環境に合わせて変更してください！***
baud_rate = 9600

# QRコード画像を保存するパス (例: スクリプトと同じディレクトリ)
# デスクトップに保存したい場合は、以下のように変更できます
# qr_code_output_path = os.path.join(os.path.expanduser("~"), "Desktop", "darts_score_qr.png")
qr_code_output_path = os.path.join(os.path.expanduser("~"), "Desktop", "darts_score_qr.png") # スクリプトと同じディレクトリに保存

def generate_and_show_qr_code(score):
    """
    指定されたスコアを含むQRコードを生成し、画像として保存し、自動で開く
    """
    qr_data = f"ダーツの合計点: {score}点"
    
    try:
        # QRコードオブジェクトを生成
        qr = qrcode.QRCode(
            version=1, # QRコードのバージョン (1-40, 大きいほど情報量が多い)
            error_correction=qrcode.constants.ERROR_CORRECT_L, # エラー訂正レベル
            box_size=10, # 各ボックスのピクセル数
            border=4, # 余白のボックス数
        )
        qr.add_data(qr_data) # データを追加
        qr.make(fit=True) # QRコードを生成

        # 画像として出力 (PIL (Pillow) ライブラリが必要)
        img = qr.make_image(fill_color="black", back_color="white")
        
        # 画像を保存
        img.save(qr_code_output_path)
        print(f"QRコードを {qr_code_output_path} に保存しました。")

        # 保存したQRコード画像を自動で開く
        try:
            if os.name == 'nt': # Windowsの場合
                os.startfile(qr_code_output_path)
            elif os.name == 'posix': # macOS / Linuxの場合
                subprocess.run(['open', qr_code_output_path], check=True) # macOS
            # Linuxの場合: subprocess.run(['xdg-open', qr_code_output_path], check=True)
            print("QRコード画像を開きました。")
        except Exception as e:
            print(f"QRコード画像の自動オープンに失敗しました: {e}")
            print("手動でファイルを開いてください。")

    except Exception as e:
        print(f"QRコードの生成または保存中にエラーが発生しました: {e}")


try:
    ser = serial.Serial(arduino_port, baud_rate, timeout=1)
    print(f"Connected to Arduino on {arduino_port}")
    print("Arduinoからの最終スコアを待機中...")

    while True: # Arduinoからの出力を継続的に監視
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            print(f"Received from Arduino: {line}")

            if "最終合計点:" in line: # '最終合計点:' という文字列を含む行を検出
                try:
                    final_score_str = line.split(":")[1].strip() # スコア部分を抽出
                    final_score = int(final_score_str) # 整数に変換
                    print(f"Final Score detected: {final_score}")

                    generate_and_show_qr_code(final_score) # QRコードを生成して表示

                    print("スコア処理が完了しました。")
                    break # スコアを受け取って処理が完了したので、スクリプトを終了
                except ValueError:
                    print(f"Could not parse score from line: {line}")
                except Exception as e:
                    print(f"Error processing score: {e}")
        time.sleep(0.1) # CPU使用率を抑えるための短い遅延

except serial.SerialException as e:
    print(f"Could not open serial port {arduino_port}: {e}")
    print("Arduinoが接続されているか、または正しいポートが設定されているか確認してください。")
except KeyboardInterrupt:
    print("ユーザーによってスクリプトが中断されました。")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("シリアルポートを閉じました。")