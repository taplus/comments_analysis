'''生成词云图'''
from wordcloud import WordCloud,ImageColorGenerator
import jieba
import numpy as np
'''创建词云图'''
import matplotlib.pyplot as plt
from imageio import imread

mask_path = r"D:\GIT\comment_analysis\im\fianl.png"
text = r"D:\GIT\comment_analysis\clean.txt"
stop_word = r"D:\GIT\comment_analysis\stopwords-master\baidu_stopwords.txt"

def jieba_processig(stop_word,text):
    '''jieba分词'''
    with open(stop_word,'r',encoding='utf-8',errors='ignore') as f:
        stop_words = f.read().splitlines()

    with open(text,'r',encoding = 'utf-8') as fi:

        jieba.add_word('细思极恐')
        jieba.add_word('快银')
        cut_str = '/'.join(jieba.cut(fi.read(),cut_all=False))

    cut_word = []
    for word in cut_str.split('/'):
        if word not in stop_words and len(word)>1:
            cut_word.append(word)
        
    return ' '.join(cut_word)
    
back_coloring = imread(mask_path)

wc = WordCloud(background_color='white',
                scale=5,
                max_words=600,
                mask=back_coloring,
                stopwords=stop_word,
                font_path= r'C:/Windows/Fonts/simfang.ttf',  # 设置中文字体
                max_font_size=60,  # 设置字体最大值
                random_state=30,  # 设置有多少种随机生成状态，即有多少种配色方案
                width=600,
                height=800).generate(jieba_processig(stop_word,text))

# 从背景图片生成颜色值
image_colors = ImageColorGenerator(back_coloring)

# 生成图片
plt.figure()
plt.imshow(wc.recolor(color_func=image_colors))
plt.axis('off')
# plt.savefig(r'D:\GIT\comment_analysis\im\wordcloud.png')
wc.to_file(r'D:\GIT\comment_analysis\im\wordcloud.png')
plt.show()
