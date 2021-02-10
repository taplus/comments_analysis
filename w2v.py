'''分词向量化'''
import jieba
import gensim
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

text = r"D:\GIT\comment_analysis\clean.txt"
stop_word = r"D:\GIT\comment_analysis\stopwords-master\baidu_stopwords.txt"
vec = r'D:\GIT\comment_analysis\vec.txt'

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


def write2txt(vec):
    with open(vec,'w',encoding='utf-8') as f:
        f.write(jieba_processig(stop_word,text))


def word_vec(vec):
    infile = open(r"",'r',encoding='utf-8') #分词好的文件
    sentence = LineSentence(infile)# 按'\t’读取
    dimention=102 #词向量维数
    model = gensim.models.Word2Vec(sentence, sg=0,size=dimention, min_count=0, window=5)#训练词向量
    model.wv.save_word2vec_format(r'', binary=False)
    infile.close()
    print('Finished!')

if __name__=='__main__':
    word_vec(vec)