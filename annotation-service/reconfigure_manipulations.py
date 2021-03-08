import pandas as pd
import sqlalchemy as sq
import sys
import random

# engine = sq.create_engine("postgresql+psycopg2://raldir:betaR!155943@localhost:5432/FeverAnnotationsDB")
engine = sq.create_engine("mysql+pymysql://raldir:betaR!155943@localhost/FeverAnnotationsDB")#/FeverAnnotationsDB?host=/var/lib/mysql/FeverAnnotationsDB/")

table_claim_data = pd.read_sql_table('ClaimAnnotationData', engine)

manipulation_list = ['More Specific', 'Generalization', 'Negation', 'Multiple Pages', 'Paraphrasing', 'Substitution']

claim_type = ['First claim', 'Second claim']

for index, row in table_claim_data.iterrows():
    if row['annotators_num'] > 0 or row['taken_flag'] == 1:
        continue
    else:
        selection_manipulation = random.choices(manipulation_list, weights=(10, 10, 25, 25, 5, 25), k=1)

        selection_claim = random.choice(claim_type)

        new_manipulation = selection_claim + ': ' + selection_manipulation[0]

        # print(new_manipulation)
        print("UPDATE ClaimAnnotationData SET manipulation= '{}' WHERE id = {};".format(new_manipulation, row['id']))
