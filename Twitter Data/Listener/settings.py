TRACK_TERMS = ["bolsonaro","pt","golpe"]
CONNECTION_STRING = "sqlite:///politics_brazil2.db"
CSV_NAME = "politics_brazil2.csv"
TABLE_NAME = "politics_brazil2"

# ["trump", "clinton", "sanders", "hillary clinton", "bernie", "donald trump"] -- do tutorial

try:
    from private import *
except Exception:
    pass