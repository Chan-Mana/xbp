import random
print ("　　　　　　　　　XBPアドベンチャーへようこそ！！")
print("ルール：君はXBPの新入生だ。先生たちを倒して単位を獲得しよう！")
print("　　　　君の武器は「Fusion」「Python」「Cura」の３つだよ！")
print("＊＊＊上の表記のまま入力しないとその場でゲームが終わります＊＊＊")
print("　　　　さあ、急ごう！")
def yes_no_question():
    while True:
        answer = input("Are you ready？（yes/no）: ").strip().lower()

        if answer == "yes":
            print("さあ行こう！")
            break
        elif answer == "no":
            print("戦闘に備えてから来よう！")
            exit()
        else:
            print("無効な入力だ")
            exit()

yes_no_question()
print("　")
print("＊")
print("＊")
print("＊")
print("　")
def rock_paper_scissors():
    
    choices = ["Fusion", "Python", "Cura"]
    
    
    computer_choice = random.choice(choices)
    print("道用先生が現れた。（特徴：よく転ける)")
    player_choice = input("さあ「Fusion」「Python」「Cura」どれで戦おうか: ")

    if player_choice not in choices:
        print("道用先生：そんなの反則だよ。君はここで終わりだ。")
        exit()

    print(f"あなたの選択: {player_choice}")
    print(f"道用先生: {computer_choice}")

    if player_choice == computer_choice:
        print("道用先生：まさか同じものを出すとは、気が合うから進んでいいよ。")
        print("　")
        print("道用先生は意外とちょろかった。とりあえず進もう。")
    elif (player_choice == "Fusion" and computer_choice == "Python") or \
         (player_choice == "Python" and computer_choice == "Cura") or \
         (player_choice == "Cura" and computer_choice == "Fusion"):
        print ("道用先生：うわあああああああ")
        print("　")
        print (player_choice, "を見た瞬間倒れた。君の勝ちだ。先を急ごう。")
    else:
        print("道用先生：ふふふまだ",player_choice,"を使っているのかい？君の負けだよ。100年後にまた待ってるね。")
        exit()
        
rock_paper_scissors()
print("　")
print("＊")
print("＊")
print("＊")
print("　")
def rock_paper_scissors():
    
    choices = ["Fusion", "Python", "Cura"]
    
    
    computer_choice = random.choice(choices)
    print("山崎先生が現れた。（特徴：声がでかい)")
    player_choice = input("さあ「Fusion」「Python」「Cura」どれで戦おうか: ")

    if player_choice not in choices:
        print("山崎先生：それはちょっとなしかなー。ここで終わりね。")
        exit()

    print(f"あなたの選択: {player_choice}")
    print(f"山崎先生: {computer_choice}")

    if player_choice == computer_choice:
        print("山崎先生：それ俺も使ってる！ちょっと話そうよ。")
        print("　")
        print("山崎先生も意外とちょろかった。どんどん進もう。")
    elif (player_choice == "Fusion" and computer_choice == "Python") or \
         (player_choice == "Python" and computer_choice == "Cura") or \
         (player_choice == "Cura" and computer_choice == "Fusion"):
        print ("山崎先生：ぎゃあああああああ")
        print("　")
        print (player_choice, "を見た瞬間走っていった。君の勝ちだ。さあ先を急ごう。")
    else:
        print("山崎先生：",player_choice,"なんか時代遅れっすよねー。君の負けだよ。100年後にまた待ってるね。")
        exit()
 
rock_paper_scissors()
print("　")
print("＊")
print("＊")
print("＊")
print("　")
print("ゴゴゴゴ、、、、")
print("！？！？")
print("　")
print("＊")
print("＊")
print("＊")
print("　")
def rock_paper_scissors():
    
    choices = ["Fusion", "Python", "Cura"]
    
    
    computer_choice = random.choice(choices)
    print("ラスボス泉水先生が現れた。（特徴：たまに聞き取れない)")
    player_choice = input("さあ「Fusion」「Python」「Cura」どれで戦おうか: ")

    if player_choice not in choices:
        print("泉水先生：それはダメだ。君はここで終わり。")
        exit()

    print(f"あなたの選択: {player_choice}")
    print(f"泉水先生: {computer_choice}")

    if player_choice == computer_choice:
        print("泉水先生：人と被るのは嫌いなんだ。君はここまでだ。")
        print("　")
        print("泉水先生はちょろくなかった。またはじめから頑張ろう。")
        exit()
    elif (player_choice == "Fusion" and computer_choice == "Python") or \
         (player_choice == "Python" and computer_choice == "Cura") or \
         (player_choice == "Cura" and computer_choice == "Fusion"):
        print ( "泉水先生：うおおおおおおおああああああああ")
        print("　")
        print (player_choice, "を見た瞬間、石になってしまった。君の勝ちだ。")
    else:
        print("泉水先生：",player_choice,"こんなのじゃあ効かないぞ。出直してこい。")
        exit()
        
rock_paper_scissors()
print("　")
print("＊")
print("＊")
print("＊")
print("＊")
print("＊")
print("　")
print("お見事！単位ゲットだ！")
print("　")
print("またの挑戦を待っているよ！")
