from flask import Flask, request, session, jsonify, make_response
from datetime import timedelta
import os

app = Flask(__name__)
app.json.compact = False

# Better secret key handling - never hardcode in production!
app.secret_key = os.environ.get('SECRET_KEY') or b'?w\x85Z\x08Q\xbdO\xb8\xa9\xb65Kj\xa9_'

# Configure session lifetime (default is 31 days)
app.permanent_session_lifetime = timedelta(days=1)  # 1 day expiration

@app.route('/sessions/<string:key>', methods=['GET'])
def show_session(key):
    # Set default session values only if they don't exist
    session.setdefault("hello", "World")
    session.setdefault("goodnight", "Moon")
    
    # Track visit count in session
    session['visit_count'] = session.get('visit_count', 0) + 1

    # Prepare response data
    response_data = {
        'session': {
            'session_key': key,
            'session_value': session[key],
            'session_accessed': session.accessed,
            'visit_count': session['visit_count'],
            'session_id': session.sid,  # Unique session ID
        },
        'cookies': [{cookie: request.cookies[cookie]} 
                   for cookie in request.cookies],
        'headers': {
            'user_agent': request.headers.get('User-Agent'),
        }
    }

    response = make_response(jsonify(response_data), 200)

    # Set secure cookies with additional options
    response.set_cookie(
        'mouse', 
        value='Cookie',
        max_age=3600,  # 1 hour expiration
        secure=True,  # Only send over HTTPS
        httponly=True,  # Prevent JavaScript access
        samesite='Lax'  # CSRF protection
    )

    return response

@app.route('/sessions/clear', methods=['POST'])
def clear_session():
    # Clear all session data
    session.clear()
    
    # Create response
    response = make_response(jsonify({'message': 'Session cleared'}), 200)
    
    # Delete the mouse cookie
    response.set_cookie('mouse', '', expires=0)
    
    return response

if __name__ == '__main__':
    app.run(port=5555, ssl_context='adhoc')  # Added adhoc SSL for testing HTTPS