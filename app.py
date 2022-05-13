import os, requests, json
from dotenv import load_dotenv

load_dotenv()

#Get token and database id from .env
tokenNotion = os.getenv('TOKEN_NOTION')
database = os.getenv('DATABASE')

#Variables
count = 0

#Function makes a request to get a listed the AHU's without filters we only get the last 100 AHU's
def listUnits(tokenNotion, database):

    url = f"https://api.notion.com/v1/databases/{database}/query"

    headers = {
        'Notion-Version': '2021-05-13',
        'Authorization': tokenNotion,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers)

    return response.text

def listToDo(tokenNotion, id):
    
    url = f"https://api.notion.com/v1/blocks/{id}/children?page_size=100"

    payload = {}
    headers = {
        'Notion-Version': '2021-05-13',
        'Authorization': tokenNotion
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.text

listResponse = listUnits(tokenNotion= tokenNotion, database= database)
jsonResponse = json.loads(listResponse)

for data in jsonResponse['results']:
    jsonId = data['id']
    jsonDate = data["created_time"]
    date2 = jsonDate.split("T")[0].split("-")
    dateFinal = "/".join(reversed(date2))
        
    jsonProperties = data['properties']
    jsonOrder = jsonProperties['Pedido']
    jsonOrderTitle = jsonOrder['title']
    for data in jsonOrderTitle:
        dataOrderText = data['text']
        dataOrder = dataOrderText['content']
                
    jsonModel = jsonProperties['Modelo']
    jsonModel_rich_text = jsonModel['rich_text']
    for dataModel in jsonModel_rich_text:
        dataModelAHU = dataModel['plain_text']
    
    count = count + 1
        
    print(f'''<<<<< Order: {dataOrder} >> Model: {dataModelAHU} >> Date: {dateFinal} >>>>>''')
    
    todoList = listToDo(tokenNotion=tokenNotion, id=jsonId)
    todoListJson = json.loads(todoList)
    
    for dataList in todoListJson['results']:
        dataToDo = dataList['to_do']
        dataText = dataToDo['text'][0]
        dataText2 = dataText['text']
        dataContent = dataText2['content']
        print(f'    [] {dataContent}')
        
    
    



