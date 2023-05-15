--
-- PostgreSQL database dump
--

-- Dumped from database version 14.3
-- Dumped by pg_dump version 14.3

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
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: alex
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO alex;

--
-- Name: courses; Type: TABLE; Schema: public; Owner: alex
--

CREATE TABLE public.courses (
    id integer NOT NULL,
    name character varying NOT NULL,
    schedule character varying(3)[],
    instrument_id integer NOT NULL
);


ALTER TABLE public.courses OWNER TO alex;

--
-- Name: courses_id_seq; Type: SEQUENCE; Schema: public; Owner: alex
--

CREATE SEQUENCE public.courses_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.courses_id_seq OWNER TO alex;

--
-- Name: courses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: alex
--

ALTER SEQUENCE public.courses_id_seq OWNED BY public.courses.id;


--
-- Name: instructor_course_relationship; Type: TABLE; Schema: public; Owner: alex
--

CREATE TABLE public.instructor_course_relationship (
    instructor_id integer NOT NULL,
    course_id integer NOT NULL
);


ALTER TABLE public.instructor_course_relationship OWNER TO alex;

--
-- Name: instructor_instrument_relationship; Type: TABLE; Schema: public; Owner: alex
--

CREATE TABLE public.instructor_instrument_relationship (
    instructor_id integer NOT NULL,
    instrument_id integer NOT NULL
);


ALTER TABLE public.instructor_instrument_relationship OWNER TO alex;

--
-- Name: instructors; Type: TABLE; Schema: public; Owner: alex
--

CREATE TABLE public.instructors (
    id integer NOT NULL,
    first_name character varying NOT NULL,
    last_name character varying NOT NULL,
    schedule character varying(3)[] NOT NULL
);


ALTER TABLE public.instructors OWNER TO alex;

--
-- Name: instructors_id_seq; Type: SEQUENCE; Schema: public; Owner: alex
--

CREATE SEQUENCE public.instructors_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.instructors_id_seq OWNER TO alex;

--
-- Name: instructors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: alex
--

ALTER SEQUENCE public.instructors_id_seq OWNED BY public.instructors.id;


--
-- Name: instruments; Type: TABLE; Schema: public; Owner: alex
--

CREATE TABLE public.instruments (
    id integer NOT NULL,
    instrument character varying NOT NULL
);


ALTER TABLE public.instruments OWNER TO alex;

--
-- Name: instruments_id_seq; Type: SEQUENCE; Schema: public; Owner: alex
--

CREATE SEQUENCE public.instruments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.instruments_id_seq OWNER TO alex;

--
-- Name: instruments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: alex
--

ALTER SEQUENCE public.instruments_id_seq OWNED BY public.instruments.id;


--
-- Name: courses id; Type: DEFAULT; Schema: public; Owner: alex
--

ALTER TABLE ONLY public.courses ALTER COLUMN id SET DEFAULT nextval('public.courses_id_seq'::regclass);


--
-- Name: instructors id; Type: DEFAULT; Schema: public; Owner: alex
--

ALTER TABLE ONLY public.instructors ALTER COLUMN id SET DEFAULT nextval('public.instructors_id_seq'::regclass);


--
-- Name: instruments id; Type: DEFAULT; Schema: public; Owner: alex
--

ALTER TABLE ONLY public.instruments ALTER COLUMN id SET DEFAULT nextval('public.instruments_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: alex
--

COPY public.alembic_version (version_num) FROM stdin;
\.


--
-- Data for Name: courses; Type: TABLE DATA; Schema: public; Owner: alex
--

COPY public.courses (id, name, schedule, instrument_id) FROM stdin;
\.


--
-- Data for Name: instructor_course_relationship; Type: TABLE DATA; Schema: public; Owner: alex
--

COPY public.instructor_course_relationship (instructor_id, course_id) FROM stdin;
\.


--
-- Data for Name: instructor_instrument_relationship; Type: TABLE DATA; Schema: public; Owner: alex
--

COPY public.instructor_instrument_relationship (instructor_id, instrument_id) FROM stdin;
\.


--
-- Data for Name: instructors; Type: TABLE DATA; Schema: public; Owner: alex
--

COPY public.instructors (id, first_name, last_name, schedule) FROM stdin;
\.


--
-- Data for Name: instruments; Type: TABLE DATA; Schema: public; Owner: alex
--

COPY public.instruments (id, instrument) FROM stdin;
\.


--
-- Name: courses_id_seq; Type: SEQUENCE SET; Schema: public; Owner: alex
--

SELECT pg_catalog.setval('public.courses_id_seq', 21, true);


--
-- Name: instructors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: alex
--

SELECT pg_catalog.setval('public.instructors_id_seq', 36, true);


--
-- Name: instruments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: alex
--

SELECT pg_catalog.setval('public.instruments_id_seq', 21, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: alex
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: courses courses_name_key; Type: CONSTRAINT; Schema: public; Owner: alex
--

ALTER TABLE ONLY public.courses
    ADD CONSTRAINT courses_name_key UNIQUE (name);


--
-- Name: courses courses_pkey; Type: CONSTRAINT; Schema: public; Owner: alex
--

ALTER TABLE ONLY public.courses
    ADD CONSTRAINT courses_pkey PRIMARY KEY (id);


--
-- Name: instructor_course_relationship instructor_course_relationship_pkey; Type: CONSTRAINT; Schema: public; Owner: alex
--

ALTER TABLE ONLY public.instructor_course_relationship
    ADD CONSTRAINT instructor_course_relationship_pkey PRIMARY KEY (instructor_id, course_id);


--
-- Name: instructor_instrument_relationship instructor_instrument_relationship_pkey; Type: CONSTRAINT; Schema: public; Owner: alex
--

ALTER TABLE ONLY public.instructor_instrument_relationship
    ADD CONSTRAINT instructor_instrument_relationship_pkey PRIMARY KEY (instructor_id, instrument_id);


--
-- Name: instructors instructors_first_name_last_name_key; Type: CONSTRAINT; Schema: public; Owner: alex
--

ALTER TABLE ONLY public.instructors
    ADD CONSTRAINT instructors_first_name_last_name_key UNIQUE (first_name, last_name);


--
-- Name: instructors instructors_pkey; Type: CONSTRAINT; Schema: public; Owner: alex
--

ALTER TABLE ONLY public.instructors
    ADD CONSTRAINT instructors_pkey PRIMARY KEY (id);


--
-- Name: instruments instruments_instrument_key; Type: CONSTRAINT; Schema: public; Owner: alex
--

ALTER TABLE ONLY public.instruments
    ADD CONSTRAINT instruments_instrument_key UNIQUE (instrument);


--
-- Name: instruments instruments_pkey; Type: CONSTRAINT; Schema: public; Owner: alex
--

ALTER TABLE ONLY public.instruments
    ADD CONSTRAINT instruments_pkey PRIMARY KEY (id);


--
-- Name: courses courses_instrument_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: alex
--

ALTER TABLE ONLY public.courses
    ADD CONSTRAINT courses_instrument_id_fkey FOREIGN KEY (instrument_id) REFERENCES public.instruments(id);


--
-- Name: instructor_course_relationship instructor_course_relationship_course_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: alex
--

ALTER TABLE ONLY public.instructor_course_relationship
    ADD CONSTRAINT instructor_course_relationship_course_id_fkey FOREIGN KEY (course_id) REFERENCES public.courses(id);


--
-- Name: instructor_course_relationship instructor_course_relationship_instructor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: alex
--

ALTER TABLE ONLY public.instructor_course_relationship
    ADD CONSTRAINT instructor_course_relationship_instructor_id_fkey FOREIGN KEY (instructor_id) REFERENCES public.instructors(id);


--
-- Name: instructor_instrument_relationship instructor_instrument_relationship_instructor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: alex
--

ALTER TABLE ONLY public.instructor_instrument_relationship
    ADD CONSTRAINT instructor_instrument_relationship_instructor_id_fkey FOREIGN KEY (instructor_id) REFERENCES public.instructors(id);


--
-- Name: instructor_instrument_relationship instructor_instrument_relationship_instrument_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: alex
--

ALTER TABLE ONLY public.instructor_instrument_relationship
    ADD CONSTRAINT instructor_instrument_relationship_instrument_id_fkey FOREIGN KEY (instrument_id) REFERENCES public.instruments(id);


--
-- PostgreSQL database dump complete
--

