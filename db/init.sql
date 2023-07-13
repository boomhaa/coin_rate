use database postgres
CREATE TABLE courses(
id INT NOT NULL PRIMARY KEY,
coin_name character varying(16) NOT NULL,
price numeric NOT NULL,
updated_at timestamp NOT NULL
);