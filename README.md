# Python 练手 —— 豆瓣短评爬虫、词云、数据整理

## 环境

``` python
import requests # 爬取网页
from bs4 import BeautifulSoup # 清洗网页
import jieba # 中文分词
import matplotlib.pyplot as plt # 绘图
from wordcloud import WordCloud,ImageColorGenerator # 创建词云
from gensim.models import Word2Vec # 分词结果向量化
```
----
## 流程图

<img src="https://github.com/Taplus/comments_analysis/blob/main/im/2.png" alt="流程图" style="zoom:67%;" />
----
## 源码，只展示了核心代码，每个脚本都是独立的

- 豆瓣内容爬取，如下爬取豆瓣电影短评前十页的内容（未登录限制只能获取前十页内容，总计九千多字）
  ```python
  import requests
  from bs4 import BeautifulSoup
  
  def Request(url):
      '''抓取网页'''
      headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.56'}#'accept-encoding':'utf-8'}
  
      try:
          r = requests.get(url,headers=headers,timeout=15)
          # print(r.encoding)
          # print(r.apparent_encoding)
          #r.encoding=r.apparent_encoding
          encoding = 'utf-8'
          return r.text
      except Exception as e:
          print(e)
          print('error')
          print(requests.get(url).status_code)
          #print(requests.raise_for_status())
          return False
          
  
  def read_page(url):
      '''获取HTML'''
      if Request(url) != False:
          soup = BeautifulSoup(Request(url),'html.parser')
          page_content = soup.find_all('span',class_='short')
          return page_content
      
  def write2txt(url,page):
      '''写入到文本文件中'''
      file = r"D:\GIT\comment_analysis\WandaVision.txt"
      with open(file,'a+',encoding = 'utf-8') as f:
  
          f.write(str(read_page(url)))
  
  def main():
      '''在未登录状态下，豆瓣短评只能爬前十页'''
      page = 1
      for start in range(0,201,20):
          url = 'https://movie.douban.com/subject/30331433/comments?start='+str(start)+'&limit=20&status=P&sort=new_score'
          write2txt(url,page)
          page += 1
      print(page)
  
  if __name__ == '__main__':
      main()
  ```

- 文本内容清洗，只保留中文字符

  ```python
  with open(file,'r',encoding='utf-8') as f:
      # 正则匹配，懒惰匹配中间内容,
      # 使用re.S参数以后，正则表达式会将这个字符串作为一个整体，将“\n”当做一个普通的字符加入到这个字符串中，在整体中进行匹配
      content = re.findall('<span class="short">(.*?)</span>', f.read(), re.S)
      with open(clean,'w',encoding='utf-8') as fi:
          for item in content:
              print(item)
              # item.strip('\n')
              # item.replace('\n','')
              pattern = re.compile('[^\u4e00-\u9fa5]')
              # jieba 似乎不能实现英文分词，还是只保留中文字符算了
              item = pattern.sub('',item)
              fi.write(item)
  ```

- 使用 jieba 进行中文分词，写入文件，同时创建词频图

  ```python
  '''中文分词，创建词频图'''
  import jieba
  import pandas as pd
  import matplotlib.pyplot as plt
  import matplotlib as mpl
  
  
  file = "clean.txt" # 清洗好的文本
  cut_word = 'cut_word.txt' # 输出文本
  stop_word = "baidu_stopwords.txt" # 停用词文本
  
  
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
              cut_list = jieba.lcut(line,cut_all=False) # 返回列表
              
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
  
      plt.savefig('') # 保存路径
      plt.show()
  
  
  
  def run():
      '''执行函数'''
      jieba_word(stop_word,file,cut_word)
      draw(stop_word,file,cut_word)
  
  run()
  
  ```

- 使用 jieba 获取文本关键词，并创建权重图

  ```python
  '''用 jieba 库进行中文分词，并提取关键词,生成图像'''
  import jieba
  import jieba.analyse
  import pandas as pd
  import matplotlib.pyplot as plt
  import matplotlib as mpl
  
  file = '' # 清洗好的文本
  stop_word = '' # 停用词文本
  
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
      plt.savefig('') # 图片输出路径
      plt.show()
  ```

- 创建词云图

  ```python
  '''生成词云图'''
  from wordcloud import WordCloud,ImageColorGenerator
  import jieba
  import numpy as np
  import matplotlib.pyplot as plt
  from imageio import imread
  
  mask_path = '' # 掩膜路径
  text = '' # 清洗好的文本
  stop_word = '' # 停用词文本
  
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
  wc.to_file('') # 设置词云输出路径
  plt.show()
  
  ```

  

2. 尝试使用 Word2Vec 统计分词的词向量 
- 创建词向量.tsv文件
   ```python
   '''分词向量化'''
   import jieba
   import gensim
   from gensim.models import Word2Vec
   from gensim.models.word2vec import LineSentence
   
   text = '' # 清洗好的文本
   stop_word = ''
   vec = '' # 输出路径
   
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
       infile = open(vec,'r',encoding='utf-8') #分词好的文件
       sentence = LineSentence(infile)# 按'\t’读取
       dimention=100 #词向量维数
       model = gensim.models.Word2Vec(sentence, sg=0,size=dimention, min_count=0, window=5)#训练词向量
       model.wv.save_word2vec_format(r'', binary=False)
       infile.close()
       print('Finished!')
   
   if __name__=='__main__':
       word_vec(vec)
   ```

- 词向量可视化，打开 https://projector.tensorflow.org/ ，加载向量文件和标签即可生成可视化图像

   <img src="https://github.com/Taplus/comments_analysis/blob/main/im/1.png" style="zoom:60%;" />

------

## 结果展示
- 词频统计图

  <img src="https://github.com/Taplus/comments_analysis/blob/main/im/frequence.png" alt="词频统计" style="zoom:60%;" />

- 关键词权重图

  <img src="https://github.com/Taplus/comments_analysis/blob/main/im/keyword.png" alt="关键词" style="zoom:60%;" />

- 词云图

  <img src="https://github.com/Taplus/comments_analysis/blob/main/im/wordcloud.png" alt="词云" style="zoom:30%;" />

- 词向量可视化

  <img src="https://github.com/Taplus/comments_analysis/blob/main/im/3.png" alt="null" style="zoom:90%;" />

  - 功夫不到家，生成的可视化数据一团糟~~~

----

## 参考

1. [[超详细\] Python3爬取豆瓣影评、去停用词、词云图、评论关键词绘图处理]: https://blog.csdn.net/qq_41815243/article/details/91693368
