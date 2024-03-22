USE test;
GO

CREATE TABLE dbo.Show (
    show_id varchar(max) NULL,
	title varchar(max) NULL,
	date_added datetime NULL,
	release_year bigint NULL,
	duration varchar(max) NULL,
	description varchar(max) NULL,
	tipo_id bigint NULL,
	rating_id bigint NULL
)
GO

CREATE TABLE dbo.Actor (
    actor_id int NULL,
    actor_name varchar(max) NULL
)
GO

CREATE TABLE dbo.Category (
    category_id int NULL,
    category_name varchar(max) NULL
)
GO

CREATE TABLE dbo.Country (
    country_id int NULL,
    country_name varchar(max) NULL
)
GO

CREATE TABLE dbo.Director (
    director_id int NULL,
    director_name varchar(max) NULL
)
GO

CREATE TABLE dbo.Rating (
    rating_id int NULL,
    rating_name varchar(max) NULL
)
GO

CREATE TABLE dbo.Tipo (
    tipo_id int NULL,
    tipo_name varchar(max) NULL
)
GO

CREATE TABLE dbo.Show_Actor (
    show_id varchar(max) NULL,
    actor_id varchar(max) NULL
)
GO

CREATE TABLE dbo.Show_Category (
    show_id varchar(max) NULL,
    category_id varchar(max) NULL
)
GO

CREATE TABLE dbo.Show_Director (
    show_id varchar(max) NULL,
    director_id varchar(max) NULL
)
GO

CREATE TABLE dbo.Show_Country (
    show_id varchar(max) NULL,
    country_id varchar(max) NULL
)
GO
