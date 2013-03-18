DBS=survey.db
TARGETS=addons/survey-methodology

.PRECIOUS: ${DBS}

all: addons

addons: ${TARGETS}

%.db: design/%.uml
	xmi2oerp -i $< -d $@

addons/%: %.db
	xmi2oerp -r -d $< -t addons -v 2

clean: clean-db clean-addons

clean-db:
	rm -rf ${DBS}

clean-addons:
	rm -rf ${TARGETS}

schemas: migration/sgr.sql

migration/sgr.sql:
	pg_dump -s test_db_sgrx -f $@

migration_restore: migration/sgr.sql
	-dropdb sgr
	createdb sgr
	psql sgr < migration/sgr.sql

question.dot: addons/survey_methodology_extra/data/questions.xml
	./tools/recover_questions.py

%.svg: %.dot
	dot -T svg -o $@ $<

dot: question.svg
	rsvg-view-3 $<


