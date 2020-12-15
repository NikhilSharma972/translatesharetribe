import ruamel.yaml as yml  
import codecs
import json
import csv 


translate_obj = []
translated_csv = []

yaml = yml.YAML(typ='safe')
yaml.allow_duplicate_keys = True

def build_value(v):
    st = ""
    wordss = v.split(" ") 
    for word in wordss:
        if '%{' in word:
            st = st + "@@@@@@" + " "
        else:
            st = st + word + " "
    st = st.replace('"',r"'")
    return st

def charscore(k):
    score = 0
    for c in k:
        score = score + ord(c) 
    return score 


def replace_special_chars(v,tvv):
     v = v.split(" ")
     values = list(filter(lambda x: ('%' in  x ),v)) 
     st = ""
     tvv = tvv.split(" ") 
     ind = 0
     for i in tvv:
         if i == "@@@@@@":
             st = st + values[ind] 
             ind = ind + 1  
         else: 
             st = st + i
         st = st + " "
     return st  



def find_replacement(k,v):
    for i in translated_csv:
        tk,tv,tvv = i
        if tk == k and charscore(tv) == charscore(v):
            return tvv

    return 0

def iterdict(d):
    for k,v in d.items():
        if isinstance(v, dict):
            iterdict(v)
        elif isinstance(v, str): 
            replace_with = find_replacement(k,build_value(v)) 
            if replace_with != 0:
                replace_ment = replace_special_chars(v,replace_with) 
                d[k] = replace_ment.strip()
            else:
                print("no replacement found for: ",k, "and ", v) 


with open('final.csv', 'r') as csvfile:
    csv_reader = csv.reader(csvfile)
    for line in csv_reader:
        translated_csv.append(line)


with open("en_main.yml") as file:
    data = yaml.load(file)
    
    

iterdict(data) 

with open('data_new.yml', 'w') as fp:
    yml.dump(data, stream=fp, allow_unicode=True,default_flow_style=False,width=float("inf"))






    