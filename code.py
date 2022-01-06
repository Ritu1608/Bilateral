import os
import time
import threading 
from threading import Thread
import mysql.connector

def createFiles():
    for filename in range (1,999):
        filepath = os.path.join('C:/Users/bhatt/OneDrive/Desktop/BilateralSolutions/processing', str(filename) + '.txt')
        file = open(filepath, "x")
        file.close()
        time.sleep(1)

def send_files_to_queue():
    source = 'C:/Users/bhatt/OneDrive/Desktop/BilateralSolutions/processing/'
    destination = 'C:/Users/bhatt/OneDrive/Desktop/BilateralSolutions/queue/'
    
    files = os.listdir(source)
    destination_files = os.listdir(destination)
    if not destination_files:
        for file in files:         
            os.rename(source + file, destination + file)
        threading.Timer(5, send_files_to_queue).start()
    else:
        Thread(target = send_files_to_queue).start()

def process_file():
    mydb = mysql.connector.connect(host="localhost", user="root", password="", database="bilateral")
    cursor = mydb.cursor()
    
    source = 'C:/Users/bhatt/OneDrive/Desktop/BilateralSolutions/queue/'
    destination = 'C:/Users/bhatt/OneDrive/Desktop/BilateralSolutions/processed/'
    source_files = os.listdir(source)

    if not source_files:
        Thread(target = process_file).start()
    else:
        for file in source_files:
            time.sleep(1)
            sql_insert = "INSERT INTO files (id, filename) VALUES (%s, %s)"
            val1 = ('',file)
            cursor.execute(sql_insert, val1)
            sql_update = "UPDATE files SET is_processed = %s WHERE filename =%s" 
            val2 = ('1',file)
            rows_affected = cursor.execute(sql_update, val2)
            mydb.commit()
            if(cursor.rowcount == 1):
                os.rename(source + file, destination + file)
        Thread(target = process_file).start()


def main():
    file_creation = Thread(target = createFiles).start()
    sendToQueue = threading.Timer(5, send_files_to_queue).start()   
    processing_file = Thread(target = process_file).start()

if __name__ == "__main__":
    main()

