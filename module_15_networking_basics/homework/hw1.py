from flask import make_response, Flask, request, jsonify
import sqlite3

app = Flask(__name__)


@app.route('/add-room', methods=['POST', ])
def add_room():
    try:
        data = request.json
        with sqlite3.connect('hotel.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO rooms (floor, beds, guestNum, price) VALUES (?, ?, ?, ?)",
                           (data['floor'], data['beds'], data['guestNum'], data['price']))
            return jsonify(susses=True), 200
    except Exception as err:
        return jsonify(error=str(err)), 500


@app.route('/room', methods=['GET', ])
def get_room():
    try:
        with sqlite3.connect('hotel.db') as conn:
            cursor = conn.cursor()
            rooms = cursor.execute("SELECT * FROM rooms").fetchall()
            data = [
                {'roomId': room[0], 'floor': room[1], 'beds': room[2], 'guestNum': room[3], 'price': room[4]}
                for room in rooms]
            return jsonify({'rooms': data}), 200
    except Exception as err:
        return jsonify(error=str(err)), 500


@app.route('/booking', methods=['POST', ])
def booking():
    try:
        data = request.json
        room_id = data.get('roomId')
        with sqlite3.connect('hotel.db') as conn:
            cursor = conn.cursor()
            room = cursor.execute("SELECT * FROM rooms WHERE roomId = ?", (room_id,)).fetchone()
            if room is None:
                return jsonify(error='Room not found'), 409
            cursor.execute("INSERT INTO booking SELECT * FROM rooms WHERE roomId = ?", (room_id,))
            cursor.execute("DELETE FROM rooms WHERE roomId = ?", (room_id,))
            response = make_response(jsonify(susses=True, bookeRoom={'floor': room[1], 'beds': room[2], 'guestNum': room[3], 'price': room[4]}), 200)
            return response
    except Exception as err:
        return jsonify(error=str(err)), 500


if __name__ == "__main__":
    app.run(debug=True)
