import psycopg2
from psycopg2 import OperationalError
from json import loads

class database:

    def __init__(self):
        self.connection = None

    def create_connection(self, db_name, db_user, db_password, db_host, db_port):
        try:
            self.connection = psycopg2.connect(
                database=db_name,
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port,
            )
            print("Connection to PostgreSQL DB successful")
        except OperationalError as e:
            print(f"The error '{e}' occurred")

    def input(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()

    def output(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()

db = database()
with open("run_config.json", "r") as readfile:
    config = loads(readfile.read())
    db.create_connection(config.get("db_name"), config.get("db_user"), config.get("db_password"), config.get("db_host"), config.get("db_port"))

def main():
    ch = "2+2"
    while ch != "q":
        eval(ch)
        ch = input('Enter the command(enter "q" to quit): ')

if __name__ == "__main__":
    main()