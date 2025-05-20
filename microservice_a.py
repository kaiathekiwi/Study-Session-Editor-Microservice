# ----------------------------------------------------------------------------------------------------
# microservice_a.py
# ----------------------------------------------------------------------------------------------------
# Handles editing and deleting study sessions for the main program.
# ----------------------------------------------------------------------------------------------------

import zmq
import json
import os


def load_sessions(filename):
    # if the study_sessions.json exists
    if os.path.exists(filename):
        # try to load the study_sessions.json
        try:
            with open(filename, 'r') as file:
                return json.load(file)

        # if unable to open/load, then return nothing
        except json.JSONDecodeError:
            return None

    # if it doesn't exist, return none
    else:
        return None


def save_session(filename, data, success_message="Changes saved successfully."):
    # try to write changes to the .json
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=2)
        return {
            "status": "success",
            "message": success_message
        }

    # if unable to write for any reason
    except (Exception,):  # written weirdly to avoid errors in PyCharm
        return {
            "status": "error",
            "message": "Failed to save changes."
        }


def edit_session(sessions, req):
    # initialize session number, found, and updated variables
    session_num = req["session_number"]
    found = False
    updated = False

    # check all sessions in the json file
    for session in sessions:
        if session.get("session_number") == session_num:
            found = True
            # if the request had a new subject tag, and it's different from the existing one
            if "new_subject_tag" in req:
                if req["new_subject_tag"] != session.get("subject_tag"):
                    session["subject_tag"] = req["new_subject_tag"]
                    updated = True
            # if the request had a new session note, and it's different from the existing one
            if "new_session_note" in req:
                if req["new_session_note"] != session.get("session_note"):
                    session["session_note"] = req["new_session_note"]
                    updated = True

            # stop looking once found
            break

    # if the session with the matching session_number wasn't found, return error
    if not found:
        return {
            "status": "error",
            "message": f"Session {session_num} not found."
        }

    # if there was no difference between the new subject tag/session note, then return error
    if not updated:
        return {
            "status": "error",
            "message": "No changes detected; session not updated."
        }

    # return success otherwise
    return {
        "status": "success",
        "message": "Session updated successfully."
    }


def delete_session(sessions, req):
    session_num = req["session_number"]

    # search for session with matching session number
    for session in sessions:

        # if found, delete the session and return success
        if session.get("session_number") == session_num:
            sessions.remove(session)
            return {
                "status": "success",
                "message": "Session deleted successfully."
            }

    # if not found, return error
    return {
        "status": "error",
        "message": "Failed to delete session; session does not exist."
    }


# set up ZeroMQ context and REP (reply) socket
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    request = socket.recv_json()

    # validate the base request
    if "session_number" not in request or "operation" not in request:
        socket.send_json({
            "status": "error",
            "message": "Request is missing session_number and operation parameters"
        })
        continue

    # get the session file from the request (defaults to study_sessions.json if filename not included)
    session_file = request.get("session_file", "study_sessions.json")

    # load the sessions from JSON file
    sessions_list = load_sessions(session_file)
    if sessions_list is None:
        socket.send_json({
            "status": "error",
            "message": "Could not load study session JSON file."
        })
        continue

    # determine the operation
    op = request["operation"].lower()

    # complete operation and save changes if successful
    # if "edit"
    if op == "edit":
        result = edit_session(sessions_list, request)
        if result["status"] == "success":
            result = save_session(session_file, sessions_list, "Session updated successfully.")
        socket.send_json(result)

    # if "delete"
    elif op == "delete":
        result = delete_session(sessions_list, request)
        if result["status"] == "success":
            result = save_session(session_file, sessions_list, "Session deleted successfully.")
        socket.send_json(result)

    # if some other operation
    else:
        socket.send_json({
            "status": "error",
            "message": f"Unknown operation: {op}"
        })
