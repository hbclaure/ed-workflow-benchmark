#place queries you want to explore here
QUERIES_EXP1 = [
    """
    ("emergency department*"[tiab] OR "emergency room*"[tiab]) AND
    ("time motion"[tiab] OR "time and motion"[tiab]
    OR "work sampling"[tiab] OR "work activities"[tiab]
    OR workflow*[tiab] OR "task analysis"[tiab])
    """,
    """
    ("emergency department*"[tiab] OR "emergency room*"[tiab])
    AND
    (communication[tiab] OR coordination[tiab]
    OR documentation[tiab] OR "decision making"[tiab])
    AND
    (observational[tiab] OR ethnograph*[tiab] OR workflow*[tiab])
    """,
    """
    ("emergency department*"[tiab] OR "emergency room*"[tiab])
    AND
    (transport*[tiab] OR restock*[tiab] OR clean*[tiab]
    OR logistics[tiab] OR "support staff"[tiab]
    OR "environmental services"[tiab] OR "supply management"[tiab])
    """

]

QUERIES_EXP2 = [
    """
    (
    "Emergency Service, Hospital"[MeSH]
    OR "emergency department"[tiab]
    OR "emergency room"[tiab]
    )
    AND
    (
    "time and motion"[tiab]
    OR "time-motion"[tiab]
    OR workflow[tiab]
    OR "task analysis"[tiab]
    OR "work sampling"[tiab]
    OR observation*[tiab]
    )
    """,
    """
    (
    "emergency department"[tiab]
    OR "emergency room"[tiab]
    )
    AND
    (
    nurs*[tiab]
    OR clinician*[tiab]
    OR technician*[tiab]
    OR "environmental services"[tiab]
    OR "patient transport"[tiab]
    )
    AND
    (
    activities[tiab]
    OR tasks[tiab]
    OR workflow[tiab]
    OR "time motion"[tiab]
    )
    """

]


