import mysql.connector, argparse, os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv("info.env")
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
current_time = datetime.now()

parser = argparse.ArgumentParser()
parser.add_argument("--add", nargs=3)
parser.add_argument("--modify", nargs=4)
parser.add_argument("--delete")

args = parser.parse_args()
cursor = db.cursor()

if args.add:
    try:    
        amount, y_n , purpose= args.add
        amount = int(amount)
        y_n = y_n.lower()
        if y_n not in ["yes", "no"]:
            print("ERROR: you need to enter \"yes\" or \"no\" in the expence argument")
            exit()
        elif amount <= 0:
            print("ERROR: you can't enter a negative number or 0 as your amount argument")
            exit()
        cursor.execute("INSERT INTO transactions (amount, expence, purpose, created_at) VALUES (%s, %s, %s, %s)", (amount, y_n, purpose, current_time))
        db.commit()
    except ValueError:
        print("ERROR: you need to enter an integer in the amount argument")    
if args.modify:
    id, amount, y_n , purpose= args.modify
    try:    
        amount = int(amount)
        id = int(id)
        y_n = y_n.lower()
        if y_n not in ["yes", "no"]:
            print("ERROR: you need to enter \"yes\" or \"no\" in the expence argument")
            exit()
        elif amount <= 0:
            print("ERROR: you can't enter a negative number or 0 as your amount argument")
            exit()
        ids = []
        cursor.execute("SELECT id FROM transactions")
        results = cursor.fetchall()
        for row in results:
            ids.append(row[0])
        if id not in ids:
            print("ERROR: id not found")     
            exit()
        cursor.execute("UPDATE transactions SET amount=%s, expence=%s, purpose=%s WHERE id=%s", (amount, y_n, purpose, id)) 
        db.commit()   
    except ValueError:
        print("ERROR: you need to enter an integer in the amount and id argument")
        exit()
elif args.delete:
    try:
        id = args.delete
        id = int(id)
        cursor.execute("DELETE FROM transactions WHERE id = %s", (id,))
        db.commit()
    except ValueError:
        print("ERROR: you need to enter an integer in the id argument")
