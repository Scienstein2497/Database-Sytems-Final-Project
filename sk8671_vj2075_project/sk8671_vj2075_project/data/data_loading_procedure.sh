psql -d vj2075_db -a -f ../code/schema.sql
cat organizations.csv | psql -d pds-test-so-1 "COPY organizations from STDIN CSV HEADER"
cat schools.csv | psql -d pds-test-so-1 -c "COPY schools from STDIN CSV HEADER"        
cat departments.csv | psql -d pds-test-so-1 -c "COPY departments from STDIN CSV HEADER"
cat locations.csv | psql -d pds-test-so-1 -c "COPY locations from STDIN CSV HEADER"   
cat students.csv | psql -d pds-test-so-1 -c "COPY students from STDIN CSV HEADER"  
cat tag_categories.csv | psql -d pds-test-so-1 -c "COPY tag_categories from STDIN CSV HEADER"
cat tags.csv | psql -d pds-test-so-1 -c "COPY tags from STDIN CSV HEADER"            
cat questions.csv | psql -d pds-test-so-1 -c "COPY questions from STDIN CSV HEADER"  
cat tags_questions.csv | psql -d pds-test-so-1 -c "COPY tags_questions from STDIN CSV HEADER"
cat answers.csv | psql -d pds-test-so-1 -c "COPY answers from STDIN CSV HEADER"      
cat comments_answers.csv | psql -d pds-test-so-1 -c "COPY comments_answers from STDIN CSV HEADER"
cat comments_questions.csv | psql -d pds-test-so-1 -c "COPY comments_questions from STDIN CSV HEADER"