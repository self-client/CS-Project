import mysql.connector
import json
import pandas 

#with mysql.connector.connect(host=hostname,user=user,passwd=password,database=database) as f:


with open('C:\\Users\\Pratham\\Desktop\\Projetcs\\cs project\\config.json','r') as f:
    config=json.load(f)
hostname=config.get("hostname")
user=config.get("user")
password=config.get("password")
database=config.get("database")

def show_table():
    with mysql.connector.connect(host=hostname,user=user,passwd=password,database=database) as f:
        cursor=f.cursor()
        table_name="pokemon"
        query=f"select * from {table_name}"
        cursor.execute(query)
        data=cursor.fetchall()
        header=('sno','ranks','name','type','total','HP','attack','defense','Sp. atk','Sp. def','Speed','generation','legendary')
        df=pandas.DataFrame(data,columns=header)#used to show the data in tabular form.
        df=df.set_index('sno')#to controll the the indexes of the dataframe
        df=df.to_string()#coverting the dataframe to string so that we can see all the entries
        print(df)

def describe_table():
    with mysql.connector.connect(host=hostname,user=user,passwd=password,database=database) as f:
        cursor=f.cursor()
        query="desc pokemon"
        cursor.execute(query)
        data=cursor.fetchall()
        header=["Field","Type","Null","Key","Default","Extra"]
        df=pandas.DataFrame(data=data,columns=header)
        print(df)

def insert_table():
    with mysql.connector.connect(host=hostname,user=user,passwd=password,database=database) as f:
        cursor=f.cursor()
        desc_query="desc pokemon"
        cursor.execute(desc_query)
        desc=cursor.fetchall()
        print("Headers:")
        for x in range(len(desc)):
            print(f"{desc[x][0]}",end=",")
        print()

        new_values=[]
        for x in range(len(desc)):
            value=eval(input("enter the new values following the above format(1 by 1):"))
            new_values.append(value)
        new_values=tuple(new_values)
        print(new_values)
        query=f"insert into pokemon values{new_values}"
        cursor.execute(f"{query}")
        f.commit()

    add_more=input("add more? [y/n]:")
    if add_more.lower() in "y":
        insert_table()#recurse
    else:
        return

def remove_table():...    
              
def menu():...