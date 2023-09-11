import json
import sys

if __name__=="__main__":
    path=sys.argv[1]
    print(path)
    with open(path,'r') as file:
        data = json.load(file)
        # data['status']=1
    print(data)
    data['status']=1
    with open(path,'w') as outfile:
        json.dump(data, outfile)
    print(data)


