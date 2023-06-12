import requests
import json
import asyncio

async def get_status(time):
    try:
        r = requests.get(f"https://russianwarship.rip/api/v2{time}")
        data = r.json()
        return data
    except Exception as ex:
        print(ex)        
        
async def get_icon():
    try:
        r = requests.get(f"https://russianwarship.rip/api/v2/terms/en")
        data = r.json()
        return data
    except Exception as ex:
        print(ex)  
        
async def get_name_uk():
    try:
        with open('name_uk.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except Exception as ex:
        print(ex)  
        
async def preob(data, name):
    list=[]
    for key, val in data.items():
        if key != 'resource' and key != 'war_status'and key != 'increase':
            if type(val) is dict:
                for key1, val1 in val.items():
                   list.append([name[key1], f'{val1} (+{data["increase"][key1]})']) 
            else:
                list.append([name[key], val])
    return list

async def send_api(time_type):
    name = await get_name_uk()
    icons = await get_icon()
    data = await get_status(time_type)
    if 'errors' in data.keys():
        return 'Вы написали дату, в которой не было войны или эта дата в будущем. Напишите, пожалуйста, другую дату.'
    else:
        preob_data = await preob(data['data'], name)
        return preob_data
    
async def send_bot(data):
    headers = data[0]
    rows = data[1:]
    
    table = " | ".join(headers) + "\n"
    table += "|".join(["---"] * len(headers)) + "\n"
    
    for row in rows:
        table += " | ".join(str(cell) for cell in row) + "\n"
    
    return table
    
async def main():
    rend = await send_api('/statistics/2023-04-12')
    table = await send_bot(rend)
    print(table)

if __name__ == '__main__':
    asyncio.run(main())
