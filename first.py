import ruamel.yaml
import json
import csv 

translate_obj = []

def iterdict(d):
    for k,v in d.items():
        if isinstance(v, dict):
            iterdict(v)
        elif isinstance(v, str):
            translate_obj.append({k: v})


def build_value(v):
    st = ""
    wordss = v.split(" ") 
    for word in wordss:
        if '%{' in word:
            st = st + "@@@@@@" + " "
        else:
            st = st + word + " "
    st = st.replace('"',r"'")
    return '"' + st + '"'



def write2csv(data):
    data_file = open('data_file_n.csv', 'w') 
    for datum in data:
        for k,v in datum.items():
            if k == "label_placeholder":
                print("the keys is",k , " the buld value is : ", build_value(v))
            s = k + "," + build_value(v) + "\n"
            data_file.write(s)
    data_file.close() 

            


yaml = ruamel.yaml.YAML(typ='safe')
yaml.allow_duplicate_keys = True

with open("en_main.yml") as file:
    data = yaml.load(file)
    print(type(data))
    iterdict(data)
    write2csv(translate_obj)