import serial
import time
import qrcode     # QRコード生成ライブラリ
import os         # ファイル操作用
import subprocess # QRコード画像を自動で開くため

# --- 設定項目 ---
# Arduinoが接続されているシリアルポートを設定してください。
# この値は、Arduino IDEでボードに書き込む際に選択したポートと同じです。
# 例: 'COM3' (Windows) または '/dev/cu.usbmodemXXXX' (Mac)
arduino_port = '/dev/cu.usbmodem1101' # ★★★ここをご自身のPCのポート名に合わせて変更してください！★★★
baud_rate = 9600

# 生成されるQRコード画像の保存先を設定してください。
# 例1: Pythonスクリプトと同じディレクトリに保存する場合（これがデフォルトで簡単です）
qr_code_output_path = "darts_score_qr.png" 
# 例2: デスクトップに保存したい場合（下のコメントを外し、上の行をコメントアウトして使用）
# qr_code_output_path = os.path.join(os.path.expanduser("~"), "Desktop", "darts_score_qr.png")
# -----------------

def generate_and_show_qr_code(score):
    """
    指定されたスコアを含むQRコードを生成し、画像として保存し、自動で開く関数
    """
    qr_data = f"ダーツの合計点: {score}点" # QRコードに含める情報（例: "ダーツの合計点: 150点"）
    print(f"DEBUG: QRコードに含めるデータ: {qr_data}") # デバッグ用メッセージ

    try:
        # QRコードオブジェクトを作成
        qr = qrcode.QRCode(
            version=1, # QRコードのバージョン（情報の複雑さ）。1が最もシンプルで一般的です。
            error_correction=qrcode.constants.ERROR_CORRECT_L, # エラー訂正レベル (L, M, Q, H - Lが最低で画像がシンプル)
            box_size=10, # QRコードの各「点」のサイズ（ピクセル）
            border=4, # QRコードの周りの余白のサイズ（「点」の数）
        )
        qr.add_data(qr_data) # QRコードにデータを追加
        qr.make(fit=True) # QRコード画像を生成するための準備

        # 画像として作成（Pillowライブラリを使用）
        img = qr.make_image(fill_color="black", back_color="white")
        print("DEBUG: QRコード画像を生成しました。") 
        
        # 画像を保存
        img.save(qr_code_output_path)
        print(f"DEBUG: QRコードを {qr_code_output_path} に保存しました。")

        # 保存したQRコード画像をOSのデフォルトの画像ビューアで開く
        try:
            if os.name == 'nt': # Windowsの場合
                os.startfile(qr_code_output_path)
            elif os.name == 'posix': # macOS / Linuxの場合
                # macOSでは 'open' コマンドが一般的。Linuxでは 'xdg-open' など
                subprocess.run(['open', qr_code_output_path], check=True) # macOS向け
            print("DEBUG: QRコード画像の自動オープンを試みました。")
        except Exception as e:
            print(f"ERROR: QRコード画像の自動オープンに失敗しました: {e}")
            print("手動で保存場所からファイルを開いてください。")

    except Exception as e:
        print(f"ERROR: QRコードの生成または保存中にエラーが発生しました: {e}")


try:
    # シリアルポートを開く
    # Pythonスクリプトを実行する際は、Arduino IDEのシリアルモニターは閉じておく必要があります！
    ser = serial.Serial(arduino_port, baud_rate, timeout=1)
    print(f"Connected to Arduino on {arduino_port}")
    print("Arduinoからの最終スコアを待機中...")

    while True: # Arduinoからの出力を常に監視するループ
        if ser.in_waiting > 0: # シリアルポートにデータが来ているかチェック
            line = ser.readline().decode('utf-8').strip() # 1行読み込み、UTF-8でデコードし、前後の空白を削除
            print(f"Received from Arduino: {line}") # 受信した行をVS Codeのターミナルに表示

            if "最終合計点: " in line: # 受信した行に「最終合計点:」が含まれていれば
                try:
                    final_score_str = line.split(":")[1].strip() # 「:」で分割し、スコア部分を抽出
                    final_score = int(final_score_str) # 抽出したスコアを整数に変換
                    print(f"最終スコアを検出しました: {final_score}")

                    generate_and_show_qr_code(final_score) # 検出したスコアでQRコードを生成・表示

                    print("スコア処理が完了しました。")
                    break # スコアを受け取って処理が完了したので、Pythonスクリプトを終了する
                except ValueError:
                    print(f"ERROR: スコアの解析中にエラーが発生しました: {line}")
                except Exception as e:
                    print(f"ERROR: スコア処理中に予期せぬエラーが発生しました: {e}")
        time.sleep(0.1) # CPU使用率を抑えるために短い間隔で待機

except serial.SerialException as e:
    print(f"ERROR: シリアルポート {arduino_port} を開けませんでした: {e}")
    print("Arduinoが正しく接続されているか、または設定されたポート番号が正しいか確認してください。")
except KeyboardInterrupt:
    print("ユーザーによってスクリプトが中断されました。")
finally:
    if 'ser' in locals() and ser.is_open: # シリアルポートが開いていれば
        ser.close() # 閉じる
        print("シリアルポートを閉じました。")