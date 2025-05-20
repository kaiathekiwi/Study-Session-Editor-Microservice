import json

sessions = [
    {
        "session_number": 1,
        "subject_tag": None,
        "session_note": None
    },
    {
        "session_number": 2,
        "subject_tag": "MATH 111",
        "session_note": "Worked on integration techniques."
    },
    {
        "session_number": 3,
        "subject_tag": "MENU TEST",
        "session_note": "If you don't delete me something very bad will happen."
    }
]

with open("study_log.json", "w") as file:
    json.dump(sessions, file, indent=2)

print("study_log.json created.")
