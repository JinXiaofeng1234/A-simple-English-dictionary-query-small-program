from requests import post as post
from pyttsx3 import init
from sys import exit
def baidu_translate(words):#请求网页
     post_url="https://fanyi.baidu.com/sug"
     #设置请求头
     headers={
         "User-Agent":"Mozilla/5.0"
     }



     data={
         "kw":words
     }

     resp=post(url=post_url,data=data,headers=headers)

     result=resp.json()

     #读取json串
     if len(result['data'])!=0:
          if len(result['data']) == 1:
               out=result['data'][0]['v']
          else:
               key_list=list(result['data'][1].keys())
               second_key=key_list[1]
               out=result['data'][1][second_key]
          return out
     else:
          print("请求的翻译没有结果")
          out=''
          return out
def add_string_list():
     new_word=str(input("请输入新单词:\n"))
     chinese_translation=str(input("请输入中文译名:\n"))
     english_agreement_word=str(input("请输入英文同意词,如果不知道，可以写None:\n"))
     string_ls=[new_word,chinese_translation,english_agreement_word]
     for i in string_ls:
          if len(i)==0:  
               print("请输入完整信息")
               add_string_list()
          else:
               return string_ls
def changed_string_list():
     string_dictionary={}
     order_changed_word=input("请输入要修改内容指向的单词")
     changed_chinese_mean=input("请输入你要修改的中文含义")
     changed_english_agreement_word=input("请输入英文同意词")
     string_dictionary[order_changed_word]=[changed_chinese_mean,changed_english_agreement_word]
     if len(order_changed_word)!=0:
          for i in string_dictionary[order_changed_word]:
               if len(i)==0:
                    print("请输入完整信息")
                    changed_string_list()
               else:
                    return string_dictionary
     else:
          print("无论怎样,字典键值不能为空,否则你怎么查字典")
          changed_string_list()
     
def save_dict_to_py(dictionary,filename):
     with open(filename,"w",encoding='utf-8') as f:
               f.write("MyDictionary="+str(dictionary))

def txt_add(Character_string):
     with open("牛津高阶英汉双解词典（第9版 同义词）115643条.txt", "a", encoding="UTF-8") as file:
          file.write("\n")
          file.write(str(Character_string))
      
def file_process():
     with open("牛津高阶英汉双解词典（第9版 同义词）115643条.txt", "r", encoding="UTF-8") as file:
         l=[i.strip() for i in file]
     dictionary={}
     for i in l:
          words=i.split(" ")
          for j in words:
               for k in j:
                    if '\u4e00' <= k <= '\u9fff':
                         if words.index(j)==1:
                              dictionary[words[0]]=[words[1],words[2:]]
                         else:
                              index=words.index(j)
                              tmp_s=' '.join(words[:index])
                              del words[:index]
                              words.insert(0,tmp_s)
                              dictionary[words[0]]=[words[1],words[2:]]
     return dictionary
def load_py():
     from output import MyDictionary
     dictionary=MyDictionary
     return dictionary
dictionary={}
if len(dictionary)==0:
     print("字典为空，请选择导入字典的源数据\n"
           "-0 从牛津词典导入"
           "-1 从json文件导入")
inputs=int(input("请输入:\n"))
if inputs==0:
     dictionary=file_process()
elif inputs==1:
     dictionary=load_py()
else:
     exit()

def voice_read(txt):
     engine=init()
     engine.setProperty('rate',120)
     engine.say(txt)
     engine.runAndWait()


while True:         
     word=input("请输入你要查询的单词:\n")
     if word=='q':
          print("退出前将导出字典")
          save_dict_to_py(dictionary, "output.py")
          break
     else:
          flag=False
          for key in  dictionary.keys():
              if key==word:
                   tmp_l=dictionary[word][1]
                   print(f"已找到单词,其中文译为:{dictionary[word][0]},英文同意词为:{tmp_l}")
                   flag=True
                   print("希望朗读这个单词吗?y/n")
                   ans=input()
                   if ans=='y':
                        print(word)
                        voice_read(word)
                   elif ans=='n':
                        pass
                   else:
                        pass
          if flag==False:
              print("未找到单词\n"
                    "请问你需要添加新的单词或词组吗?\n"
                    "-0 添加新的单词或词组"
                    "-1 不添加"
                    "-2 修改字典"
                    "-3 请求百度翻译")
              ans=str(input())
              if ans=="0":
                   string_ls=add_string_list()
                   Character_string=f"{string_ls[0]} {string_ls[1]} {string_ls[2]}"
                   txt_add(Character_string)
                   dictionary[string_ls[0]]=[string_ls[1],string_ls[2]]
              elif ans=="1":
                   pass
              elif ans=="2":
                   string_dictionary=changed_string_list()
                   key,values=list(string_dictionary.items())[0]
                   Character_string=key+' '+' '.join(map(str,values))
                   txt_add(Character_string)
                   dictionary[key]=values
                   


                        
              elif ans=='3':
                   words=''
                   while len(words)==0:
                        words = input("请输入要翻译的内容:\n")
                        if words=='q':
                             pass
                        elif words!='q':
                             if len(words)!=0:
                                  result=baidu_translate(words)
                                  if len(result)!=0:
                                       print(result)
                                       dictionary[words]=[result,"None"]
                                       Character_string=f"{words} {result} None"
                                       txt_add(Character_string)
                                  else:
                                       print("请求无结果")
                             else:
                                  print("请输入一个单词")

              else:
                   print("请不要输入其它内容")

                             
                   

                   
              
    
        

