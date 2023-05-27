--
-- PostgreSQL database dump
--

-- Dumped from database version 15.2
-- Dumped by pg_dump version 15.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: courses; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.courses (
    id integer NOT NULL,
    name character varying NOT NULL,
    schedule character varying(3)[],
    instrument_id integer NOT NULL
);


ALTER TABLE public.courses OWNER TO postgres;

--
-- Name: courses_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.courses_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.courses_id_seq OWNER TO postgres;

--
-- Name: courses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.courses_id_seq OWNED BY public.courses.id;


--
-- Name: instructor_course_relationship; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.instructor_course_relationship (
    instructor_id integer NOT NULL,
    course_id integer NOT NULL
);


ALTER TABLE public.instructor_course_relationship OWNER TO postgres;

--
-- Name: instructor_instrument_relationship; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.instructor_instrument_relationship (
    instructor_id integer NOT NULL,
    instrument_id integer NOT NULL
);


ALTER TABLE public.instructor_instrument_relationship OWNER TO postgres;

--
-- Name: instructors; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.instructors (
    id integer NOT NULL,
    first_name character varying NOT NULL,
    last_name character varying NOT NULL,
    schedule character varying(3)[] NOT NULL
);


ALTER TABLE public.instructors OWNER TO postgres;

--
-- Name: instructors_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.instructors_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.instructors_id_seq OWNER TO postgres;

--
-- Name: instructors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.instructors_id_seq OWNED BY public.instructors.id;


--
-- Name: instruments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.instruments (
    id integer NOT NULL,
    instrument character varying NOT NULL
);


ALTER TABLE public.instruments OWNER TO postgres;

--
-- Name: instruments_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.instruments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.instruments_id_seq OWNER TO postgres;

--
-- Name: instruments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.instruments_id_seq OWNED BY public.instruments.id;


--
-- Name: courses id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.courses ALTER COLUMN id SET DEFAULT nextval('public.courses_id_seq'::regclass);


--
-- Name: instructors id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.instructors ALTER COLUMN id SET DEFAULT nextval('public.instructors_id_seq'::regclass);


--
-- Name: instruments id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.instruments ALTER COLUMN id SET DEFAULT nextval('public.instruments_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
2aa572de219e
\.


--
-- Data for Name: courses; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.courses (id, name, schedule, instrument_id) FROM stdin;
1	Beginner Guitar	{Sun,Mon,Tue,Wed,Thu,Fri,Sat}	1
2	Advanced Guitar	{Mon,Tue,Wed,Thu,Fri}	1
3	Jazz Guitar	{Mon,Tue,Thu}	1
5	Beginner Bass	{Sun,Mon,Tue,Wed,Thu,Fri,Sat}	2
6	Advanced Bass	{Mon,Tue,Wed,Thu,Fri}	2
7	Jazz Bass	{Sun,Wed,Thu}	2
8	Beginner Drums	{Sun,Mon,Tue,Wed,Thu,Fri,Sat}	3
9	Advanced Drums	{Mon,Tue,Wed,Thu,Fri}	3
10	Jazz Drums	{Tue,Thu,Sat}	3
11	Beginner Piano	{Sun,Mon,Tue,Wed,Thu,Fri}	4
12	Classical Piano	{Tue,Wed,Fri}	4
13	Jazz Piano	{Mon,Thu,Sat}	4
14	Beginner Vocals	{Sun,Mon,Tue,Wed,Thu,Fri,Sat}	5
15	Advanced Vocals	{Mon,Tue,Wed,Thu,Fri,Sat}	5
16	Jazz Vocals	{Mon,Tue,Wed,Thu,Fri,Sat}	5
17	Banjo	{Mon,Tue,Wed,Thu,Fri}	6
18	Mandolin	{Mon,Wed,Fri}	7
19	Saxophone	{Sun,Mon,Tue,Wed,Thu,Fri}	8
20	Trumpet	{Sun,Mon,Wed,Thu,Fri}	9
4	Blues Guitar	{Tue,Fri,Sat}	1
\.


--
-- Data for Name: instructor_course_relationship; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.instructor_course_relationship (instructor_id, course_id) FROM stdin;
1	1
1	2
2	1
2	2
3	2
3	5
4	2
5	1
5	18
6	6
6	7
7	5
7	6
8	5
8	11
8	14
9	5
9	6
9	18
10	8
10	14
11	8
11	9
12	8
12	9
12	10
13	9
13	10
14	11
14	13
15	11
15	13
16	11
16	14
17	12
18	12
19	15
19	16
20	15
21	17
22	14
22	17
23	17
24	19
25	19
26	19
26	20
27	16
27	20
28	16
28	20
29	20
35	1
35	14
35	18
36	5
36	6
2	4
\.


--
-- Data for Name: instructor_instrument_relationship; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.instructor_instrument_relationship (instructor_id, instrument_id) FROM stdin;
1	1
1	5
2	1
3	1
4	1
5	1
5	5
5	7
6	2
7	2
8	1
8	2
8	3
8	4
8	5
9	2
9	4
9	7
10	3
10	5
11	3
12	3
13	3
14	4
15	4
16	4
16	5
17	4
18	4
19	5
20	5
21	5
21	6
22	5
22	6
23	6
24	8
25	8
26	8
26	9
27	5
27	9
28	5
28	9
29	9
35	1
35	5
35	7
36	2
36	1
36	5
36	3
36	4
35	17
\.


--
-- Data for Name: instructors; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.instructors (id, first_name, last_name, schedule) FROM stdin;
1	Jimi	Hendrix	{Sun,Tue,Wed,Thu}
2	Rosetta	Tharpe	{Mon,Tue,Fri,Sat}
3	Charlie	Christian	{Mon,Tue,Wed,Thu}
4	Tosin	Abasi	{Sun,Mon,Thu,Fri}
5	Jack	White	{Sun,Wed,Fri,Sat}
6	Jaco	Pastorius	{Sun,Tue,Wed,Thu}
7	Tina	Weymouth	{Sun,Wed,Fri,Sat}
8	Paul	McCartney	{Mon,Tue,Fri}
9	John Paul	Jones	{Mon,Thu,Fri,Sat}
10	Ringo	Starr	{Mon,Wed,Fri,Sat}
11	Danny	Carey	{Sun,Tue,Thu,Sat}
12	Max	Roach	{Sun,Mon,Thu,Fri}
13	Gene	Krupa	{Tue,Wed,Sat}
14	Thelonious	Monk	{Mon,Tue,Wed,Thu}
15	Bud	Powell	{Sun,Tue,Fri,Sat}
16	Billy	Joel	{Tue,Wed,Thu}
17	Bela	Bartok	{Sun,Tue,Wed,Fri}
18	Olga	Kern	{Mon,Thu,Fri,Sat}
19	Ella	Fitzgerald	{Sun,Tue,Thu,Sat}
20	Ariana	Grande	{Mon,Tue,Wed,Thu}
21	Kermit	Frog	{Sun,Mon,Tue,Wed}
22	Pete	Seeger	{Mon,Wed,Fri,Sat}
23	Steve	Martin	{Tue,Wed,Thu}
24	Charlie	Parker	{Sun,Tue,Thu}
25	John	Coltrane	{Mon,Wed,Thu,Fri}
26	Ornette	Coleman	{Mon,Tue,Fri,Sat}
27	Dizzy	Gillespie	{Sun,Tue,Wed,Fri}
28	Louis	Armstrong	{Mon,Wed,Sat}
29	Miles	Davis	{Sun,Wed,Thu,Fri}
35	Ian	Anderson	{Mon,Wed,Fri,Sat}
36	Kim	Deal	{Mon,Wed,Fri}
\.


--
-- Data for Name: instruments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.instruments (id, instrument) FROM stdin;
1	Guitar
2	Bass
3	Drums
4	Piano
5	Vocals
6	Banjo
7	Mandolin
8	Saxophone
9	Trumpet
12	Clarinet
17	Flute
\.


--
-- Name: courses_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.courses_id_seq', 21, true);


--
-- Name: instructors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.instructors_id_seq', 36, true);


--
-- Name: instruments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.instruments_id_seq', 21, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: courses courses_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.courses
    ADD CONSTRAINT courses_name_key UNIQUE (name);


--
-- Name: courses courses_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.courses
    ADD CONSTRAINT courses_pkey PRIMARY KEY (id);


--
-- Name: instructor_course_relationship instructor_course_relationship_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.instructor_course_relationship
    ADD CONSTRAINT instructor_course_relationship_pkey PRIMARY KEY (instructor_id, course_id);


--
-- Name: instructor_instrument_relationship instructor_instrument_relationship_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.instructor_instrument_relationship
    ADD CONSTRAINT instructor_instrument_relationship_pkey PRIMARY KEY (instructor_id, instrument_id);


--
-- Name: instructors instructors_first_name_last_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.instructors
    ADD CONSTRAINT instructors_first_name_last_name_key UNIQUE (first_name, last_name);


--
-- Name: instructors instructors_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.instructors
    ADD CONSTRAINT instructors_pkey PRIMARY KEY (id);


--
-- Name: instruments instruments_instrument_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.instruments
    ADD CONSTRAINT instruments_instrument_key UNIQUE (instrument);


--
-- Name: instruments instruments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.instruments
    ADD CONSTRAINT instruments_pkey PRIMARY KEY (id);


--
-- Name: courses courses_instrument_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.courses
    ADD CONSTRAINT courses_instrument_id_fkey FOREIGN KEY (instrument_id) REFERENCES public.instruments(id);


--
-- Name: instructor_course_relationship instructor_course_relationship_course_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.instructor_course_relationship
    ADD CONSTRAINT instructor_course_relationship_course_id_fkey FOREIGN KEY (course_id) REFERENCES public.courses(id);


--
-- Name: instructor_course_relationship instructor_course_relationship_instructor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.instructor_course_relationship
    ADD CONSTRAINT instructor_course_relationship_instructor_id_fkey FOREIGN KEY (instructor_id) REFERENCES public.instructors(id);


--
-- Name: instructor_instrument_relationship instructor_instrument_relationship_instructor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.instructor_instrument_relationship
    ADD CONSTRAINT instructor_instrument_relationship_instructor_id_fkey FOREIGN KEY (instructor_id) REFERENCES public.instructors(id);


--
-- Name: instructor_instrument_relationship instructor_instrument_relationship_instrument_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.instructor_instrument_relationship
    ADD CONSTRAINT instructor_instrument_relationship_instrument_id_fkey FOREIGN KEY (instrument_id) REFERENCES public.instruments(id);


--
-- PostgreSQL database dump complete
--

