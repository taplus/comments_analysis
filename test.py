'''没什么用的脚本'''
ori = r"D:\test\word.txt"
n = 1
f = open(ori,'r',encoding='utf-8')
fi = open(r'D:\test\word.tsv','w',encoding='utf-8')
for word in f.read().split():
    print(word)
    n += 1

    fi.write(str(word)+'\n')
f.close()
fi.close()

file = r"D:\test\word.tsv"

with open(file,'r',encoding='utf-8') as f:
    print(f.readlines())
print(n)