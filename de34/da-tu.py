import serial
import time
import json
import subprocess
import webbrowser # これを追加！

# Arduinoが接続されているシリアルポートを設定
# Windowsの場合: 'COMx' (例: 'COM3')
# macOS/Linuxの場合: '/dev/tty.usbmodemXXXX' や '/dev/ttyUSBx' (例: '/dev/ttyUSB0')
arduino_port = '/dev/cu.usbmodem1101' # ***ご自身の環境に合わせて変更してください！***
baud_rate = 9600

# GitHubリポジトリのパス (ローカルPC上でのパス)
github_repo_path = '/Users/manatotamura/GitHub/my-darts-score' # ***ご自身の環境に合わせて変更してください！***
json_file_path = f"{github_repo_path}/score.json" # スコアを保存するJSONファイルのパス

# ★ここにGitHub PagesのURLを設定してください！★
# 例: 'https://Chan-Mana.github.io/[リポジトリ名]/'
github_pages_url = 'https://Chan-Mana.github.io/my-darts-score/' # ***ご自身のGitHub PagesのURLに必ず変更してください！***

# Gitコマンドを実行してGitHubにプッシュする関数
def update_github_pages(score_data):
    """スコアデータをJSONファイルに保存し、GitHubにプッシュする"""
    try:
        # スコアをJSONファイルに保存
        with open(json_file_path, 'w') as f:
            json.dump(score_data, f, indent=4)
        print(f"Score saved to {json_file_path}")

        # Gitコマンドを実行してGitHubにプッシュ
        subprocess.run(['git', 'add', json_file_path], cwd=github_repo_path, check=True)
        subprocess.run(['git', 'commit', '-m', 'Update darts score'], cwd=github_repo_path, check=True)
        subprocess.run(['git', 'push'], cwd=github_repo_path, check=True)
        print("Score successfully pushed to GitHub!")

        # ★GitHub Pagesのサイトを自動で開く★
        print(f"Opening GitHub Pages: {github_pages_url}")
        webbrowser.open(github_pages_url)

    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {e}")
        print("Please ensure your local Git repository is set up correctly and you have push access.")
    except Exception as e:
        print(f"Error updating GitHub Pages: {e}")

try:
    ser = serial.Serial(arduino_port, baud_rate, timeout=1)
    print(f"Connected to Arduino on {arduino_port}")
    print("Arduinoからの最終スコアを待機中...")

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            print(f"Received from Arduino: {line}")

            if "最終合計点:" in line:
                try:
                    final_score_str = line.split(":")[1].strip()
                    final_score = int(final_score_str)
                    print(f"Final Score detected: {final_score}")

                    score_data = {"last_score": final_score, "timestamp": int(time.time())}
                    update_github_pages(score_data)
                    
                    print("スコア処理が完了しました。")
                    break 
                except ValueError:
                    print(f"Could not parse score from line: {line}")
                except Exception as e:
                    print(f"Error processing score: {e}")
        time.sleep(0.1)

except serial.SerialException as e:
    print(f"Could not open serial port {arduino_port}: {e}")
    print("Arduinoが接続されているか、または正しいポートが設定されているか確認してください。")
except KeyboardInterrupt:
    print("ユーザーによってスクリプトが中断されました。")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("シリアルポートを閉じました。")