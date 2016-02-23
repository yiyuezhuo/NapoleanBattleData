# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 13:38:04 2015

@author: yiyuezhuo
"""

import re
import urllib
from bs4 import BeautifulSoup
import bs4
import os
import csv



#这里爬爬wiki百科的拿破仑战役词条的内容，获取各战役的信息。主要统计战役损失与战役投入的关系。
f=open('data.txt','r')
s=f.read()
f.close()
record=re.findall(r'href=".+"',s)
url=[]
namel=[]
for string in record:
    url.append(re.search(r'href="(.+?)"',string).groups()[0])
    namel.append(re.search(r'title="(.+?)"',string).groups()[0])
    
def download(p=0):
    #注意按这种方法会把滑铁卢漏掉，待会要手动加进去
    for i in range(p,len(url)):
        a=urllib.urlopen(url[i])
        html=a.read()
        f=open(namel[i],'wb')
        f.write(html)
        f.close()
        print i
        
class Attr(object):
    def __init__(self,name,soup):
        self.name=name
        self.soup=soup
        self.value=None
    def get(self):
        return self.value
    def take(self):
        pass
    
def get_right(soup,name):
    th=soup.find(name='th',text=name)
    ss=[i for i in th.next_siblings if i>1]
    s=ss[1].text
    return s
    
def jump2(soup,name):
    th=soup.find(name='th',text=name)
    tr=th.parent
    trs=tr.next_siblings
    trss=[i for i in trs if SBcheck(i)]
    #print trss
    return trss[0]

def jump(soup,name):
    r=jump2(soup,name)
    rs=[i for i in r.children if SBcheck(i)]
    return rs
  
def SBcheck(obj):
    return not(isinstance(obj,bs4.element.NavigableString))
  
def Press(name):
    def _func(func):
        def ff(self):
            try:
                func(self)
            except:
                print name,'BUG!'
        return ff
    return _func
        
class Wiki(object):
    def __init__(self):
        self.credit=True
        self.value={'Name':None,'Part':None,'Date':None,'Location':None,'Result':None,
                    'BelligerentsA':None,'BelligerentsB':None,'CommanderA':None,'CommanderB':None,
                    'StrengthA':None,'StrengthB':None,'LossA':None,'LossB':None}
    def setup_html(self,html):
        self.html=html
        self.soup= BeautifulSoup(self.html)
    def rel(self,tag):
        #print tag
        try:
            tag.sup.extract()
        except:
            pass
        s=''
        for i in tag.strings:
            s=s+i
        return s
    def draw_number(self,s):
        #print '---------'
        #print s
        ss=s.replace(',','')
        ssl=re.findall(r'\d+',ss)
        nl=[int(i) for i in ssl]
        return nl
    def draw_number_max(self,s):
        l=self.draw_number(s)
        if len(l)>0:
            return max(l)
        else:
            self.credit=False
            return 1
    def draw_number_max_list(self,sl):
        return [self.draw_number_max(s) for s in sl]
    def setup_max(self):
        self.A11m,self.A12m,self.A21m,self.A22m=self.draw_number_max_list([self.A11,self.A12,self.A21,self.A22])
        self.odds_s=float(self.A11m)/self.A12m
        self.odds_l=float(self.A21m)/self.A22m
        self.loss_percent=(self.A21m+self.A22m)/float(self.A11m+self.A12m)
    def setup_load(self,name):
        f=open(name,'rb')
        s=f.read()
        f.close()
        self.setup_html(s)
    def is_bs_str(self,obj):
        p=str(type(obj))=="<class 'bs4.element.NavigableString'>"
        #print str(type(obj))
        #print p
        return p
    def setup_name(self,name):
        self.setup_load(name)
        soup=self.soup
        try:
            th=soup.find(name='th',text='Strength')
            tr=th.parent
            trs=tr.next_siblings
            trss=[i for i in trs if len(i)>1]
            if len(trss)!=3:
                print 'bug'
            tr1,tr2=trss[0],trss[2]
            #trr1=[i for i in tr1 if len(i)>1]
            #trr2=[i for i in tr2 if len(i)>1] not(self.is_bs_str(i))
            trr1=[i for i in tr1 if not(self.is_bs_str(i))]
            trr2=[i for i in tr2 if not(self.is_bs_str(i))]
            A11,A12=trr1
            A21,A22=trr2
            A11,A12,A21,A22=self.rel(A11),self.rel(A12),self.rel(A21),self.rel(A22)
            self.A11,self.A12,self.A21,self.A22=A11,A12,A21,A22
            self.setup_max()
        except:
            pass#因为主要不调用这个暂时能运行运行不运行拉倒
    def take(self):#狗血的解耦方法，为了分块处理信息
        self.take_Summary()
        self.take_Summary2()
        self.take_Belligerents()
        self.take_Commanders()
        self.take_Strength()
        self.take_Loss()
    @Press('Summary')
    def take_Summary(self):
        soup=self.soup
        th=soup.find(name='th',attrs={'class':'summary'})
        self.value['Name']=th.text
        tr=th.parent
        trs=tr.next_siblings
        l=[i for i in trs if SBcheck(i)]
        self.value['Part']=l[0].text
    @Press('Summary2')
    def take_Summary2(self):
        soup=self.soup
        self.value['Date']=get_right(soup,'Date')
        span=soup.find(name='span',attrs={'class':'location'})
        self.value['Location']=span.text
        self.value['Result']=get_right(soup,'Result')
    @Press('take_Belligerents')
    def take_Belligerents(self):
        soup=self.soup
        ths=jump(soup,'Belligerents')
        self.value['BelligerentsA']=ths[0].text
        self.value['BelligerentsB']=ths[1].text
    @Press('Commanders')
    def take_Commanders(self):
        soup=self.soup
        ths=jump(soup,'Commanders and leaders')
        self.value['CommanderA']=ths[0].text
        self.value['CommanderB']=ths[1].text  
    @Press('Strength')
    def take_Strength(self):
        soup=self.soup
        ths=jump(soup,'Strength')
        self.value['StrengthA']=ths[0].text
        self.value['StrengthB']=ths[1].text   
    @Press('Loss')
    def take_Loss(self):
        soup=self.soup
        ths=jump(soup,'Casualties and losses')
        self.value['LossA']=ths[0].text
        self.value['LossB']=ths[1].text   
    def display(self):
        print self.A11,self.A12
        print self.A21,self.A22
        print '--'
        print self.A11m,self.A12m
        print self.A21m,self.A22m
        print self.odds_s,self.odds_l
    def setup_id(self,ids):
        self.setup_name(namel[ids])
    def get(self,label_list):
        l=[]
        for label in label_list:
            l.append(self.value[label])
        return l
    
post=Wiki()
post.setup_name('battle\\'+'Battle of Ligny')
soup=post.soup
post.display()
post.take()
print post.value
'''
wikil=[]
WIKIL=True
if WIKIL:
    for name in namel:
        
        print name
        try:
            obj=Wiki()
            obj.setup_name('battle\\'+name)
            wikil.append(obj)
        except:
            wikil.append(None)
            print 'fail'
            
    print 'success percent',1-float(wikil.count(None))/len(wikil)
wikill=[i for i in wikil if i!=None]
wikis=[i for i in wikill if i.credit!=False]
print 'credit percent:',float(len(wikis))/len(wikil)
def dec(wiki):
    return min([wiki.A11m,wiki.A12m])

wikia=[i for i in wikis if dec(i)>1000]
print 'army percent:',float(len(wikia))/len(wikil)
'''
wikil=os.listdir('battle')
obj_l=[]
for wiki in wikil:
    print wiki
    obj=Wiki()
    obj.setup_name('battle\\'+wiki)
    obj.take()
    obj_l.append(obj)

labels=['Name','Part','Location','Date','Result','BelligerentsA','BelligerentsB','CommanderA','CommanderB','StrengthA','StrengthB','LossA','LossB']

sl=[[s.encode('utf8') if s!=None else None for s in obj.get(labels)] for obj in obj_l]
f=open('NaD.csv','wb')
writer=csv.writer(f)
writer.writerow(labels)
writer.writerows(sl)
f.close()
'''在wiki表格中各个人名的出现次数，缪拉怒刷存在感（主要是那个那不勒斯王国是怎么被吊打的战绩），达武并没有什么卵用
Napoleon I 37
Michel Ney 24
Joachim Murat 21
Davout 8

Wellington 17
回归，处理变异性之精细结构者也。然众多结构，唯使其化为一特定结构，any合理性乎？
'''