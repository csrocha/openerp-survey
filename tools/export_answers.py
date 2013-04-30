#!/usr/bin/python
# -*- coding: utf-8 -*-
import psycopg2
import csv

def list_inputs(cur):
        _q_input = """
                select QA.name, Q.variable_name, valid, input, message, formated
                        from survey_methodology_answer as A 
                        left join survey_methodology_question as Q on (A.question_id = Q.id) 
                        left join survey_methodology_questionnaire as QA on (A.questionnaire_id = QA.id) 
                        where type = 'Variable'
                        order by QA.name, Q.variable_name;
                """
        cur.execute(_q_input)
        for i in cur.fetchall():
                yield i

def list_variables(cur):
        _q_variables = """
                select variable_name from survey_methodology_question where type = 'Variable' order by complete_place;
        """
        cur.execute(_q_variables)
        return [ i[0] for i in cur.fetchall() ]

def iter_dump(iterator, out_csv):
        out_csv.writeheader()

        row = None
        questionaire = None

        for i in iterator:
                if questionaire !=  i[0]:
                        questionaire = i[0]
                        if row is not None:
                                out_csv.writerow(row)
                        row = dict( (k,None) for k in keys )
                        row['questionaire'] = questionaire
                row[i[1]] = i[2:]
        out_csv.writerow(row)
 
def dump_inputs(db_name, out_filename):
        conn = psycopg2.connect("dbname=%s" % db_name)
        cur = conn.cursor()

        keys = ['questionaire'] + list_variables(cur)

        out_file = open(out_filename, 'w')
        out_csv = csv.DictWriter(out_file, fieldnames=keys)

        iter_dump(list_inputs(cur), out_csv)

if __name__ == "__main__":
        db_name = "fop_v7_0"
        dump_inputs(db_name, 'inputs.csv')
                                



