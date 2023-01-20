CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;

-- Table: public.organizations

DROP TABLE IF EXISTS public.organizations;

CREATE TABLE IF NOT EXISTS public.organizations
(
    org_id uuid NOT NULL DEFAULT uuid_generate_v4() PRIMARY KEY,
    org_name character(128) COLLATE pg_catalog."default" NOT NULL UNIQUE
);

-- TABLESPACE pg_default;

-- ALTER TABLE IF EXISTS public.organizations
--     OWNER to postgres;





-- Table: public.schools

DROP TABLE IF EXISTS public.schools;

CREATE TABLE IF NOT EXISTS public.schools
(
    school_id uuid NOT NULL DEFAULT uuid_generate_v4() PRIMARY KEY,
    school_name character(128) NOT NULL UNIQUE,
    org_id uuid NOT NULL,
    FOREIGN KEY (org_id)
        REFERENCES public.organizations (org_id)
        ON DELETE CASCADE
);

-- TABLESPACE pg_default;

-- ALTER TABLE IF EXISTS public.schools
--     OWNER to postgres;



-- Table: public.departments

DROP TABLE IF EXISTS public.departments;

CREATE TABLE IF NOT EXISTS public.departments
(
    dept_id uuid NOT NULL DEFAULT uuid_generate_v4() PRIMARY KEY,
    dept_name character(128) NOT NULL,
    school_id uuid NOT NULL,
    FOREIGN KEY (school_id)
        REFERENCES public.schools (school_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- TABLESPACE pg_default;

-- ALTER TABLE IF EXISTS public.departments
--     OWNER to postgres;


-- Table: public.locations

-- DROP TABLE IF EXISTS public.locations;

CREATE TABLE IF NOT EXISTS public.locations
(
    location_id uuid NOT NULL DEFAULT uuid_generate_v4() PRIMARY KEY,
    address_line1 character(64) NOT NULL,
    address_line2 character(64),
    city character(32) NOT NULL,
    state character(32) NOT NULL,
    zipcode integer NOT NULL,
    country character(32) NOT NULL
);

-- TABLESPACE pg_default;

-- ALTER TABLE IF EXISTS public.locations
--     OWNER to postgres;




-- Table: public.students

DROP TABLE IF EXISTS public.students;

CREATE TABLE IF NOT EXISTS public.students
(
    sid uuid NOT NULL DEFAULT uuid_generate_v4() PRIMARY KEY,
    first_name character(32) NOT NULL,
    last_name character(32) NOT NULL,
    email character(64) NOT NULL UNIQUE,
    password character(64) NOT NULL,
    degree character(128),
    dept_id uuid NOT NULL,
    graduation_year bigint,
    location uuid NOT NULL,
    dob date,
    FOREIGN KEY (dept_id)
        REFERENCES public.departments (dept_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (location)
        REFERENCES public.locations (location_id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- TABLESPACE pg_default;

-- ALTER TABLE IF EXISTS public.students
--     OWNER to postgres;




-- Table: public.tag_categories

DROP TABLE IF EXISTS public.tag_categories;

CREATE TABLE IF NOT EXISTS public.tag_categories
(
    tc_id uuid NOT NULL DEFAULT uuid_generate_v4() PRIMARY KEY,
    category_name character(32) NOT NULL UNIQUE
);


-- Table: public.tags

DROP TABLE IF EXISTS public.tags;

CREATE TABLE IF NOT EXISTS public.tags
(
    tid uuid NOT NULL DEFAULT uuid_generate_v4() PRIMARY KEY,
    tag_name character(32) NOT NULL UNIQUE,
    tc_id uuid NOT NULL,
    FOREIGN KEY (tc_id)
        REFERENCES public.tag_categories (tc_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- TABLESPACE pg_default;

-- ALTER TABLE IF EXISTS public.tags
--     OWNER to postgres;


-- Table: public.questions
-- Table: public.questions

DROP TABLE IF EXISTS public.questions;

CREATE TABLE IF NOT EXISTS public.questions
(
    qid uuid NOT NULL DEFAULT uuid_generate_v4() PRIMARY KEY,
    body text NOT NULL,
    title character(64) NOT NULL UNIQUE,
    posted_by uuid NOT NULL,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    updated_by timestamp with time zone NOT NULL DEFAULT now(),
    FOREIGN KEY (posted_by)
        REFERENCES public.students (sid)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- TABLESPACE pg_default;

-- ALTER TABLE IF EXISTS public.questions
--     OWNER to postgres;



-- Table: public.answers

DROP TABLE IF EXISTS public.answers;

CREATE TABLE IF NOT EXISTS public.answers
(
    aid uuid NOT NULL DEFAULT uuid_generate_v4() PRIMARY KEY,
    body text COLLATE pg_catalog."default" NOT NULL,
    qid uuid NOT NULL,
    posted_by uuid NOT NULL,
    FOREIGN KEY (posted_by)
        REFERENCES public.students (sid)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (qid)
        REFERENCES public.questions (qid)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- TABLESPACE pg_default;

-- ALTER TABLE IF EXISTS public.answers
--     OWNER to postgres;


-- Table: public.tags_questions

DROP TABLE IF EXISTS public.tags_questions;

CREATE TABLE IF NOT EXISTS public.tags_questions
(
    qid uuid NOT NULL,
    tag_id uuid NOT NULL,
    qt_id uuid NOT NULL DEFAULT uuid_generate_v4() PRIMARY KEY,
    FOREIGN KEY (qid)
        REFERENCES public.questions (qid)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (tag_id)
        REFERENCES public.tags (tid)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- TABLESPACE pg_default;

-- ALTER TABLE IF EXISTS public.tags_questions
--     OWNER to postgres;


-- Table: public.comments_questions

DROP TABLE IF EXISTS public.comments_questions;

CREATE TABLE IF NOT EXISTS public.comments_questions
(
    comment_id uuid NOT NULL DEFAULT uuid_generate_v4() PRIMARY KEY,
    qid uuid NOT NULL,
    body character(256) NOT NULL UNIQUE,
    posted_by uuid NOT NULL,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    updated_at timestamp with time zone NOT NULL DEFAULT now(),
    FOREIGN KEY (posted_by)
        REFERENCES public.students (sid)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (qid)
        REFERENCES public.questions (qid)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- TABLESPACE pg_default;

-- ALTER TABLE IF EXISTS public.comments_questions
--     OWNER to postgres;


-- Table: public.comments_answers

-- DROP TABLE IF EXISTS public.comments_answers;

CREATE TABLE IF NOT EXISTS public.comments_answers
(
    comment_id uuid NOT NULL DEFAULT uuid_generate_v4() PRIMARY KEY,
    aid uuid NOT NULL,
    body character(256) NOT NULL UNIQUE,
    posted_by uuid NOT NULL,
    FOREIGN KEY (aid)
        REFERENCES public.answers (aid)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (posted_by)
        REFERENCES public.students (sid)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- TABLESPACE pg_default;

-- ALTER TABLE IF EXISTS public.comments_answers
--     OWNER to postgres;
