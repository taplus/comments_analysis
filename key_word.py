'''用 jieba 库进行中文分词，并提取关键词,生成图像'''
import jieba
import jieba.analyse
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

file = r"D:\GIT\comment_analysis\clean.txt"
stop_word = r"D:\GIT\comment_analysis\stopwords-master\baidu_stopwords.txt"

with open(file,'rb') as comments:
    # 设置停用词
    jieba.analyse.set_stop_words(stop_word)
    # 关键词抽取
    keywords = jieba.analyse.extract_tags(comments.read(), topK=15, withWeight=True)
    print(type(keywords))

    # for keyword,weight in keywords:
    #     print(keyword,weight)

    # 列表转dataframe
    df = pd.DataFrame(keywords)
    # print(type(df))
    print(df[0])

    # 设置画布大小
    plt.figure(figsize=(15,9))
    # 显示中文
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    # 画图
    plt.bar(df[0], df[1], color="c")
    # 设置标签，标题，调整大小
    # plt.xlabel('词语', fontsize=20)
    plt.ylabel('权重', fontsize=15)
    plt.title('关键词权重', fontsize=20)
    # 参考刻度线设置
    plt.tick_params(labelsize=10)
    # 在每个直条上加标签
    for word,value in zip(df[0], df[1]):
        print(word)
        plt.text(word, value, '%.2f' %value, ha='center', va='bottom', fontsize=10)
    plt.savefig('D:\\GIT\comment_analysis\\im\\keyword.png')
    plt.show()