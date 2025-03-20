from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from datetime import datetime
import sqlite3
import logging
from werkzeug.security import check_password_hash
import uuid

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Ensure this is a secure key

# Helper function to check if user is admin
def is_admin():
    return 'user_id' in session and session.get('is_admin', False)

@app.route('/')
def index():
    try:
        # Ensure a user_id exists in the session (for guests)
        if 'user_id' not in session:
            session['user_id'] = str(uuid.uuid4())  # Assign a unique ID to guests
        conn = sqlite3.connect('parking.db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT spot_id, status, user_plate, last_updated, latitude, longitude, "
            "user_id FROM parking_spots"
        )
        spots = cursor.fetchall()
        conn.close()
        user_id = session.get('user_id', None)
        admin_status = is_admin()
        return render_template(
            'index.html', spots=spots, user_id=user_id, is_admin=admin_status
        )
    except Exception as e:
        logger.error(f"Error rendering index: {e}")
        return "An error occurred. Check the server logs.", 500

@app.route('/get_user_id')
def get_user_id():
    try:
        user_id = session.get('user_id', str(uuid.uuid4()))
        if 'user_id' not in session:
            session['user_id'] = user_id
        return jsonify({'user_id': user_id})
    except Exception as e:
        logger.error(f"Error getting user ID: {e}")
        return jsonify({'user_id': null}), 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        try:
            conn = sqlite3.connect('parking.db')
            cursor = conn.cursor()
            cursor.execute(
                "SELECT user_id, password_hash, is_admin FROM users WHERE username = ?",
                (username,)
            )
            user = cursor.fetchone()
            conn.close()
            if user:
                logger.debug(f"User found: {user}")
                if check_password_hash(user[1], password):
                    session['user_id'] = user[0]
                    session['is_admin'] = bool(user[2])
                    logger.debug(
                        f"Logged in user: {username}, user_id: {user[0]}, is_admin: {user[2]}"
                    )
                    return jsonify({'success': True})
                else:
                    logger.warning(f"Password mismatch for username: {username}")
                    return jsonify({'success': False, 'message': 'Invalid username or password'})
            else:
                logger.warning(f"User not found for username: {username}")
                return jsonify({'success': False, 'message': 'Invalid username or password'})
        except Exception as e:
            logger.error(f"Error in login: {str(e)}")
            return jsonify({'success': False, 'message': f'Server error during login: {str(e)}'})
    return ''

@app.route('/logout')
def logout():
    try:
        session.pop('user_id', None)
        session.pop('is_admin', None)
        logger.debug("User logged out")
        return redirect(url_for('index'))
    except Exception as e:
        logger.error(f"Error in logout: {e}")
        return "An error occurred during logout.", 500

@app.route('/get_spots')
def get_spots():
    try:
        conn = sqlite3.connect('parking.db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT spot_id, status, last_updated, latitude, longitude, user_id "
            "FROM parking_spots"
        )
        spots = [
            {
                'spot_id': row[0], 'status': row[1], 'last_updated': row[2],
                'latitude': row[3], 'longitude': row[4], 'user_id': row[5]
            } for row in cursor.fetchall()
        ]
        conn.close()
        return jsonify(spots)
    except Exception as e:
        logger.error(f"Error getting spots: {e}")
        return jsonify({'error': 'Failed to retrieve spots'}), 500

@app.route('/update_spot', methods=['POST'])
def update_spot():
    spot_id = request.form['spot_id']
    user_id = session.get('user_id', str(uuid.uuid4()))
    try:
        conn = sqlite3.connect('parking.db')
        cursor = conn.cursor()
        # Check if the user already has a spot
        cursor.execute(
            "SELECT spot_id FROM parking_spots WHERE user_id = ? AND status = 'occupied'",
            (user_id,)
        )
        existing_spot = cursor.fetchone()
        if existing_spot:
            conn.close()
            message = f'You already have Spot {existing_spot[0]} selected. Cancel it first to select a new spot.'
            logger.warning(message)
            return jsonify({'message': message})

        # Proceed with selecting the new spot
        cursor.execute("SELECT status, user_id FROM parking_spots WHERE spot_id = ?",
                      (spot_id,))
        status, spot_user_id = cursor.fetchone() or (None, None)
        if status == 'available' and spot_user_id is None:
            cursor.execute(
                "UPDATE parking_spots SET status = 'occupied', user_id = ?, "
                "last_updated = ? WHERE spot_id = ?",
                (user_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), spot_id)
            )
            conn.commit()
            message = f'Spot {spot_id} marked as occupied'
            logger.debug(message)
        else:
            message = f'Spot {spot_id} is already occupied or reserved'
            logger.warning(message)
        conn.close()
        return jsonify({'message': message})
    except Exception as e:
        logger.error(f"Error updating spot {spot_id}: {e}")
        return jsonify({'message': 'Server error updating spot'}), 500

@app.route('/cancel_user_spot', methods=['POST'])
def cancel_user_spot():
    spot_id = request.form['spot_id']
    user_id = session.get('user_id', None)
    if not user_id:
        return jsonify({'message': 'User not authenticated'}), 401
    try:
        conn = sqlite3.connect('parking.db')
        cursor = conn.cursor()
        # Verify the spot belongs to the user
        cursor.execute(
            "SELECT user_id FROM parking_spots WHERE spot_id = ? AND status = 'occupied'",
            (spot_id,)
        )
        spot = cursor.fetchone()
        if not spot or spot[0] != user_id:
            conn.close()
            message = 'You can only cancel your own spot'
            logger.warning(message)
            return jsonify({'message': message})

        cursor.execute(
            "UPDATE parking_spots SET status = 'available', user_id = NULL, "
            "last_updated = ? WHERE spot_id = ?",
            (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), spot_id)
        )
        conn.commit()
        conn.close()
        message = f'Spot {spot_id} cancelled by user'
        logger.debug(message)
        return jsonify({'message': message})
    except Exception as e:
        logger.error(f"Error cancelling spot {spot_id}: {e}")
        return jsonify({'message': 'Server error cancelling spot'}), 500

@app.route('/reset_spot', methods=['POST'])
def reset_spot():
    if not is_admin():
        return jsonify({'message': 'Admin access required'}), 403
    spot_id = request.form['spot_id']
    try:
        conn = sqlite3.connect('parking.db')
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE parking_spots SET status = 'available', user_id = NULL, "
            "last_updated = ? WHERE spot_id = ?",
            (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), spot_id)
        )
        conn.commit()
        conn.close()
        message = f'Spot {spot_id} marked as available by admin'
        logger.debug(message)
        return jsonify({'message': message})
    except Exception as e:
        logger.error(f"Error resetting spot {spot_id}: {e}")
        return jsonify({'message': 'Server error resetting spot'}), 500

@app.route('/reserve_spot', methods=['POST'])
def reserve_spot():
    spot_id = request.form['spot_id']
    start_time = request.form['start_time']
    end_time = request.form['end_time']
    user_id = session.get('user_id', str(uuid.uuid4()))
    try:
        conn = sqlite3.connect('parking.db')
        cursor = conn.cursor()
        # Check if the user already has a spot
        cursor.execute(
            "SELECT spot_id FROM parking_spots WHERE user_id = ? AND status = 'reserved'",
            (user_id,)
        )
        existing_spot = cursor.fetchone()
        if existing_spot:
            conn.close()
            message = f'You already have Spot {existing_spot[0]} reserved. Cancel it first to reserve a new spot.'
            logger.warning(message)
            return jsonify({'message': message})

        cursor.execute("SELECT status, user_id FROM parking_spots WHERE spot_id = ?",
                      (spot_id,))
        status, spot_user_id = cursor.fetchone() or (None, None)
        if status == 'available' and spot_user_id is None:
            cursor.execute(
                "SELECT * FROM reservations WHERE spot_id = ? AND "
                "((start_time <= ? AND end_time >= ?) OR "
                "(start_time <= ? AND end_time >= ?))",
                (spot_id, end_time, start_time, start_time, end_time)
            )
            overlapping = cursor.fetchone()
            if not overlapping:
                cursor.execute(
                    "UPDATE parking_spots SET status = 'reserved', user_id = ?, "
                    "last_updated = ? WHERE spot_id = ?",
                    (user_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), spot_id)
                )
                cursor.execute(
                    "INSERT INTO reservations (spot_id, user_id, start_time, end_time) "
                    "VALUES (?, ?, ?, ?)",
                    (spot_id, user_id, start_time, end_time)
                )
                conn.commit()
                message = f'Spot {spot_id} reserved by {("admin" if is_admin() else "user")} from {start_time} to {end_time}'
                logger.debug(message)
            else:
                message = f'Spot {spot_id} is already reserved during this time'
                logger.warning(message)
        else:
            message = f'Spot {spot_id} is not available for reservation'
            logger.warning(message)
        conn.close()
        return jsonify({'message': message})
    except Exception as e:
        logger.error(f"Error reserving spot {spot_id}: {e}")
        return jsonify({'message': 'Server error reserving spot'}), 500

@app.route('/cancel_reservation', methods=['POST'])
def cancel_reservation():
    if not is_admin():
        return jsonify({'message': 'Admin access required'}), 403
    spot_id = request.form['spot_id']
    try:
        conn = sqlite3.connect('parking.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM reservations WHERE spot_id = ?", (spot_id,))
        cursor.execute(
            "UPDATE parking_spots SET status = 'available', user_id = NULL, "
            "last_updated = ? WHERE spot_id = ?",
            (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), spot_id)
        )
        conn.commit()
        conn.close()
        message = f'Reservation for Spot {spot_id} cancelled by admin'
        logger.debug(message)
        return jsonify({'message': message})
    except Exception as e:
        logger.error(f"Error cancelling reservation for spot {spot_id}: {e}")
        return jsonify({'message': 'Server error cancelling reservation'}), 500

if __name__ == '__main__':
    app.run(debug=True)