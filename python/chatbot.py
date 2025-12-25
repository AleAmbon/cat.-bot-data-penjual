import mysql.connector
import time
import random

# Database connection config
db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'toko_iki',
}

def get_connection():
    return mysql.connector.connect(**db_config)

def chatbot_response(message):
    msg = message.lower()
    if 'halo' in msg:
        return "Halo! Ada yang bisa saya bantu?"
    elif 'stok' in msg:
        return "Untuk cek stok, silakan buka menu Data Barang."
    elif 'harga' in msg:
        return "Harga barang bisa dilihat di menu Data Barang."
    elif 'jam' in msg:
        return "Toko buka dari jam 08:00 - 17:00."
    else:
        return "Maaf, saya tidak mengerti. Silakan tanya admin."

def run_bot():
    print("Chatbot Toko Iki is running...")
    while True:
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Find messages with NULL response
            cursor.execute("SELECT id, message FROM chat_history WHERE response IS NULL")
            unanswered = cursor.fetchall()
            
            for chat in unanswered:
                print(f"Processing message: {chat['message']}")
                response = chatbot_response(chat['message'])
                
                # Update with response
                sql = "UPDATE chat_history SET response = %s WHERE id = %s"
                cursor.execute(sql, (response, chat['id']))
                conn.commit()
                print(f"Replied: {response}")
                
            cursor.close()
            conn.close()
            
            time.sleep(2) # Poll every 2 seconds
            
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    run_bot()
