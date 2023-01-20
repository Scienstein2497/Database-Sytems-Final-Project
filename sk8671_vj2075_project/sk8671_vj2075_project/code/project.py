import logging
from configparser import ConfigParser
import pandas as pd
import psycopg2
import streamlit as st

logging.basicConfig(level=logging.DEBUG)

import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False

class DBHelper:

    @staticmethod
    @st.cache
    def __get_config(filename: str = "database.ini", section: str = "postgresql"):
        logging.info("DBHelper :: get_config() : start")
        logging.debug(f"filename: {filename}, section: {section}")

        parser = ConfigParser()
        parser.read(filename)
        configs = {k: v for k, v in parser.items(section)}

        logging.debug(f"configs: {configs}")
        logging.info("DBHelper :: get_config() : end")
        return configs

    @staticmethod
    @st.cache(suppress_st_warning=True)
    def query_db(sql: str):
        logging.info("DBHelper :: query_db() : start")
        logging.debug(f"sql: {sql}")

        db_info = DBHelper.__get_config()
        try:
            # Connect to an existing database
            conn = psycopg2.connect(**db_info)

            # Open a cursor to perform database operations
            cur = conn.cursor()

            # Execute a command
            cur.execute(sql)
        except Exception as e:
            st.write(e)

        # Obtain data
        data = cur.fetchall()
        logging.debug(f"data: {data}")

        column_names = [desc[0] for desc in cur.description]
        logging.debug(f"columns_names: {column_names}")

        # Make the changes to the database persistent
        conn.commit()

        # Close communication with the database
        cur.close()
        conn.close()

        df = pd.DataFrame(data=data, columns=column_names)
        logging.debug(f"df.shape: {df.shape}")

        logging.info("DBHelper :: query_db() : end")
        return df
    def insert_into_db(sql: str):
        logging.info("DBHelper :: insert_into_db() : start")
        logging.debug(f"sql: {sql}")

        db_info = DBHelper.__get_config()
        try:
            # Connect to an existing database
            conn = psycopg2.connect(**db_info)

            # Open a cursor to perform database operations
            cur = conn.cursor()

            # Execute a command
            cur.execute(sql)
        except Exception as e:
            st.write(e)
        # Make the changes to the database persistent
        conn.commit()
        # Close communication with the database
        cur.close()
        conn.close()
        return True


class DBIO:
    Organizations = "organizations"


    @staticmethod
    @st.cache(suppress_st_warning=True)
    def get_orgs() -> pd.DataFrame:
        print("inside get_orgs")
        logging.info("DBIO :: get_orgs : start")
        sql = f"""
            select org_name as name
            from {DBIO.Organizations}
            order by name
            limit 10;
        """
        logging.debug(sql)

        df = DBHelper.query_db(sql=sql)

        logging.debug(f"df.columns: {df.columns}")
        logging.debug(f"df.shape: {df.shape}")

        logging.info("DBIO :: get_users : end")
        return df
    def get_users() -> pd.DataFrame:
        print("inside get_users")
        logging.info("DBIO :: get_users : start")
        sql = f"""
            select s.first_name, s.email, l.address_line1, l.city
            from students s
            join locations l
            on s.location = l.location_id
            order by s.first_name;
        """
        logging.debug(sql)

        df = DBHelper.query_db(sql=sql)

        logging.debug(f"df.columns: {df.columns}")
        logging.debug(f"df.shape: {df.shape}")

        logging.info("DBIO :: get_users : end")
        st.write(df)

def home():
    pass
def intro():
    @st.cache(suppress_st_warning=True)
    def get_orgs() -> pd.DataFrame:
        print("inside get_orgs")
        logging.info("DBIO :: get_orgs : start")
        sql = f"""
            select org_name as name
            from {DBIO.Organizations}
            order by name
            limit 10;
        """
        logging.debug(sql)
        df = DBHelper.query_db(sql=sql)
        logging.debug(f"df.columns: {df.columns}")
        logging.debug(f"df.shape: {df.shape}")

        logging.info("DBIO :: get_orgs : end")
        return df
    st.subheader(DBIO.Organizations)
#         most_active = st.checkbox("most active users")
    organizations_df = get_orgs()
    st.write(organizations_df)

def signup():
	st.subheader("Create an Account")
	new_user = st.text_input('Enter your email')
	new_passwd = st.text_input('Password',type='password')
	if st.button('SignUp'):
	    add_student(new_user,make_hashes(new_passwd))
	    st.success("You have successfully created an account.Go to the Login Menu to login")

def add_student(email,password):
	print("inside add_student")
	logging.info("DBIO :: add_student : start")
# 	print("password", password)
	sql = f"""INSERT INTO students(email, password) VALUES ({email},{password})"""
	logging.debug(sql)
	df = DBHelper.query_db(sql=sql)
	logging.debug(f"df.columns: {df.columns}")
	logging.debug(f"df.shape: {df.shape}")
	logging.info("DBIO :: add_student : end")
	return df

def login():
	st.subheader("Login Section")

	email = st.sidebar.text_input("Email")
	password = st.sidebar.text_input("Password",type='password')
	if st.sidebar.checkbox("Login"):
		# if password == '12345':
# 		hashed_pswd = make_hashes(password)

# 		result = login_user(username,check_hashes(password,hashed_pswd))
		result = login_user(email, password)
		print(result)
		if len(result)!=0:
			result = result.iloc[0]
			st.success(f"Logged in as {result['first_name']} {result['last_name']}")
			st.success("Logged In as {}".format(email))
			answer_comment_posted_by = result['sid']
# 			st.write(answer_comment_posted_by)
# 			task = st.selectbox("Task",["Post a question","Post an answer","Post a comment"])
			task = st.selectbox("Action",["Post an answer"])
			if task == "Add Post":
				st.subheader("Add Your Post")

			elif task == "Post an answer":
				question_result = get_all_questions()
				st.subheader("Questions")
# 				questions = st.selectbox("Search Question By",["All", "Tags","Tag Categories"])
				questions = st.selectbox("Search Question By",["All"])
				if questions == "All":
					question_result = get_all_questions()
# 					st.write(question_result)
				elif questions == "Tags":
					question_result = get_all_questions_by_tag()
				elif questions == "Tag Categories":
					question_result = get_all_questions_by_tag_categories()
				j = 1
				for i in question_result.to_numpy().tolist():
					get_all_questions_markdown(i, j, answer_comment_posted_by)
					j += 1
			elif task == "Profiles":
				st.subheader("User Profiles")
				user_result = view_all_users()
				clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
				st.dataframe(clean_db)
		else:
			st.warning("Incorrect Username/Password")


def login_user(email,password):
	print("inside login_user")
	logging.info("DBIO :: login_user : start")
# 	print("password", password)
	sql = f"""SELECT * FROM students WHERE email ='{email}' AND password = '{password}'"""
	logging.debug(sql)
	df = DBHelper.query_db(sql=sql)
	logging.debug(f"df.columns: {df.columns}")
	logging.debug(f"df.shape: {df.shape}")
	logging.info("DBIO :: login_user : end")
	return df


def post_a_question():
# 	tag_category = st.selectbox("Select a tag category", get_all_tag_categories())
# 	if tag_category:
	st.selectbox("Select a tag", get_all_tags())


def get_all_questions():
	print("inside get_all_questions")
	logging.info("DBIO :: get_all_questions : start")
# 	print("password", password)
	sql = f"""
		select q.title as "Title", q.body as "Body", concat(s.first_name, s.last_name) as "Question Posted By",
	    t.tag_name as "Tag", tc.category_name as "Tag Category", q.qid
	    from questions q
	    join students s
	    on s.sid = q.posted_by
	    left join tags_questions tq
	    on tq.qid = q.qid
	    left join tags t
	    on t.tid = tq.tag_id
	    left join tag_categories tc
	    on tc.tc_id = t.tc_id
	    order by q.created_at DESC;
	"""
	logging.debug(sql)
	df = DBHelper.query_db(sql=sql)
	logging.debug(f"df.columns: {df.columns}")
	logging.debug(f"df.shape: {df.shape}")
	logging.info("DBIO :: get_all_questions : end")
	return df

def get_all_questions_markdown(i, j, answer_comment_posted_by):
	q_title = i[0]
	q_body = i[1]
	q_question_posted_by = i[2]
	t_tag_name = i[3]
	t_tag_category = i[4]
	q_qid = i[5]
	st.markdown(f"<h3>{j}.Question</h3>", unsafe_allow_html=True)
	st.markdown(f"<h4>{q_title}</h4>", unsafe_allow_html=True)
	st.markdown(f"{q_body}")
	st.markdown(f"Question Posted By - {q_question_posted_by}")
	st.markdown(f"Tag - {t_tag_name}")
	st.markdown(f"Tag Category - {t_tag_category}")
# 	st.markdown(q_qid)
# 	st.markdown(answer_comment_posted_by)
	if st.checkbox("Post your answer", key=j):
		print("here")
		answer_body = st.text_input('Enter your Answer')
		if st.button('Click here to post'):
			add_answer(answer_body,q_qid, answer_comment_posted_by)
			st.success("Your answer has been posted successfully")


def add_answer(body, qid, posted_by):
	print("inside add_answer")
	logging.info("DBIO :: add_answer : start")
# 	print("password", password)
	sql = f"""
		INSERT INTO answers(body, qid, posted_by) VALUES ('{body}','{qid}', '{posted_by}')
	"""
	logging.debug(sql)
	return DBHelper.insert_into_db(sql=sql)

def get_all_questions_by_tag():
	pass
def get_all_questions_by_tag_categories():
	pass

def get_all_tags() -> pd.DataFrame:
	print("inside get_all_tags")
	logging.info("DBIO :: get_all_tags : start")
	sql = "select tag_name from tags;"
	logging.debug(sql)
	df = DBHelper.query_db(sql=sql)
	logging.debug(f"df.columns: {df.columns}")
	logging.debug(f"df.shape: {df.shape}")
	logging.info("DBIO :: get_all_tags : end")
	return df

def get_all_tag_categories() -> pd.DataFrame:
	print("inside get_all_tags")
	logging.info("DBIO :: get_all_tags : start")
	sql = "select category_name from tag_categories;"
	logging.debug(sql)
	df = DBHelper.query_db(sql=sql)
	logging.debug(f"df.columns: {df.columns}")
	logging.debug(f"df.shape: {df.shape}")
	logging.info("DBIO :: get_all_tags : end")
	return df


def search_questions():
	st.subheader("Search Question")
	if st.button("Get all tags"):
		st.subheader("Tags")
		all_tags = get_all_tags()
		st.write(all_tags)
	if st.button("Get all Tag Categories"):
    		st.subheader("Tag Categories")
    		all_tags = get_all_tag_categories()
    		st.write(all_tags)
	search_term = str(st.text_input('Enter your question/tag'))
	search_choice = st.radio("Field to Search By",("Question Body","Tags", "Tag Category"))
	if st.button("Search"):
		if search_choice == "Question Body":
			questions_result = get_questions_by_body(search_term)
		elif search_choice == "Tags":
			questions_result = get_questions_by_tag(search_term)
		elif search_choice == "Tag Category":
			questions_result = get_questions_by_tag_category(search_term)
		st.write(questions_result)
# 		for i in questions_result.to_numpy().tolist():
# 			get_questions_by_body_markdown(i)

def sql_for_question_body_tag_tag_category(key, value):
	sql = f"""
		select q.qid, q.title, q.body, concat(s.first_name, s.last_name) as question_posted_by, cq.body as comment,
        concat(s2.first_name, s2.last_name) as comment_posted_by,
        ans.body as answer, concat(s1.first_name, s1.last_name) as answer_posted_by,
        t.tag_name, tc.category_name as tag_category from questions q
        join students s
        on s.sid = q.posted_by
        left join tags_questions tq
        on tq.qid = q.qid
        left join tags t
        on t.tid = tq.tag_id
        left join answers ans
        on ans.qid = q.qid
        join students s1
        on s1.sid = ans.posted_by
        left join comments_questions cq
        on cq.qid = q.qid
        join students s2
        on s2.sid = cq.posted_by
        left join tag_categories tc
        on tc.tc_id = t.tc_id
        where {key} like '%{value}%'
        order by q.created_at desc, cq.created_at desc;
	"""
	return sql

def get_questions_by_body(body) -> pd.DataFrame:
	print("inside get_questions_by_body")
	logging.info("DBIO :: get_questions_by_body : start")
	sql = sql_for_question_body_tag_tag_category("q.body", body)
	logging.debug(sql)
	df = DBHelper.query_db(sql=sql)
	logging.debug(f"df.columns: {df.columns}")
	logging.debug(f"df.shape: {df.shape}")
	logging.info("DBIO :: get_questions_by_body : end")
	return df
def get_questions_by_body_markdown(i):
	q_title = i[0]
	q_body = i[1]
	q_question_posted_by = i[2]
	st.markdown("<h3>Question</h3>", unsafe_allow_html=True)
	st.markdown(f"<h4>{q_title}</h4>", unsafe_allow_html=True)
	st.markdown(f"{q_body}")
	st.markdown(f"Question Posted By - {q_question_posted_by}")


def get_questions_by_tag(tag) -> pd.DataFrame:
	print("inside get_questions_by_tag")
	logging.info("DBIO :: get_questions_by_tag : start")
	sql = sql_for_question_body_tag_tag_category("t.tag_name", tag)
	logging.debug(sql)
	df = DBHelper.query_db(sql=sql)
	logging.debug(f"df.columns: {df.columns}")
	logging.debug(f"df.shape: {df.shape}")
	logging.info("DBIO :: get_questions_by_tag : end")
	return df
def get_questions_by_tag_markdown(i):
	q_title = i[0]
	q_body = i[1]
	q_question_posted_by = i[2]
	st.markdown("<h3>Question</h3>", unsafe_allow_html=True)
	st.markdown(f"<h4>{q_title}</h4>", unsafe_allow_html=True)
	st.markdown(f"{q_body}")
	st.markdown(f"Question Posted By - {q_question_posted_by}")

def get_questions_by_tag_category(tag) -> pd.DataFrame:
	print("inside get_questions_by_tag_category")
	logging.info("DBIO :: get_questions_by_tag_category : start")
	sql = sql_for_question_body_tag_tag_category("tc.category_name", tag)
	logging.debug(sql)
	df = DBHelper.query_db(sql=sql)
	logging.debug(f"df.columns: {df.columns}")
	logging.debug(f"df.shape: {df.shape}")
	logging.info("DBIO :: get_questions_by_tag_category : end")
	return df
def get_questions_by_tag_category_markdown(i):
	q_title = i[0]
	q_body = i[1]
	q_question_posted_by = i[2]
	st.markdown("<h3>Question</h3>", unsafe_allow_html=True)
	st.markdown(f"<h4>{q_title}</h4>", unsafe_allow_html=True)
	st.markdown(f"{q_body}")
	st.markdown(f"Question Posted By - {q_question_posted_by}")

def users():
    st.subheader("All Students")
    user_result = get_students()
    j = 0
    for i in user_result.to_numpy().tolist():
        j += 1
        get_student_markdown(i, j)


def get_students() -> pd.DataFrame:
    print("inside get_students")
    logging.info("DBIO :: get_students : start")
    sql = f"""
        select s.first_name, s.last_name, s.email, s.degree, s.graduation_year,
        s.dob, l.address_line1, l.address_line2, l.city, l.state, l.zipcode,
        l.country, dept.dept_name, school.school_name, org.org_name, s.sid
        from students s
        join locations l
        on s.location = l.location_id
        join departments dept
        on dept.dept_id = s.dept_id
        join schools school
        on school.school_id = dept.school_id
        join organizations org
        on org.org_id = school.org_id;
    """
    logging.debug(sql)
    df = DBHelper.query_db(sql=sql)
    logging.debug(f"df.columns: {df.columns}")
    logging.debug(f"df.shape: {df.shape}")
    logging.info("DBIO :: get_students : end")
    return df

def get_student_markdown(i, j):
	s_first_name = i[0]
	s_last_name = i[1]
	s_email = i[2]
	s_degree = i[3]
	s_graduation_year = i[4]
	s_dob = i[5]
	l_address_line1 = i[6]
	l_address_line2 = i[7]
	l_city = i[8]
	l_state = i[9]
	l_zipcode = i[10]
	l_country = i[11]
	dept_dept_name = i[12]
	school_school_name = i[13]
	org_org_name = i[14]
	st.markdown(f"<h1>{j}. {s_first_name} {s_last_name}</h1", unsafe_allow_html=True)
	st.markdown(f"Email - {s_email}", unsafe_allow_html=True)
	st.markdown(f"""
		Date of Birth - {s_dob}""",
		unsafe_allow_html=True)
	st.markdown(f"""
		Degree - {s_degree}, {s_graduation_year}""",
		unsafe_allow_html=True)
	st.markdown(f"""
		<h5>Address</h5> {l_address_line1}\n{l_address_line2}\n{l_city}, {l_state} - {l_zipcode}\n{l_country}""",
		unsafe_allow_html=True)
	st.markdown(f"""
		<h5>School Info</h5> {dept_dept_name}, {school_school_name},\n{org_org_name}""",
		unsafe_allow_html=True)
	st.markdown(f"""\n\n\n\n\n\n\n\n""")
	s_sid = i[15]
	activity_choice = st.radio("Activity",("Questions asked","Question answered", "Commented on Questions", "Commented on Answers"), key=s_sid)
	if activity_choice == "Questions asked":
		question_result = get_questions_by_sid(s_sid)
		j = 1
		for question in question_result.to_numpy().tolist():
			get_questions_by_sid_markdown(question, j)
			j += 1
	elif activity_choice == "Question answered":
		answer_result = get_answers_by_sid(s_sid)
		j = 1
		for answer in answer_result.to_numpy().tolist():
			get_answers_by_sid_markdown(answer, j)
			j += 1
	elif activity_choice == "Commented on Questions":
		comment_question_result = get_comments_questions_by_sid(s_sid)
		j = 1
		for comment_question in comment_question_result.to_numpy().tolist():
			get_comments_questions_by_sid_markdown(comment_question, j)
			j += 1
	elif activity_choice == "Commented on Answers":
		comment_answer_result = get_comments_answers_by_sid(s_sid)
		j = 1
		for comment_answer in comment_answer_result.to_numpy().tolist():
			get_comments_answers_by_sid_markdown(comment_answer, j)
			j += 1

def get_questions_by_sid(sid):
    print("inside get_questions_by_sid")
    logging.info("DBIO :: get_questions_by_sid : start")
    sql = f"""
	    select q.title, q.body, concat(s1.first_name, s1.last_name) as question_posted_by
        from questions q
        join students s1
        on s1.sid = q.posted_by
        where q.posted_by = '{sid}';
	"""
    logging.debug(sql)
    df = DBHelper.query_db(sql=sql)
    logging.debug(f"df.columns: {df.columns}")
    logging.debug(f"df.shape: {df.shape}")
    logging.info("DBIO :: get_questions_by_sid : end")
    return df



def get_questions_by_sid_markdown(i, j):
	q_title = i[0]
	q_body = i[1]
	q_question_posted_by = i[2]
	st.markdown(f"<h3>{j}.Question</h3>", unsafe_allow_html=True)
	st.markdown(f"<h4>{q_title}</h4>", unsafe_allow_html=True)
	st.markdown(f"{q_body}")
	st.markdown(f"Question Posted By - {q_question_posted_by}")


def get_answers_by_sid(sid):
    print("inside get_answers_by_sid")
    logging.info("DBIO :: get_answers_by_sid : start")
    sql = f"""
			select q.title, q.body as question, ans.body as answer, concat(s1.first_name, s1.last_name) as question_posted_by,
			concat(s2.first_name, s2.last_name) as ans_answer_posted_by
			from answers ans
			join  questions q
			on ans.qid = q.qid
			join students s1
			on s1.sid = q.posted_by
			join students s2
			on s2.sid = ans.posted_by
			where ans.posted_by = '{sid}';
		"""
    logging.debug(sql)
    df = DBHelper.query_db(sql=sql)
    logging.debug(f"df.columns: {df.columns}")
    logging.debug(f"df.shape: {df.shape}")
    logging.info("DBIO :: get_answers_by_sid : end")
    return df

def get_answers_by_sid_markdown(i, j):
	q_title = i[0]
	q_body = i[1]
	ans_body = i[2]
	q_question_posted_by = i[3]
	ans_answer_posted_by = i[4]
	st.markdown(f"<h3>{j}.Answer</h3>", unsafe_allow_html=True)
	st.markdown(f"<h4>{q_title}</h4>", unsafe_allow_html=True)
	st.markdown(f"{q_body}")
	st.markdown(f"Question Posted By - {q_question_posted_by}")
	st.markdown(f"{ans_body}")
	st.markdown(f"Answer Posted By - {ans_answer_posted_by}")

def get_comments_questions_by_sid(sid):
    print("inside get_comments_questions_by_sid")
    logging.info("DBIO :: get_comments_questions_by_sid : start")
    sql = f"""
        select q.title as title, q.body as question, concat(s1.first_name, s1.last_name) as question_posted_by,
        cq.body as comment, concat(s2.first_name, s2.last_name) as comment_posted_by
        from questions q
        left join comments_questions cq
        on cq.qid = q.qid
        join students s1
        on q.posted_by = s1.sid
        join students s2
        on cq.posted_by = s2.sid
        where cq.posted_by = '{sid}'
        order by q.body;
	"""
    logging.debug(sql)
    df = DBHelper.query_db(sql=sql)
    logging.debug(f"df.columns: {df.columns}")
    logging.debug(f"df.shape: {df.shape}")
    logging.info("DBIO :: get_comments_questions_by_sid : end")
    return df

def get_comments_questions_by_sid_markdown(i, j):
	q_title = i[0]
	q_body = i[1]
	q_question_posted_by = i[2]
	cq_comment_body = i[3]
	cq_comment_posted_by = i[4]
	st.markdown(f"<h3>{j}.Question</h3>", unsafe_allow_html=True)
	st.markdown(f"<h4>{q_title}</h4>", unsafe_allow_html=True)
	st.markdown(f"{q_body}")
	st.markdown(f"Question Posted By - {q_question_posted_by}")
	st.markdown(f"Comments - {cq_comment_body}")
	st.markdown(f"Comment Posted By - {cq_comment_posted_by}")

def get_comments_answers_by_sid(sid):
    print("inside get_comments_answers_by_sid")
    logging.info("DBIO :: get_comments_answers_by_sid : start")
    sql = f"""
            select q.title, q.body as question, concat(s3.first_name, s3.last_name) as question_posted_by,
            ans.body as answer, concat(s1.first_name, s1.last_name) as ans_posted_by,
            ca.body as comment, concat(s2.first_name, s2.last_name) as comment_posted_by
            from answers ans
            left join comments_answers ca
            on ca.aid = ans.aid
            join students s1
            on ans.posted_by = s1.sid
            join students s2
            on ca.posted_by = s2.sid
            join questions q
            on q.qid = ans.qid
            join students s3
            on q.posted_by = s3.sid
            where ca.posted_by = '{sid}'
            order by ans.body;
		"""
    logging.debug(sql)
    df = DBHelper.query_db(sql=sql)
    logging.debug(f"df.columns: {df.columns}")
    logging.debug(f"df.shape: {df.shape}")
    logging.info("DBIO :: get_comments_answers_by_sid : end")
    return df


def get_comments_answers_by_sid_markdown(i, j):
	q_title = i[0]
	q_body = i[1]
	q_question_posted_by = i[2]
	ans_body = i[3]
	ans_answer_posted_by = i[4]
	ca_comment_body = i[5]
	ca_comment_posted_by = i[6]
	st.markdown(f"<h3>{j}.Question</h3>", unsafe_allow_html=True)
	st.markdown(f"<h4>{q_title}</h4>", unsafe_allow_html=True)
	st.markdown(f"{q_body}")
	st.markdown(f"Question Posted By - {q_question_posted_by}")
	st.markdown(f"Answer - {ans_body}")
	st.markdown(f"Answer Posted By - {ans_answer_posted_by}")
	st.markdown(f"Comments - {ca_comment_body}")
	st.markdown(f"Comment Posted By - {ca_comment_posted_by}")

def search_users():
    def get_sql(key, value) -> str:
        sql = f"""
	        select s.first_name, s.last_name, s.email, s.degree, s.graduation_year,
			s.dob, l.address_line1, l.address_line2, l.city, l.state, l.zipcode,
			l.country, dept.dept_name, school.school_name, org.org_name, s.sid
			from students s
			join locations l
			on s.location = l.location_id
			join departments dept
			on dept.dept_id = s.dept_id
			join schools school
			on school.school_id = dept.school_id
			join organizations org
			on org.org_id = school.org_id
			where s.{key} like '%{value}%';
		"""
        return sql
    def get_user_by_name(name) -> pd.DataFrame:
        print("inside get_user_by_name")
        logging.info("DBIO :: get_user_by_name : start")
        sql = get_sql("first_name", name)
        logging.debug(sql)
        df = DBHelper.query_db(sql=sql)
        logging.debug(f"df.columns: {df.columns}")
        logging.debug(f"df.shape: {df.shape}")
        logging.info("DBIO :: get_user_by_name : end")
        return df
    def get_user_by_email(email) -> pd.DataFrame:
        print("inside get_user_by_email")
        logging.info("DBIO :: get_user_by_email : start")
        sql = get_sql("email", email)
        logging.debug(sql)
        df = DBHelper.query_db(sql=sql)
        logging.debug(f"df.columns: {df.columns}")
        logging.debug(f"df.shape: {df.shape}")
        logging.info("DBIO :: get_user_by_email : end")
        return df
    st.subheader("Search Users")
    search_term = st.text_input('Enter Search User')
    search_choice = st.radio("Field to Search By",("first name","email"))
    if st.button("Search"):
        if search_choice == "first name":
            user_result = get_user_by_name(search_term)
        elif search_choice == "email":
            user_result = get_user_by_email(search_term)
        j = 1
        for i in user_result.to_numpy().tolist():
            get_student_markdown(i, j)
            j += 1
def plotting_demo():
    pass
def mapping_demo():
    pass
def data_frame_demo():
    pass


def main():
    st.set_page_config(
        page_title="Stack Overflow",
        page_icon="👋",
    )
    st.write("# Welcome to Stack Overflow! 👋")

    st.sidebar.success("Select a option from the Menu")
    page_names_to_funcs = {
        "Home": home,
        "Users": users,
        "Search User": search_users,
        "Log In": login,
        "Search a question": search_questions,
    }
    demo_name = st.sidebar.selectbox("Choose an option", page_names_to_funcs.keys())
    page_names_to_funcs[demo_name]()


if __name__ == '__main__':
	main()
