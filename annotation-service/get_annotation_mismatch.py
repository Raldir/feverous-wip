import pandas as pd
import sqlalchemy as sq
import sys
from datetime import datetime
import json

# if len(sys.argv) > 2:
#     time_start = sys.argv[2]
#     time_start  = datetime.strptime(time_start, '%Y-%m-%d')
# if len(sys.argv) > 3:
#     time_end = sys.argv[3]
#     time_end  = datetime.strptime(time_end, '%Y-%m-%d')

# engine = sq.create_engine("postgresql+psycopg2://raldir:betaR!155943@localhost:5432/FeverAnnotationsDB")
engine = sq.create_engine("mysql+pymysql://raldir:betaR!155943@localhost/FeverAnnotationsDB")#/FeverAnnotationsDB?host=/var/lib/mysql/FeverAnnotationsDB/")

table_evidence  = pd.read_sql_table('CalibrationEvidence', engine)
table_claims = pd.read_sql_table('CalibrationClaims', engine)
table_claim_data = pd.read_sql_table('CalibrationClaimAnnotationData', engine)

mismatched_pairs = []

# for index, row in table_evidence.iterrows():
#     evidence1 = row['evidence1']
#     evidence1 = set(evidence1.split(' [SEP] '))
#     for index_sec, row_sec in table_evidence.iterrows():
#         if index_sec < index:
#             continue
#         if row['claim'] == row_sec['claim'] and row['id'] != row_sec['id']:
#             evidence1_sec = row_sec['evidence1']
#             evidence1_sec = set(evidence1_sec.split(' [SEP] '))
#             if evidence1 != evidence1_sec:
#                 print(evidence1, evidence1_sec)
#                 mismatched_pairs.append((row['id'], row_sec['id']))

for index, row in table_evidence.iterrows():
    evidence1 = row['verdict']
    for index_sec, row_sec in table_evidence.iterrows():
        if index_sec < index:
            continue
        if row['claim'] == row_sec['claim'] and row['id'] != row_sec['id']:
            evidence1_sec = row_sec['verdict']
            if evidence1 != evidence1_sec:
                mismatched_pairs.append((row['id'], row_sec['id']))

with open('evidence_annotation_verdict_mismatches.json', 'w') as outfile:
    json.dump(mismatched_pairs, outfile)
