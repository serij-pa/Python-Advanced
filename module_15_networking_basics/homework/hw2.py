from flask import make_response, Flask, request, jsonify
import sqlite3

app = Flask(__name__)


@app.route('/room', methods=['GET', 'POST', 'DELETE'])
def get_room():
    try:
        with sqlite3.connect('hotel.db') as conn:
            cursor = conn.cursor()

            if request.method == 'GET':
                rooms = cursor.execute("SELECT * FROM rooms").fetchall()
                data = [
                    {'roomId': room[0], 'floor': room[1], 'beds': room[2], 'guestNum': room[3], 'price': room[4],
                     'links': {'info_room': '/room/' + str(room[0])}}
                    for room in rooms]
                return jsonify({'rooms': data}), 200

            elif request.method == 'POST':
                data = request.json
                cursor.execute("INSERT INTO rooms (floor, beds, guestNum, price) VALUES (?, ?, ?, ?)",
                               (data['floor'], data['beds'], data['guestNum'], data['price']))
                return jsonify(susses=True, message="Room is created"), 201

            elif request.method == 'DELETE':
                data = request.json
                room_id = data.get('roomId')
                room = cursor.execute("SELECT * FROM rooms WHERE roomId = ?", (room_id,)).fetchone()
                if room is None:
                    return jsonify(error='Такой комнаты нет'), 404
                cursor.execute("DELETE FROM rooms WHERE roomId = ?", (room_id,))
                response = make_response(jsonify(susses=True, deleted_room=f"Комната (roomId:{room_id}) удалена"), 200)
                return response
            
    except Exception as err:
        return jsonify(error=str(err)), 500


@app.route('/room/<int:room_id>', methods=['GET', 'POST'])
def info_room(room_id):
    try:
        with sqlite3.connect('hotel.db') as conn:
            cursor = conn.cursor()

            if request.method == 'GET':
                room = cursor.execute("SELECT * FROM rooms WHERE roomId = ?", (room_id,)).fetchone()
                if room is None:
                    return jsonify(error='Room not found'), 404
                response = make_response(jsonify(susses=True, bookedRoom={'floor': room[1], 'beds': room[2], 'guestNum': room[3], 'price': room[4]},
                                                 description='описание комнаты',),200)
                return response

            elif request.method == 'POST':
                room = cursor.execute("SELECT * FROM rooms WHERE roomId = ?", (room_id, )).fetchone()
                if room is None:
                    return jsonify(error='Room not found'), 409
                cursor.execute("INSERT INTO booking SELECT * FROM rooms WHERE roomId = ?", (room_id,))
                cursor.execute("DELETE FROM rooms WHERE roomId = ?", (room_id,))
                response = make_response(jsonify(susses=True,
                                                 bookedRoom={'floor': room[1], 'beds': room[2], 'guestNum': room[3], 'price': room[4]},
                                                 message="Booking is created"), 201)
                return response
    except Exception as err:
        return jsonify(error=str(err)), 500


@app.route('/booking', methods=['GET', 'POST', 'DELETE'])
def booking():
    try:
        with sqlite3.connect('hotel.db') as conn:
            cursor = conn.cursor()
            if request.method == 'GET':
                rooms = cursor.execute("SELECT * FROM booking").fetchall()
                data = [
                    {'roomId': room[0], 'floor': room[1], 'beds': room[2], 'guestNum': room[3], 'price': room[4],
                     'links': {'info_booking': '/room/' + str(room[0])}}
                    for room in rooms]
                return jsonify({'rooms': data}), 200

            elif request.method == 'POST':
                data = request.json
                room_id = data.get('roomId')
                room = cursor.execute("SELECT * FROM rooms WHERE roomId = ?", (room_id,)).fetchone()
                if room is None:
                    return jsonify(error='Room not found'), 409
                cursor.execute("INSERT INTO booking SELECT * FROM rooms WHERE roomId = ?", (room_id,))
                cursor.execute("DELETE FROM rooms WHERE roomId = ?", (room_id,))
                response = make_response(jsonify(susses=True, bookeRoom={'floor': room[1], 'beds': room[2], 'guestNum': room[3], 'price': room[4]}, message="Комната забронирована"), 201)
                return response

            elif request.method == 'DELETE':
                data = request.json
                room_id = data.get('roomId')
                room = cursor.execute("SELECT * FROM booking WHERE roomId = ?", (room_id)).fetchone()
                if room is None:
                    return jsonify(error='Такой комнаты нет'), 404
                cursor.execute("INSERT INTO rooms SELECT * FROM booking WHERE roomId = ?", (room_id,))
                cursor.execute("DELETE FROM booking WHERE roomId = ?", (room_id,))
                response = make_response(jsonify(susses=True, message=f"Бронь {room_id} отменена"), 200)
                return response

    except Exception as err:
        return jsonify(error=str(err)), 500


@app.route('/booking/<int:room_id>', methods=['GET', ])
def info_booking(room_id):
    try:
        with sqlite3.connect('hotel.db') as conn:
            cursor = conn.cursor()
            room = cursor.execute("SELECT * FROM booking WHERE roomId = ?", (room_id,)).fetchone()
            if room is None:
                return jsonify(error='Комната не найдена'), 404
            response = make_response(jsonify(susses=True,
                                             bookedRoom={'floor': room[1], 'beds': room[2], 'guestNum': room[3], 'price': room[4]},
                                             description='описание комнаты', ), 200)
            return response
    except Exception as err:
        return jsonify(error=str(err)), 500


if __name__ == "__main__":
    app.run(debug=True)
