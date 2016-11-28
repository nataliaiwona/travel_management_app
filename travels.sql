--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.4
-- Dumped by pg_dump version 9.5.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'LATIN1';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: locations; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE locations (
    id integer NOT NULL,
    city character varying(100) NOT NULL,
    state character varying(100),
    country character varying(100) NOT NULL,
    latitude double precision,
    longitude double precision
);


ALTER TABLE locations OWNER TO vagrant;

--
-- Name: locations_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE locations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE locations_id_seq OWNER TO vagrant;

--
-- Name: locations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE locations_id_seq OWNED BY locations.id;


--
-- Name: pin_types; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE pin_types (
    id integer NOT NULL,
    description character varying(50) NOT NULL
);


ALTER TABLE pin_types OWNER TO vagrant;

--
-- Name: pin_types_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE pin_types_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE pin_types_id_seq OWNER TO vagrant;

--
-- Name: pin_types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE pin_types_id_seq OWNED BY pin_types.id;


--
-- Name: pins; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE pins (
    id integer NOT NULL,
    user_id integer,
    pin_type_id integer,
    location_id integer
);


ALTER TABLE pins OWNER TO vagrant;

--
-- Name: pins_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE pins_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE pins_id_seq OWNER TO vagrant;

--
-- Name: pins_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE pins_id_seq OWNED BY pins.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE users (
    id integer NOT NULL,
    fname character varying(50),
    lname character varying(50),
    email character varying(64) NOT NULL,
    password character varying(500) NOT NULL
);


ALTER TABLE users OWNER TO vagrant;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE users_id_seq OWNER TO vagrant;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE users_id_seq OWNED BY users.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY locations ALTER COLUMN id SET DEFAULT nextval('locations_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY pin_types ALTER COLUMN id SET DEFAULT nextval('pin_types_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY pins ALTER COLUMN id SET DEFAULT nextval('pins_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY users ALTER COLUMN id SET DEFAULT nextval('users_id_seq'::regclass);


--
-- Data for Name: locations; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY locations (id, city, state, country, latitude, longitude) FROM stdin;
1	Pago Pago	\N	American Samoa	-14.2756000000000007	-170.701999999999998
2	Buenos Aires	\N	Argentina	-34.6037000000000035	-58.3815999999999988
4	Rio de Janeiro	State of Rio de Janeiro	Brazil	-22.9068466999999991	-43.1728964999999789
5	Catalão	Goiás	Brazil	-18.1660958000000008	-47.9444844999999873
6	Belo Horizonte	State of Minas Gerais	Brazil	-19.9166813000000005	-43.9344930999999974
7	São Paulo	State of São Paulo	Brazil	-23.5505199000000012	-46.6333094000000301
8	Mendoza	Mendoza Province	Argentina	-32.8894586999999987	-68.8458385999999791
9	Santiago	Santiago Metropolitan Region	Chile	-33.4378304999999969	-70.6504492000000255
10	Patagonia	Departamento del Beni	Bolivia	-12.4000000000000004	-65.6499999999999773
11	Bogotá	Bogota	Colombia	4.71098859999999942	-74.0720919999999978
12	Mexico City	Mexico City	Mexico	19.4326076999999984	-99.1332079999999678
13	Lima District	Lima Region	Peru	-12.0463740000000001	-77.0427933999999937
14	Easter Island	Valparaiso Region	Chile	-27.0889844999999987	-109.354527000000019
15	Orlando	Florida	United States	28.5383354999999987	-81.3792364999999904
16	Gary	Indiana	United States	41.5933696000000026	-87.3464271000000281
17	Detroit	Michigan	United States	42.3314269999999908	-83.0457538
18	Chicago	Illinois	United States	41.8781135999999989	-87.629798199999982
19	Minneapolis	Minnesota	United States	44.9777529999999999	-93.2650108000000273
20	New York	New York	United States	40.7127837000000028	-74.0059413000000177
21	Portland	Oregon	United States	45.5230622000000125	-122.676481599999988
22	Vancouver	Washington	United States	45.6387281000000016	-122.661486099999991
23	San Diego	California	United States	32.7157380000000018	-117.161083800000029
24	San Francisco	California	United States	37.7749294999999989	-122.419415500000014
25	Austin	Texas	United States	30.2671530000000004	-97.7430607999999665
26	Tucson	Arizona	United States	32.2217429000000024	-110.926478999999972
27	Panama City Beach	Florida	United States	30.1765913999999995	-85.8054879000000028
28	Philadelphia	Pennsylvania	United States	39.9525839000000005	-75.1652215000000297
29	Mackinac Island	Michigan	United States	45.8491796000000065	-84.6189339000000018
30	Grand Canyon Village	Arizona	United States	36.0544445000000024	-112.140110800000002
31	Las Vegas	Nevada	United States	36.1699411999999967	-115.139829599999985
32	Nashville	Tennessee	United States	36.1626637999999971	-86.7816015999999877
33	New Orleans	Louisiana	United States	29.9510657999999914	-90.0715323000000012
34	Butte	Montana	United States	46.0038231999999994	-112.534777599999984
35	Toronto	Ontario	Canada	43.6532259999999965	-79.3831842999999822
36	Seattle	Washington	United States	47.6062094999999985	-122.332070799999997
37	Lisbon	Lisbon	Portugal	38.7222524000000021	-9.13933659999997872
38	Monaco-Ville	\N	Monaco	43.7374109999999874	7.42081600000005892
39	Zagreb	City of Zagreb	Croatia	45.8150108000000031	15.9819190000000617
40	Dubrovnik	Dubrovnik-Neretva County	Croatia	42.6506605999999877	18.0944237999999586
41	Split	Split-Dalmatia County	Croatia	43.5081322999999998	16.4401934999999639
42	Kraków	Lesser Poland Voivodeship	Poland	50.0646500999999873	19.9449799000000212
43	Warsaw	Masovian Voivodeship	Poland	52.2296756000000002	21.012228700000037
44	Barcelona	Catalonia	Spain	41.3850638999999916	2.17340349999994942
45	Porto	Porto District	Portugal	41.1579437999999982	-8.62910529999999198
46	Madrid	Community of Madrid	Spain	40.4167753999999988	-3.70379019999995762
47	Naples	Campania	Italy	40.8517745999999988	14.2681244000000333
48	Rome	Lazio	Italy	41.9027834999999911	12.4963655000000244
49	Rabat	Rabat-Sale-Zemmour-Zaer	Morocco	33.9715903999999966	-6.84981289999996079
50	Riyadh	Riyadh Province	Saudi Arabia	24.7135517	46.6752956999999924
51	Singapore	\N	Singapore	1.3553793999999999	103.867744399999992
52	Manila	Metro Manila	Philippines	14.5995124000000001	120.984219499999995
53	Moscow	Moscow	Russia	55.755825999999999	37.6173000000000002
54	Beijing	Beijing	China	39.9042109999999965	116.407394999999951
55	Kyoto	Kyoto Prefecture	Japan	35.0116362999999922	135.768029399999932
56	Sydney	New South Wales	Australia	-33.8688197000000031	151.209295500000053
57	Auckland	Auckland	New Zealand	-36.8484596999999994	174.763331500000049
58	Mumbai	Maharashtra	India	19.0759836999999983	72.8776559000000361
59	Goa	Himachal Pradesh	India	30.7688315999999986	77.656296999999995
60	Pune	Maharashtra	India	18.520430300000001	73.8567436999999245
61	Hyderabad	Telangana	India	17.3850440000000006	78.4866710000000012
62	Colombo	Western Province	Sri Lanka	6.92707860000000242	79.8612430000000586
63	Ahmedabad	Gujarat	India	23.0225049999999989	72.5713620999999875
64	New Delhi	Delhi	India	28.6139390999999996	77.209021200000052
65	Kolkata	West Bengal	India	22.5726459999999989	88.3638949999999568
66	Dehradun	Uttarakhand	India	30.316494500000001	78.0321917999999641
67	Jakarta	Special Capital Region of Jakarta	Indonesia	-6.2087633999999996	106.845598999999993
68	London	England	United Kingdom	51.5073508999999987	-0.127758299999982228
69	Edinburgh	Scotland	United Kingdom	55.9532519999999991	-3.18826699999999619
70	Dublin	County Dublin	Ireland	53.3498052999999999	-6.26030969999999343
71	Ljubljana	Ljubljana	Slovenia	46.0569465000000022	14.5057514999999739
72	Mandalay	Mandalay Region	Myanmar (Burma)	21.9588281999999992	96.0891031999999541
73	Cape Town	Western Cape	South Africa	-33.9248685000000023	18.4240552999999636
74	Luanda	Luanda Province	Angola	-8.83998759999999884	13.2894367999999758
75	Antananarivo	Antananarivo Province	Madagascar	-18.8791902	47.5079054999999926
76	Cairo	Cairo Governorate	Egypt	30.0444196000000012	31.2357116000000588
77	Tehran	Tehran Province	Iran	35.6891974999999988	51.3889735999999857
78	Kathmandu	Central Development Region	Nepal	27.7172452999999983	85.3239604999999983
79	Huaihua	Hunan	China	27.5695170000000012	110.001923000000033
80	Saint Petersburg	Saint Petersburg	Russia	59.9342802000000034	30.3350986000000375
81	Dubai	Dubai	United Arab Emirates	25.2048492999999993	55.2707828000000063
82	Buenos Aires	Autonomous City of Buenos Aires	Argentina	-34.603684400000013	-58.381559100000004
83	Havana	Havana	Cuba	23.1135924999999993	-82.3665955999999824
84	El cascajo	Islas Galápagos	Ecuador	-0.66543870000000005	-90.2737422999999808
85	Waimea	Hawaii	United States	20.0230555999999993	-155.671666700000003
86	Anchorage	Alaska	United States	61.2180555999999996	-149.900277800000026
87	Reykjavík	Capital Region	Iceland	64.1265205999999921	-21.8174392999999327
88	Kuala Lumpur	Federal Territory of Kuala Lumpur	Malaysia	3.13900300000000021	101.686854999999923
89	Ho Chi Minh City	Ho Chi Minh	Vietnam	10.8230988999999997	106.629663800000003
90	Bangkok	\N	Thailand	13.7563309	100.501765100000057
91	Chennai	Tamil Nadu	India	13.0826802000000004	80.270718400000078
92	Bengaluru	Karnataka	India	12.9715986999999995	77.5945626999999831
93	Udaipur	Rajasthan	India	24.585445	73.7124790000000303
94	Agra	Uttar Pradesh	India	27.1766700999999991	78.0080745000000206
95	Jaipur	Rajasthan	India	26.9124336	75.7872709000000668
96	Jerusalem	Jerusalem District	Israel	31.7683190000000018	35.2137099999999919
97	Tunis	Tunis	Tunisia	36.806494800000003	10.1815315999999711
98	Córdoba	Andalusia	Spain	37.888175099999998	-4.77938349999999446
99	Salamanca	Castile and León	Spain	40.970103899999998	-5.66353970000000118
100	Paris	Île-de-France	France	48.8566140000000075	2.35222190000001774
101	Bordeaux	Aquitaine-Limousin-Poitou-Charentes	France	44.8377890000000008	-0.579179999999951178
102	Milan	Lombardy	Italy	45.4654219000000026	9.18592430000001059
103	Zürich	Zurich	Switzerland	47.3768865999999989	8.54169400000000678
104	Berlin	Berlin	Germany	52.5200065999999879	13.4049539999999752
105	Brussels	Brussels	Belgium	50.8503395999999981	4.35171030000003611
106	Prague	Prague	Czech Republic	50.0755381000000028	14.4378004999999803
107	Vienna	Vienna	Austria	48.2081743000000031	16.3738189000000602
108	Budapest	Budapest	Hungary	47.4979119999999995	19.0402349999999387
109	Frankfurt	Hesse	Germany	50.1109220999999891	8.68212670000002618
110	Sarajevo	Federation of Bosnia and Herzegovina	Bosnia and Herzegovina	43.8562585999999968	18.413076300000057
111	Athens	Attica	Greece	37.9838096000000007	23.7275388000000476
112	Stockholm	Stockholm County	Sweden	59.3293234999999868	18.0685808000000634
113	Helsinki	Uusimaa	Finland	60.1698556999999923	24.9383789999999408
114	Venice	Veneto	Italy	45.4408474000000027	12.3155150999999705
115	Kaunas	Kaunas County	Lithuania	54.8985206999999988	23.9035965000000488
116	Snoqualmie	Washington	United States	47.5287131999999986	-121.825390599999992
\.


--
-- Name: locations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('locations_id_seq', 116, true);


--
-- Data for Name: pin_types; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY pin_types (id, description) FROM stdin;
1	Wish List
2	Going back!
3	Never going back.
\.


--
-- Name: pin_types_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('pin_types_id_seq', 1, false);


--
-- Data for Name: pins; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY pins (id, user_id, pin_type_id, location_id) FROM stdin;
1	1	1	1
2	1	1	2
4	2	2	4
5	2	2	5
6	2	2	6
7	2	2	7
8	2	1	8
9	2	1	9
10	2	1	10
11	2	1	11
12	2	1	12
13	2	1	13
14	2	1	14
15	2	3	15
16	2	3	16
17	2	2	17
18	2	2	18
19	2	2	19
20	2	2	20
21	2	1	21
22	2	1	22
23	2	1	23
25	2	1	25
26	2	2	26
27	2	3	27
28	2	2	28
29	2	2	29
30	2	1	30
31	2	1	31
32	2	1	32
33	2	1	33
34	2	1	34
35	2	1	35
36	2	2	36
37	2	2	37
38	2	2	38
39	2	2	39
40	2	2	40
41	2	2	41
42	2	2	42
43	2	2	43
44	2	2	44
45	2	1	45
46	2	1	46
47	2	1	47
48	2	1	48
49	2	1	49
50	2	3	50
51	2	2	51
52	2	3	52
53	2	1	53
54	2	1	54
55	2	1	55
56	2	1	56
57	2	1	57
58	2	2	58
59	2	1	59
60	2	3	60
61	2	2	61
62	2	2	62
63	2	2	63
64	2	2	64
65	2	2	65
66	2	3	66
67	2	2	67
68	2	2	68
69	2	1	69
70	2	1	70
71	2	1	71
72	2	1	72
73	2	1	73
74	2	1	74
75	2	1	75
76	2	1	76
77	2	1	77
78	2	2	78
79	2	1	79
80	2	1	80
81	2	2	81
82	2	1	82
83	2	1	83
84	2	1	84
85	2	1	85
86	2	1	86
87	2	1	87
88	2	3	88
89	2	1	89
90	2	1	90
91	2	2	91
92	2	2	92
93	2	1	93
94	2	2	94
95	2	1	95
96	2	1	96
97	2	1	97
98	2	1	98
99	2	1	99
100	2	2	100
101	2	1	101
102	2	1	102
103	2	2	103
104	2	1	104
105	2	1	105
106	2	1	106
107	2	1	107
108	2	1	108
109	2	3	109
110	2	1	110
111	2	1	111
112	2	1	112
113	2	1	113
115	2	1	114
24	2	1	24
116	2	1	115
117	4	2	116
\.


--
-- Name: pins_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('pins_id_seq', 117, true);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY users (id, fname, lname, email, password) FROM stdin;
1	Ann	Fortner	aceyfor@gmail.com	$2b$12$yMeCAc1QuYroFBsaB7a/6unkTA369KJRkAUN7rl5UrPJtM/yZ3op2
2	Guest	Guest	guest@guest.com	$2b$12$SnASuhzGqKi82q3YGlezfeSoNENZiahay8sUG9ZRpSqt1tf2P/yG2
4	Dale	Cooper	dalecooper@fbi.com	$2b$12$0QYiQF19m4UamoGcYsWfmO87JbNOV6DsNyOQZLN1Nlk9TRZlN4FT.
\.


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('users_id_seq', 4, true);


--
-- Name: locations_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY locations
    ADD CONSTRAINT locations_pkey PRIMARY KEY (id);


--
-- Name: pin_types_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY pin_types
    ADD CONSTRAINT pin_types_pkey PRIMARY KEY (id);


--
-- Name: pins_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY pins
    ADD CONSTRAINT pins_pkey PRIMARY KEY (id);


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: pins_location_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY pins
    ADD CONSTRAINT pins_location_id_fkey FOREIGN KEY (location_id) REFERENCES locations(id);


--
-- Name: pins_pin_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY pins
    ADD CONSTRAINT pins_pin_type_id_fkey FOREIGN KEY (pin_type_id) REFERENCES pin_types(id);


--
-- Name: pins_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY pins
    ADD CONSTRAINT pins_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

