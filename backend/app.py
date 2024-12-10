from datetime import datetime
from flask import request,Flask,Response,jsonify
import mysql.connector
from mysql.connector import errorcode

app = Flask(__name__)

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    print(response)
    return response

def get_connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="kuo",
            passwd="313831005",
            database="hw_database"
        )
    except Exception as err:
        print(f"in get connection {err}")

@app.route("/")
def hello():
    get_connection()
    return "Hello world"

@app.route("/login",methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    try:
        with get_connection() as connection:
            with connection.cursor(dictionary=True)  as cursor:
                query = "SELECT * FROM member WHERE name=%s AND password=%s"
                cursor.execute(query,[username,password])
                info = cursor.fetchone()                
                return jsonify({'success': True, 'id': info["id"]})
    except Exception as err:
        print(f"login in {err}")
        return jsonify({'success': False,'error': f"{err}"}),400
    
    return jsonify({'success': False}),400

@app.route("/register",methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get("email")
    phone = request.form.get("phone")
    address = request.form.get("address")

    with get_connection() as connection:
        with connection.cursor() as cursor:
            try:
                query = "INSERT INTO member (name, email, password, phone, address) VALUE (%s,%s,%s,%s,%s)"
                cursor.execute(query,[username,email,password,phone,address])
                connection.commit()
                return jsonify({'success': True, 'id': cursor.lastrowid})
            except mysql.connector.IntegrityError as err:
                if err.errno == errorcode.ER_DUP_ENTRY:
                    return "The email has been used.",400
            except Exception as err:
                print(err)
                return f"Error: {err}",400
            
    return "Error unknown",404

@app.route("/bid",methods=['POST'])
def bid():
    item_id= request.form.get('item_id')
    bid_price= int(request.form.get('bid_price'))
    buyer_id= request.form.get('buyer_id')
    with get_connection() as connection:
        with connection.cursor(dictionary=True) as cursor:
            try:
                cursor.execute("SELECT current_price, starting_price, auction_end_time FROM auction_item WHERE id = %s", [item_id])
                item = cursor.fetchone()
                # 是否有這個item
                if not item: return jsonify({"error": "Auction item not found"}), 404
                # 驗證拍賣是否結束  
                if datetime.now() > item['auction_end_time']: return jsonify({"error": "Auction has already ended"}), 400 
                # 檢查是否出價高於當前出價
                current_price = item['current_price']
                if bid_price <= current_price: return jsonify({"error": "Bid price must be higher than the current price"}), 400

                cursor.execute("""
                UPDATE auction_item
                SET current_price = %s, buyer_id = %s
                WHERE id = %s
                """, (bid_price, buyer_id, item_id))
                connection.commit()
                # 新增至歷史紀錄
                cursor.execute("""
                INSERT INTO memeber_auction_record (item_id,member_id,price) VALUES (%s,%s,%s)
                """, (item_id,buyer_id,bid_price))
                connection.commit()

                return jsonify({"success": True, "message": "Bid placed successfully", "item_id": item_id}), 200
            
            except mysql.connector.Error as err:
                print(err.msg)
                return jsonify({"success": False, "Error": f"{err}"}), 400
            except Exception as err:
                print(err)
            
    return "Error unknown",404

@app.route("/getAuctionItems",methods=['GET'])
def getAuctionItem():
    with get_connection() as connection:
        with connection.cursor(dictionary=True) as cursor:
            try:
                cursor.execute("SELECT * FROM auction_item",[])
                rows = cursor.fetchall()
                print(rows)
                return jsonify(rows)
            except Exception as err:
                print(err)
    return ""

@app.route("/getUserBids",methods=['POST'])
def getUserBids():
    buyer_id = request.form.get('buyer_id')
    with get_connection() as connection:
        with connection.cursor(dictionary=True) as cursor:
            try:
                cursor.execute("""
                SELECT 
                    mar.id AS record_id,
                    auction.item_name AS item_name,
                    mar.price,
                    mar.update_time
                FROM 
                    memeber_auction_record AS mar
                JOIN 
                    auction_item AS auction
                ON 
                    mar.item_id = auction.id
                WHERE 
                    mar.member_id = %s;
               """,[buyer_id])
                rows = cursor.fetchall()
                return jsonify(rows)
            except Exception as err:
                print(err)
    return "",404

@app.route("/evlAuctionItem",methods=['POST'])
def evlAuctionItem():
    data = request.form
    region = data.get('region')
    author = data.get('author')
    name = data.get('name')
    material = data.get('material')
    time_of_work = data.get('time_of_work')
    source = data.get('source')
    price = data.get('price')
    description = data.get('description')
    member_id = data.get('member_id')
    query = """
        INSERT INTO evaluate_item (
            region, author, name, material, time_of_work, source, price, description, member_id 
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s
        );
    """

    print("Hello in evl",author,price)
    with get_connection() as connection:
        with connection.cursor(dictionary=True) as cursor:
            try:
                cursor.execute(query,[region,author,name,material,time_of_work,source,price,description,member_id])
                connection.commit()

                return jsonify({'success':True})
            except Exception as err:
                print(err)
                return "",401
    return "",404

@app.route("/getSellerEvlItems",methods=['POST'])
def getSellerEvlItems():
    member_id = request.form.get('id')
    query = "SELECT name,image,evaluate_price,evaluate_status FROM evaluate_item WHERE member_id=%s"
    with get_connection() as connection:
        with connection.cursor(dictionary=True) as cursor:
            try:
                cursor.execute(query,[member_id])
                rows = cursor.fetchall()
                return jsonify(rows)
            except Exception as err:
                print(err)
                return "",404
    return "",404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)