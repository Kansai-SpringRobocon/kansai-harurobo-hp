##############################################################
# 【参考】
# https:/note.nkmk.me/python-glob-usage/
# https:/qiita.com/Yuu94/items/9ffdfcb2c26d6b33792e
# https:/note.nkmk.me/python-split-rsplit-splitlines-re/
# Pythonで文字画像を作る
# http:/kamiya.tech/blog/draw-font/
# PIL（Python Imaging Library）を使って画像ファイルを作成する。(Qiita)
# https:/qiita.com/suto3/items/5181b4a3b9ebc206f579
# 同一要素の削除
# https:/ja.stackoverflow.com/questions/21070/Pythonで1次元のリストを比較し-同一の要素の削除について
# Pythonでの文字列抽出
# https:/note.nkmk.me/python-str-extract/

# Author : Hideto Niwa
##############################################################

from PIL import Image, ImageDraw, ImageFont
import unicodedata
import glob
import os

height = 400
horizontal = 764

#カード作成を無視するファイルリスト
ignore_list = {}

# 文字数取得（全角2文字、半角1文字）
# 参考：https://note.nkmk.me/python-unicodedata-east-asian-width-count/
def get_east_asian_width_count(text):
    count = 0
    for c in text:
        if unicodedata.east_asian_width(c) in 'FWA':
            count += 2
        else:
            count += 1
    return count

# 記事タイトル取得
def get_title(file_path):
    print("Open file...", file_path)

    f = open(file_path, 'r', encoding="utf-8")  # File Open（文字コード指定）
    datalist = f.readlines()
    f.close()
    title_string = "title = "

    for i in range(len(datalist)):
        text = datalist[i]
        title = text.split('"')
        if title[0] == title_string:
            break
    print(title)
    return title[1]

# ディレクトリ取得
def get_dir(path):
    file_list = glob.glob(path, recursive=True)
    file_list = list(filter(lambda x: x not in ignore_list, file_list))
    return file_list

# 文字未入れ状態の画像作成
def make_base_image(logo_path, img_path):
    tmp = Image.new('RGB', (horizontal, height),
                    (0xFF, 0xFF, 0xFF))  # dummy for get text_size
    print("output dir : ",img_path)
    logo = Image.open(logo_path)

    save_img = tmp.copy()
    save_img.paste(logo)
    os.makedirs(os.path.dirname(img_path), exist_ok=True)
    save_img.save(img_path)

# 文字入れ部分
def make_image(font_path, img_path, text, x=0.0, y=0.0, font_size=32, font_color="black"):
    font = ImageFont.truetype(font_path, font_size)
    img = Image.open(img_path)

    img_d = ImageDraw.Draw(img)
    text_size = img_d.textsize(text, font)  # テキストサイズの取得

    img_d.text((x-(text_size[0]/2), y-(text_size[1]/2)),
               text, fill=font_color, font=font)
    img.save(img_path)

def add_card_info(file_path,card_path):
    f = open(file_path, 'r', encoding="utf-8")  # File Open（文字コード指定）
    datalist = f.readlines()
    f.close()

    card_path = card_path[13:]
    img_string = "card_image = "
    section_string = "+++"

    start_formatter = False
    img_info = False

    for i in range(len(datalist)):
        text = datalist[i][:14]
        if img_string in text:
            img_info = True
            break
        text = text[:3]
        if text == section_string:
            if start_formatter:
                break
            else:
                start_formatter=True
    
    card_info = img_string + " " + '"img/'+card_path+'"\n'
    if img_info:
        datalist[i]=card_info
    else:
        datalist.insert(2,card_info)

    f = open(file_path, 'w', encoding="utf-8")  # File Open（文字コード指定）
    f.writelines(datalist)
    f.close()
    return text

file_list = get_dir('./content/**/*.md')
# for 
print(file_list)

for i in file_list:
    title = get_title(i)
    save_pic_filename=i[9:]
    save_pic_filename=save_pic_filename[:-3]
    #print(save_pic_filename)

    save_pic_dir='./static/img/card'+save_pic_filename+'.png'

    #print(save_pic_dir)

    font = "./static/mplus-2p-regular.ttf"
    
    make_base_image("./static/img/logo.jpg", save_pic_dir)
    make_image(font ,save_pic_dir, "春ロボコン(関西)",horizontal*0.75, height*0.4,42)

    if get_east_asian_width_count(title)>24:
        make_image(font ,save_pic_dir, title,horizontal*0.75, height*0.53,18)
    else:
        make_image(font ,save_pic_dir, title,horizontal*0.75, height*0.53,34)

    make_image(font , save_pic_dir, "https://関西春ロボコン.com",horizontal*0.75, height*0.64,18)
    add_card_info(i,save_pic_dir)
    print()