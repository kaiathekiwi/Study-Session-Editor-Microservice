# Study Session Editor Microservice

This microservice enables programs to edit or delete study session entries stored in a JSON file. The client sends a request to change or remove a session, and receives a success or error message in response.

## Protocol Summary
**Communication Style**: ZeroMQ REQ/REP (Request-Reply) 

**Transport**: TCP

**Server Bind Address**: `tcp://*:5555`

**Message Format**: JSON (sent and received via send_json/recv_json)

**Data Format**: JSON objects

## How to REQUEST Data (Client ⟶ Microservice)

Your application must:
- Create a ZeroMQ Context (i.e. `context = zmq.Context()`)
- Open a REQ socket (i.e. `socket = context.socket(zmq.REQ)`)
- Connect it to the server's address (i.e. `socket.connect("tcp://localhost:5555")`)
- send a .json object using `socket.send_json()` containing a dictionary with at least the required fields

Use a ZeroMQ REQ socket to send a JSON object dictionary containing the following fields:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `session_number` | integer | :white_check_mark: | Identifies which study session to modify |
| `operation` | string | :white_check_mark: | "edit" or "delete" |
| `new_subject_tag` | string | :x: (*see note) | New subject tag (if editing) |
| `new_session_note` | string | :x: (*see note) | New session note (if editing) |
| `session_file` | string | :x: | Path to session file (default: study_sessions.json) |

**Note:** For the "edit" operation, at least one of the `new_subject_tag` or `new_session_note` must be included. If neither is provided, the microservice will return an error.

### Example call:
```
socket.send_json({
    "session_number": 1,
    "operation": "edit",
    "new_subject_tag": "CS 361",
    "new_session_note": "Reviewed Agile vs Waterfall.",
    "session_file": "study_log.json"
})
```

## How to RECEIVE Data (Microservice ⟶ Client)

After sending the request, the client must wait for the server to respond using `recv_json()`.

### Example call
```
response = socket.recv_json()
response_dict = json.load(response)  # converts the JSON object into a dictionary and saves it to "sessions" variable
```

Once received, the JSON object is parsed into a dictionary so your application can work with the status and message key-value pairs. It is suggested to use this with code like `response_dict.get("status")` to retreive the status value.

The message values may vary, however the only possible status values are "success" and "error". As such, your program should check the "status" field to determine if the operation succeeded. The message should only be used for debugging.

### Example success response
```
{
"status": "success",
"message": "Session updated successfully."
}
```
### Example error response
```
{
"status": "error",
"message": "Could not load study session JSON file."
}
```

## UML Diagram

![image](https://github.com/user-attachments/assets/d98e83c8-f3fc-4229-8594-e991ffa5701b)

## File Descriptions

**microservice_a.py** - Contains the microservice for use with a main program

**microservice_test.py** - Contains the various tests for rigorous examples of possible responses and requests

**json maker.py** - Contains a basic program to reset the test study session JSON file for re-running microservice_test.py

**study_log.json** - The test study session JSON file for using with the microservice_test.py
