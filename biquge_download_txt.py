import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from tqdm import tqdm
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
}
def clean(contents):
    result = contents
    keywords = ["记住网址m.ｍｉａｏｓｈｕｗｕ．ｃｃ",
                           "一秒记住ｈｔｔｐs：//ｍ．miaoｓｈｕｗｕ．ｃc",
                           "https：//www.miaoshuwu.cc/最快更新！无广告！",
                           "首发网址ｈｔｔps://m.miaoshuｗｕ.ｃｃ",
                           "天才一秒记住本站地址：[秒书屋]",
                           "https://www.miaoshuwu.cc/最快更新！无广告！",
                           "一秒记住ｈｔｔｐs://ｍ．miaoｓｈｕｗｕ．ｃc",
                           "v,i,p完整章节请访问www.kshu08.com",
                           "@本站开始更新这本书，@喜欢看本书的读友请添加收藏哦O(∩_∩)O~w.w.w.kshu08.c.o.m！！"]
    for each in keywords:
        result = result.replace(each,'')
    return result

def getcontent(url):
    response = requests.get(url,headers=headers)
    response.encoding = response.apparent_encoding
    content_soup = BeautifulSoup(response.text, "lxml")
    # content_soup.find('div',id='content')
    # p_list = content_soup.find('div',id='content').find_all('p')
    content = content_soup.find('div',id='content').text
    if(content.find('本章未完，点击下一页继续阅读')>0):
        # 说明有第二页内容 拼接URL获取第二页
        tmp_url = url[:-5]+'_2.html'
        response = requests.get(tmp_url,headers=headers)
        response.encoding = response.apparent_encoding
        content_soup2 = BeautifulSoup(response.text, "lxml")
        content2 = content_soup2.find('div',id='content').text
        content = content + '\n' + content2
        content = content.replace('-->>本章未完，点击下一页继续阅读','')
    content = "\n".join(content.split())
    #净化
    content = clean(content)
    return content

if __name__ == "__main__":
    allcontent=''
    url = str(input("请输入小说目录下载地址:\n"))
    response=requests.get(url)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, "lxml")
    info = soup.find('h1').text.strip()
    dd_list = soup.find_all('dd')
    print('小说:%s' % info ) 
    for each in tqdm(dd_list):
        url2 = each.find('a').get('href')
        #text =  each.text.strip().replace('h','第',1).replace('【求全订阅月票】','').replace('【求订阅】','').replace(' ','章 ',1).replace('（补更）','').replace('【求全订阅】','').replace('【求全订阅！】','').replace('（求月票）','').replace('（求月票！）','')
        text =  each.text.strip().replace('【求全订阅月票】','').replace('【求订阅】','').replace('（补更）','').replace('【求全订阅】','').replace('【求全订阅！】','').replace('（求月票）','').replace('（求月票！）','')
        #print(text)
        parse = urlparse(url)
        tra=url
        if(url2[0] == "/"):
            tra=parse.scheme+"://"+parse.netloc
        #print (tra + url2)
        thiscontent = text +'\n' + getcontent(tra + url2)
        allcontent = allcontent + '\n' + thiscontent + '\n'
    filename = '%s.txt' % info
    allcontent = info +'\n'+ allcontent
    #统一换行符
    eachline = allcontent.split('\n')
    allcontent2 = ''
    i=0
    for each in eachline:
        each.replace('\r\n','\n').replace('\r','\n')
        if(i == 0):
            allcontent2 = each
        else:
            allcontent2 = allcontent2 + '\n' + each
        i +=1
    with open(filename, 'w',encoding='utf-8') as file_object:
        file_object.write(allcontent2)