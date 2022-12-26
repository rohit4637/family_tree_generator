from flask import Flask,request,Response
from flask_pymongo import pymongo
from pandas import DataFrame
#from flask_cors import CORS,cross_origin
from flask import jsonify
from flask import send_file
from treelib import Node, Tree
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)
# app.config['CORS_HEADERS'] = 'Content-Type'
# CORS(app)

CONNECTION_STRING=os.environ.get('MONGO')
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('test')

def family(name,voter_id,df):
    relation={}
    index=df[df['voter_id']==voter_id].index
    house=df.iloc[index[0]]['house_number']
    if(df.iloc[index[0]]['sex']=='FEMALE'):
       relation['father']=df.iloc[index[0]]['father/husband']
    else:
       relation['father']=df.iloc[index[0]]['father/husband']
    temp=df[(df['father/husband']==name)&(df['house_number']==house)]
    list_1=[]
    list_2=[]
    for index, row in temp.iterrows():
      if(row['sex']=='FEMALE'):
         list_1.append(row['name'])
      elif(row['sex']=='MALE'):
         list_2.append(row['name'])
    relation['wife/daughter']=list_1
    relation['son']=list_2 
    house_members=df[df.house_number==house].name.unique()
    family_members=[x for x in house_members if x.split(' ')[-1]==name.split(' ')[-1]]
    return relation,family_members 

@app.route("/")
def home():
    return ("Hello") 

@app.route("/fetch_family",methods=["GET","POST"])
def fetch_family():
    if request.method=="POST":
        request_data=request.get_json()
        voter_id=request_data['voter_id']
        name=request_data['name']
        father=request_data['father/husband']
        state=request_data['state']
        age=request_data['age']
        coll = pymongo.collection.Collection(db,state)
        df = DataFrame(list(coll.find()))
        try:
          relation,family_members=family(name,voter_id,df)
        except:
          return("Data not found") 
        tree = Tree()
        tree.create_node(relation['father'],relation['father'])  # No parent means its the root node
        tree.create_node(name,name,parent=relation['father'])
        for i in relation['son']:
         if(len(i)>0):
           tree.create_node(i,i,parent=name)
        for i in relation['wife/daughter']:
         if(len(i)>0):
          tree.create_node(i,i,parent=name)
        open('tree.txt', 'w').close()  
        tree.save2file('tree.txt')  
#         return(jsonify(f'{relation}',f'{family_members}'))
        return send_file('tree.txt')


if __name__=="__main__":
  app.run(debug=True)
