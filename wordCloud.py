#%%
#encoding=utf-8
import matplotlib.pyplot as plt
from scipy.misc import imread
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from os import path
import pandas
import jieba
import jieba.analyse

# 构造词云生成类
class Cloud:
  def __init__(self, content, img_filepath, font_filepath):
    
    #使用结巴分词 
    tags = jieba.analyse.extract_tags(content, topK=200, withWeight=False)

    self.d = path.dirname(__name__)

    self.text = " ".join(tags)
    self.img = imread(img_filepath)
    self.wc = WordCloud(background_color="white", #背景颜色 
               max_words=2000,# 词云显示的最大词数
               mask=self.img,#设置背景图片
               font_path = font_filepath, #设置中文字体，使得词云可以显示（词云默认字体是“DroidSansMono.ttf字体库”，不支持中文） 
              #  stopwords=STOPWORDS.add("said"),
               max_font_size=38, #字体最大值
               random_state=42) #颜色种类
    self.wc.generate(self.text)

  #展示词云 
  def show_wc(self):
    img_color = ImageColorGenerator(self.img)
    plt.imshow(self.wc.recolor(color_func=img_color))
    plt.axis('off')
    plt.show()

  #保存词云
  def save_wc(self, out_file_name):
    self.wc.to_file(path.join(self.d, out_file_name))


#获取csv 中的评论
def readCsv(path, star):
  dataFrame = pandas.read_csv(path)
  comments = dataFrame[dataFrame['stars'] >= star]

  comemntsText = " "
  for index,row in comments.iterrows():
    comemntsText += str(row['content'])
  
  return comemntsText


if __name__ == '__main__':
  content = readCsv('comments.csv', 5)
  fo = open("text.txt", "w")
  fo.write(content)
  fo.close()

  #给词云配置内容,图片,字体（为了使中文字体不会乱码
  wc = Cloud(content, 'hunter.jpg', '宋体.ttc')
  wc.show_wc()
  wc.save_wc('world_cloud.png')


