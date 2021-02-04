'''中文分词，创建词频图'''
import jieba
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl


file = r"D:\GIT\comment_analysis\clean.txt"
cut_word = r'D:\GIT\comment_analysis\cut_word.txt'
stop_word = r"D:\GIT\comment_analysis\stopwords-master\baidu_stopwords.txt"


def jieba_word(stop_word,file,cut_word):
    '''执行中文分词'''
    with open(stop_word,'r',encoding='utf-8') as f:
        stop_words = f.read().split('\n')
        #stop_words = list(f.read())
        #print(stop_words)

    with open(file,'r',encoding = 'utf-8',errors='ignore') as f:
        dict = {}
        for line in f.readlines():
            print(line)
            cut_list = jieba.lcut(line,cut_all=False)
            
            for word in cut_list:
                if (word not in stop_words and len(word)>1):
                    dict[word] = dict.get(word,0) + 1

    result = list(dict.items())
    result.sort(key=lambda x:x[-1],reverse=True)
    return result

def write2txt(cut_word,result):
    '''将分词结果写到文件'''
    with open(cut_word,'w',encoding='utf-8') as fi:
        for item in result:
            key,value = item
            fi.write(str(key)+'\t'+str(value)+'\n')

def draw(stop_word,file,cut_word):
    '''创建分词前15词词频统计条形图'''
    result = jieba_word(stop_word,file,cut_word)
    df = pd.DataFrame(result)
    print(df)

    # 显示中文
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure(figsize=(15,9))
    plt.bar(df[0][0:15],df[1][0:15])
    plt.title('词频统计',fontsize=20)
    # plt.xlabel('词语',fontsize=12)
    plt.ylabel('频数',fontsize=15)
    # 参考线设置
    plt.tick_params(labelsize=10)
    # 加标注
    for word,value in zip(df[0][0:15], df[1][0:15]):
        plt.text(word, value, '%.0f' %value, ha='center', va='bottom', fontsize=10)

    plt.savefig('D:\\GIT\comment_analysis\\im\\frequence.png')
    plt.show()



def run():
    '''执行函数'''
    jieba_word(stop_word,file,cut_word)
    draw(stop_word,file,cut_word)

run()
