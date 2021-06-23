import psycopg2
import example_psql as creds

#import sqlite3
#from pysqlcipher3 import dbapi2 as sqlite3

DEBUG=False

class Message:
    def __init__(self, type, description):
        self.type = type
        self.desc = description

    def __str__(self):
        return f"[{self.type}] {self.desc}"


class Database:
    def __init__(self, currentDB):
        self.currentDB = currentDB

    def connect(self):
        if self.currentDB == "SQLite":
            try:
                connection = sqlite3.connect(creds.DATABASE_PATH)
                return connection
            except:
                print("[ERROR] Failed to connect to database path.")
        if self.currentDB == "POSTGRESQL":
            try:
                conn_string = "host="+ creds.PGHOST +" port="+ creds.PGPORT +" dbname="+ creds.PGDATABASE +" user=" + creds.PGUSER \
                +" password="+ creds.PGPASSWORD
                connection=psycopg2.connect(conn_string)
                return connection
                if DEBUG==True:
                    print("[INFO] Connected to database.")
            except (Exception, psycopg2.Error) as e:
                print(f"[ERROR] Could not connect to database: {e}")

    def find_password(self, app_name):
        try:
            connection = self.connect()
            cursor = connection.cursor()
            postgres_select_query = f""" SELECT password FROM accounts WHERE app_name = '{app_name}'"""
            if self.currentDB == "SQLite":
                cursor.execute(postgres_select_query)
            elif self.currentDB == "POSTGRESQL":
                cursor.execute(postgres_select_query)
            connection.commit()
            result = cursor.fetchone()
            return Message("RESULT", result[0])
        except Exception if self.currentDB=="SQLite" else (Exception, psycopg2.Error) as error:
            return Message("ERROR", error)

    def store_passwords(self, password, user_email, username, url, app_name):
        try:
            connection = self.connect()
            cursor = connection.cursor()
            record_to_insert = (password, user_email, username, url, app_name)
            if self.currentDB == "SQLite":
                postgres_insert_query = f"INSERT INTO accounts (password, email, username, url, app_name) VALUES (?,?,?,?,?)"
                cursor.execute(postgres_insert_query, record_to_insert)
            elif self.currentDB == "POSTGRESQL":
                postgres_insert_query = f"INSERT INTO accounts (password, email, username, url, app_name) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(postgres_insert_query, record_to_insert)
            connection.commit()
            return Message("RESULT","\nDone \nI will remember it for you\n")
        except Exception if self.currentDB=="SQLite" else (Exception, psycopg2.Error) as error:
            return Message("ERROR", error)

    def find_info(self, field, value, want="*"):
        data = ('Password: ', 'Email: ', 'Username: ', 'url: ', 'App/Site name: ') 
        try:
            connection = self.connect()
            cursor = connection.cursor()
            postgres_select_query = """ SELECT """ + want+""" FROM accounts WHERE """+ field +" = '"+value+"'"
            if self.currentDB == "SQLite":
                cursor.execute(postgres_select_query)
            elif self.currentDB == "POSTGRESQL":
                cursor.execute(postgres_select_query, (want, field, value))
            connection.commit()
            result = cursor.fetchall()
            if result!= []:
                return Message("RESULT", result)
                #print(result)
                '''for row in result:
                    for i in range(0, len(row)):
                        if want=="*":
                            print(data[i] + row[i])
                        else:
                            print(want,": ", row[i])
                print('')
                print('-'*30)'''
            else: return Message("RESULT", "No data found.")
        
        except Exception if self.currentDB=="SQLite" else (Exception, psycopg2.Error) as error:
            return Message("ERROR", error)

    def change_password_to(self, new_password, app_name):
        try:
            connection = self.connect()
            cursor = connection.cursor()
            postgres_select_query = """ UPDATE accounts SET password = '"""+ new_password +"""' WHERE app_name = '""" + app_name + "'"
            if self.currentDB == "SQLite":
                cursor.execute(postgres_select_query)
            elif self.currentDB == "POSTGRESQL":
                cursor.execute(postgres_select_query, (new_password, app_name))
            connection.commit()
            return Message("RESULT", "Password has been changed successfull.")
        except Exception if self.currentDB=="SQLite" else (Exception, psycopg2.Error) as error:
            return Message("ERROR", error)
    
    def delete_data_with(self, field, value):
        try:
            connection = self.connect()
            cursor = connection.cursor()
            postgres_delete_query = f"DELETE FROM accounts WHERE {field}='{value}'"
            if self.currentDB == "SQLite":
                cursor.execute(postgres_delete_query)
            elif self.currentDB == "POSTGRESQL":
                cursor.execute(postgres_delete_query)
            connection.commit()
            return Message("RESULT", f"All the data with {field}='{value}' have been deleted")
        except Exception if self.currentDB=="SQLite" else (Exception, psycopg2.Error) as error:
            return Message("ERROR", error)

    def change_user_password(self, new_password):
        try:
            connection = self.connect()
            postgres_change_query = f"ALTER ROLE username WITH PASSWORD '{new_password}'"

        except:
            pass

    def __str__(self):
        if self.currentDB == "SQLite":
            return f"Running database with '{self.currentDB}'"
        elif self.currentDB == "POSTGRESQL":
            info = "Host="+ creds.PGHOST +"\nPort="+ creds.PGPORT +" \nDatabasename="+ creds.PGDATABASE +" \nUser=" + creds.PGUSER
            return info


def test():
    db = Database("POSTGRESQL")
    print(db)
    r1 = db.store_passwords(password="password", url="url1", username="username", user_email="user_email", app_name="app_name")
    r2 = db.find_info(field="app_name", value="app_name")
    r3 = db.find_password("app_name")
    r4 = db.find_info(field="url", value="url1")
    r5 = db.delete_data_with(field="url", value="url1")
    r6 = db.find_info(field="url", value="url1")
    print("r1: ", r1, "\nr2: ", r2, "\nr3: ", r3, "\nr4: ", r4, "\nr5: ", r5, "\nr6: ", r6)


def shell_for_sqlite():
    connection = sqlite3.connect(creds.DATABASE_PATH)
    cursor = connection.cursor()
    postgres_select_query=""
    while postgres_select_query!="\q":
        postgres_select_query = input(f"{creds.DATABASE_PATH}=#")
        cursor.execute(postgres_select_query)
        connection.commit()
        result = cursor.fetchall()
        print(result)

if __name__=="__main__":
    test()
    #shell_for_sqlite()

def connect():
    try:
        conn_string = "host="+ creds.PGHOST +" port="+ creds.PGPORT +" dbname="+ creds.PGDATABASE +" user=" + creds.PGUSER \
        +" password="+ creds.PGPASSWORD
        connection=psycopg2.connect(conn_string)
        return connection
        if DEBUG==True:
            print("[INFO] Connected to database.")
    except (Exception, psycopg2.Error) as e:
        print("[ERROR] Could not connect to database: %s"%e)


def store_passwords(password, user_email, username, url, app_name):
    try:
        connection = connect()
        cursor = connection.cursor()
        postgres_insert_query = f" INSERT INTO accounts (password, email, username, url, app_name) VALUES (?, ?, ?, ?, ?)"
        record_to_insert = (password, user_email, username, url, app_name)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        return "\nDone \nI will remember it for you\n"
    except Exception as e:
        return f"[ERROR] {e}"
    '''except (Exception, psycopg2.Error) as error:
        return f"[ERROR] {error}"'''


def find_info(field, value, want="*"):
    data = ('Password: ', 'Email: ', 'Username: ', 'url: ', 'App/Site name: ') 
    try:
        connection = connect()
        cursor = connection.cursor()
        postgres_select_query = """ SELECT """ + want+""" FROM accounts WHERE """+ field +" = '"+value+"'"
        #print("-->",postgres_select_query)
        #cursor.execute(postgres_select_query, (want, field, value))
        cursor.execute(postgres_select_query)
        connection.commit()
        result = cursor.fetchall()
        if result!= []:
            print('')
            print('RESULT')
            print('')
            #print(result)
            for row in result:
                for i in range(0, len(row)):
                    if want=="*":
                        print(data[i] + row[i])
                    else:
                        print(want,": ", row[i])
            print('')
            print('-'*30)
        else: print("No data found.")
    except Exception as e:
        return f"[ERROR] {e}"
    '''except (Exception, psycopg2.Error) as error:
        print("[Error] ", error)'''


def find_password(app_name):
    try:
        connection = connect()
        cursor = connection.cursor()
        postgres_select_query = f""" SELECT password FROM accounts WHERE app_name = '{app_name}'"""
        #cursor.execute(postgres_select_query, app_name)
        cursor.execute(postgres_select_query)
        connection.commit()
        result = cursor.fetchone()
        return str(result[0])
        #print('Password is: ' )
        #print(result[0])
    except Exception as e:
        return f"[ERROR] {e}"
    '''except (Exception, psycopg2.Error) as error:
        print("[Error] ", error)'''

def change_password_to(new_password, app_name):
    try:
        connection = connect()
        cursor = connection.cursor()
        postgres_select_query = """ UPDATE accounts SET password = '"""+ new_password +"""' WHERE app_name = '""" + app_name + "'"
        cursor.execute(postgres_select_query, app_name)
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print("[Error] ", error)

#store_passwords(password="B1921117589v", app_name="github", user_email="vigneshbezawada3@gmail.com", url="https://www.github.com/login", username="BezawadaVignesh")
#find_users(field="email", value="vigneshbezawada3@gmail.com")
#find_users(field="url", value="https://www.github.com/login", want="username")
#find_users(field="url", value="Bezawadavignesh")
#find_password("github")
#change_password("This is my pass", "github")

