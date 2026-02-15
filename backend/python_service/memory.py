# simple in-memory session store
sessions = {}

def get_session(session_id):
    return sessions.get(session_id)

def save_session(session_id, itinerary):
    sessions[session_id] = itinerary
