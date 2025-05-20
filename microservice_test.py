# ----------------------------------------------------------------------------------------------------
# microservice_test.py
# ----------------------------------------------------------------------------------------------------
# Demonstrates that the microservice can be called and respond with data
# ----------------------------------------------------------------------------------------------------

import zmq
import time


def send_test(test_socket, description, request_data):
    print(f"\n[Test]\n-----{description}-----")
    test_socket.send_json(request_data)
    res = test_socket.recv_json()
    print(f"Response:\n{res}")
    time.sleep(2)  # small delay so it's easier to see


# set up ZeroMQ context and REQ (request) socket
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

# test 1: edit the subject tag and session note if subject tag and session note are initially None
send_test(socket, "Edit subject tag and session note of session #1 "
                  "(if subject tag and session note are initially None)",
          {
              "session_number": 1,
              "operation": "edit",
              "new_subject_tag": "CS 3",
              "new_session_note": "Reviewed differences between Agile, Waterfall, and Sprial/",
              "session_file": "study_log.json"
          })

# test 2: edit just the subject tag
send_test(socket, "Edit subject tag of session #1",
          {
              "session_number": 1,
              "operation": "edit",
              "new_subject_tag": "CS 361",
              "session_file": "study_log.json"
          })

# test 3: edit just the session note
send_test(socket, "Edit session note of session #1",
          {
              "session_number": 1,
              "operation": "edit",
              "new_session_note": "Reviewed differences between Agile, Waterfall, and Spiral.",
              "session_file": "study_log.json"
          })

# test 4: edit the subject tag and session note if the subject tag and session note are initially filled
send_test(socket, "Edit subject tag and session note of session #1"
                  "(if the subject tag and session note are initially filled)",
          {
              "session_number": 2,
              "operation": "edit",
              "new_subject_tag": "Evil 100",
              "new_session_note": "This is an evil session and should be destroyed at all costs!",
              "session_file": "study_log.json"
          })

# test 5: edit with no changes
send_test(socket, "Edit with no changes",
          {
              "session_number": 1,
              "operation": "edit",
              "new_subject_tag": "CS 361",
              "new_session_note": "Reviewed differences between Agile, Waterfall, and Spiral.",
              "session_file": "study_log.json"
          })

# test 6: missing required parameters (subject tag or session note)
send_test(socket, "Editing without a new subject tag or new session note",
          {
              "session_number": 1,
              "operation": "edit",
              "session_file": "study_log.json"
          })

# test 7: missing required parameters (session number)
send_test(socket, "Editing without a session number",
          {
              "operation": "edit",
              "new_subject_tag": "CS 361",
              "new_session_note": "Reviewed differences between Agile, Waterfall, and Spiral.",
              "session_file": "study_log.json"
          })

# test 8: session doesn't exist (edit)
send_test(socket, "Edit a non-existent session",
          {
              "session_number": 0,
              "operation": "edit",
              "new_subject_tag": "FAKE SUBJECT",
              "new_session_note": "This shouldn't exist.",
              "session_file": "study_log.json"
          })

# test 9: successful delete
send_test(socket, "Delete a session",
          {
              "session_number": 2,
              "operation": "delete",
              "new_subject_tag": "Evil 100",
              "new_session_note": "This is an evil session and should be destroyed at all costs!",
              "session_file": "study_log.json"
          })
# note: new_subject_tag and new_session_note are still included to demonstrate that they are not considered when
# deleting a session!

# test 10: session doesn't exist (delete)
send_test(socket, "Delete a non-existent session",
          {
              "session_number": 2,
              "operation": "delete",
              "session_file": "study_log.json"
          })
# note: new_subject_tag and new_session_note are not included to demonstrate that they are not considered when deleting
# a session!

# test 11: unknown operation
send_test(socket, "Unknown operation",
          {
              "session_number": 1,
              "operation": "explode",
              "new_subject_tag": "Evil 100",
              "new_session_note": "This is an evil session and should be destroyed at all costs!",
              "session_file": "study_log.json"
          })

# test 12: no operation
send_test(socket, "No operation",
          {
              "session_number": 1,
              "new_subject_tag": "HUH 200",
              "new_session_note": "What is going on???",
              "session_file": "study_log.json"
          })

# test 13: failed to load file
send_test(socket, "Fail to load file",
          {"session_number": 1,
           "new_subject_tag": "HUH 200",
           "new_session_note": "What is going on???",
           })

# test 14: testing a confirm functionality
print("\n-----[Test]-----\n-----Menu Simulation-----\n")

while True:
    print("Would you like to edit or delete a file?")
    print("\n[1] Delete a session\n[2] Edit a session note\n[3] Edit a subject tag\n")

    choice = input("Enter your choice (1, 2, or 3): ")

    if choice == "1":
        print("\n[Delete selected]\nPretend you selected a session to delete\n")
        print("Are you sure you want to delete [session 2]?")

        while True:
            print("\n[1] Yes")
            print("[2] No\n")

            confirm = input("Enter your choice (1 or 2): ")

            if confirm == "1":
                print("\n[Confirmed] Proceeding with changes . . .")
                deleting_data = {
                    "session_number": 3,
                    "operation": "delete",
                    "session_file": "study_log.json"
                }
                socket.send_json(deleting_data)
                response = socket.recv_json()
                print(f"Response:\n{response}")

            else:
                print("[Canceled] Returning to menu . . .")

            break
        break

    elif choice == "2":
        print("\nThis is just a test, why did you select this??")
        break

