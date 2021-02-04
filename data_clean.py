'''文本内容清洗'''
import re

file = r"D:\GIT\comment_analysis\WandaVision.txt"
clean = r"D:\GIT\comment_analysis\\clean.txt"

def test1(file,test):
    '''或许提取所有中文字符，简单粗暴'''
    with open(file,'r',encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip('\n')
            pattern = re.compile('[^\u4e00-\u9fa5]')
            line = pattern.sub('',line)
            with open(test,'a+',encoding='utf-8') as fi:
                fi.write(line)

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

