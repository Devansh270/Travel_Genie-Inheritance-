# Simple in-memory session storage.
# This is mainly for development/testing purposes.
# Data will be lost if the server restarts.
sessions = {}


def get_session(session_id):
    """
    Fetch an existing itinerary using the session ID.

    Returns:
        The stored itinerary if the session exists,
        otherwise None.
    """
    return sessions.get(session_id)


def save_session(session_id, itinerary):
    """
    Save or update a user's itinerary in the session store.
    """
    sessions[session_id] = itinerary