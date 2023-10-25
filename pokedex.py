import mysql.connector
import pandas 
import csv
from details import sql_details
#with mysql.connector.connect(host=hostname,user=user,passwd=password,database=database) as f:
#create table pokedex(sno int primary key,ranks int,name varchar(255),type1 varchar(20),total int,hp int,attack int,defense int,sp_atk int,sp_def int,speed int,generation int,legendary varchar(25));
hostname,user,password,database=sql_details()

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

def remove_table():
    with mysql.connector.connect(host=hostname,user=user,passwd=password,database=database) as f:
        cursor=f.cursor()
        query="desc pokemon"
        cursor.execute(query)
        desc=cursor.fetchall()
        print("Headers:")
        for x in range(len(desc)):
            print(f"{desc[x][0]}",end=",")
        print()
        condition_header=input("enter the condition column:")
        condition_operator=input("enter the condition operator:")
        condition=eval(input("enter the value for condition:"))

        if type(condition)==type(int()):
            query=f"delete from pokemon where {condition_header}{condition_operator}{condition}"
        elif type(condition)==type(str()):
            query=f"delete from pokemon where {condition_header}{condition_operator}'{condition}'"

        confirmation=input("are you sure you want to delete this data? [y/n]:")
        if confirmation.lower() in 'y':
            cursor.execute(query)
            f.commit()
            print("deleted the data!")
            i=input("do you want to see the table after this change? [y/n]:")
            if i.lower() in 'y':
                show_table()
                return
            else:
                print("ending the program!")
                pass
            
        else:
            query=""
            print("deletion has been stopped!")
            return

def Select_table():
    with mysql.connector.connect(host=hostname,user=user,passwd=password,database=database) as f:
        cursor=f.cursor()
        
        query="desc pokemon"
        cursor.execute(query)
        desc=cursor.fetchall()
        print("Headers:")
        for x in range(len(desc)):
            print(f"{desc[x][0]}",end=",")
        print()

        condition_header=input("enter the condition column:")
        condition_operator=input("enter the condition operator:")
        condition=eval(input("enter the value for condition:"))
        print()

        query_data=[]
        while True:
            print()
            ColumnName=input("enter the column name:")
            query_data.append(ColumnName)
            Conti=input("do you want to continue? [y/n]?:")
            if Conti.lower() not in ['y']:
                break
        print()

        leng=len(query_data)
        cstring=""
        for x in range(leng):
            if x==0:
                cstring+=f"{query_data[x]}"
            else:
                cstring+=f",{query_data[x]}"

        if type(condition) == type(int()):
            qstring=f"select {cstring} from pokemon where {condition_header}{condition_operator}{condition}"
        elif type(condition) == type(str()):
            qstring=f"select {cstring} from pokemon where {condition_header}{condition_operator}'{condition}'"
        cursor.execute(qstring)
        data=cursor.fetchall()
            

        df=pandas.DataFrame(data=data,columns=query_data)
        df=df.to_string()
        print(df)

def update_table():
    with mysql.connector.connect(host=hostname,user=user,passwd=password,database=database) as f:
        cursor=f.cursor()

        print("loading all the data from the sql table!\nThis may take some time!\n")
        show_table()
        print()
        query="desc pokemon"
        cursor.execute(query)
        desc=cursor.fetchall()
        print("Headers:")
        for x in range(len(desc)):
            print(f"{desc[x][0]}",end=",")
        print()
        cname=input('enter the coulmn name you want to update:')
        value=eval(input("enter the value for this column:"))
        condition_header=input("enter the condition header:")
        condition_operator=input('enter the operator:')
        condition=eval(input("enter the condition:"))
        print()
        if type(condition) == type(int()):
            query=f"update pokemon set {cname}={value} where {condition_header}{condition_operator}{condition}"
        elif type(condition)==type(str()):
            query=f"update pokemon set {cname}={value} where {condition_header}{condition_operator}'{condition}'"
        
        cursor.execute(query)
        f.commit()

def sql_to_csv():
    with mysql.connector.connect(host=hostname,user=user,passwd=password,database=database) as f:
        cursor=f.cursor()
        query="desc pokemon"
        cursor.execute(query)
        desc=cursor.fetchall()

        headers=[]
        for x in range(len(desc)):
            headers.append(desc[x][0])
        headers=tuple(headers)

        query="select * from pokemon"

        cursor.execute(query)
        data=cursor.fetchall()

        data=tuple(data)

    CsvName=input('enter the csv file name (which will be generated and created):')
    with open(f"{CsvName}.csv","w",newline='\n') as fo:
        w=csv.writer(fo)
        w.writerow(headers)
        w.writerows(data)

def csv_to_sql(CsvFileName:str,TableName:str):
    with open(f"{CsvFileName}.csv","r") as f:
        reader=csv.reader(f)
        csv_list=[]
        for x in reader:
            x=tuple(x)
            csv_list.append(x)
        headers=csv_list.pop(0)
        csv_list=tuple(csv_list)
        #print(csv_list)
    header=input("enter your header query seperate every query with ',' (format: <name> <data_type> <constraint>, <--repeat):")
    headers=input("enter your headers without the the datatype and constraint:")
    with mysql.connector.connect(host=hostname,user=user,passwd=password,database=database) as f:
        cursor=f.cursor()
        query=f"create table {TableName}({header})"
        #cursor.execute(query)
        for x in csv_list:
            #print(x)
            query=f"insert into {TableName}({headers}) values{x}"
            print(query)
            cursor.execute(query)
        f.commit()
