import pandas as pd
import pyodbc
import sqlalchemy
import os

# Ruta actual
current_directory = os.path.dirname(__file__)

def crearRuta(nombreArchivo):
    return os.path.join(current_directory, 'data', nombreArchivo)

df = pd.read_csv('netflix_titles.csv')

# Eliminar registros con valores nulos
df = df.dropna()

# Convertir la columna 'date_added' a tipo datetime
df['date_added'] = pd.to_datetime(df['date_added'], format="mixed")

# Creamos backup
netflix_titles = df

# Separar los datos de la columna 'cast' para tener un actor por fila
actors_df = df['cast'].str.split(',', expand=True).apply(lambda x: x.str.strip()).stack().reset_index(level=0).rename(columns={0: 'actor_name'}).rename_axis('show_id')
# Quitar actores duplicados y añadir índice
unique_actors = actors_df['actor_name'].drop_duplicates().reset_index(drop=True).reset_index()
# Renombrar columna index a actor_id
unique_actors = unique_actors.rename(columns={'index': 'actor_id'})

# Separar los datos de la columna 'listed_in' para tener una categoría por fila
category_df = df['listed_in'].str.split(',', expand=True).apply(lambda x: x.str.strip()).stack().reset_index(level=0).rename(columns={0: 'category_name'}).rename_axis('show_id')
# Quitar categorías duplicadas y añadir índice
unique_categories = category_df['category_name'].drop_duplicates().reset_index(drop=True).reset_index()
# Renombrar columna index a category_id
unique_categories = unique_categories.rename(columns={'index': 'category_id'})

# Separar los datos de la columna 'director' para tener un director por fila
director_df = df['director'].str.split(',', expand=True).apply(lambda x: x.str.strip()).stack().reset_index(level=0).rename(columns={0: 'director_name'}).rename_axis('show_id')
# Quitar directores duplicados y añadir índice
unique_directors = director_df['director_name'].drop_duplicates().reset_index(drop=True).reset_index()
# Renombrar columna index a director_id
unique_directors = unique_directors.rename(columns={'index': 'director_id'})

# Separar los datos de la columna 'country' para tener un país por fila
country_df = df['country'].str.split(',', expand=True).apply(lambda x: x.str.strip()).stack().reset_index(level=0).rename(columns={0: 'country_name'}).rename_axis('show_id')
# Quitar columnas vacías
country_df = country_df.dropna(subset=['country_name'])
# Quitar países duplicadas y añadir índice
unique_countries = country_df['country_name'].drop_duplicates().reset_index(drop=True).reset_index()
# Renombrar columna index a country_id
unique_countries = unique_countries.rename(columns={'index': 'country_id'})

# Obtener la columna rating del df y renombrarla
rating_df = df['rating'].rename('rating_name').reset_index()
# Quitar los valores nulos
rating_df = rating_df.dropna(subset=['rating_name'])
# Quitar duplicados y añadir índice
unique_ratings = rating_df['rating_name'].drop_duplicates().reset_index(drop=True).reset_index()
# Renombrar columna index a tipo_id
unique_ratings = unique_ratings.rename(columns={'index': 'rating_id'})

# Obtener la columna type del df y renombrarla
tipo_df = df['type'].rename('tipo_name').reset_index()
# Quitar los valores nulos
tipo_df = tipo_df.dropna(subset=['tipo_name'])
# Quitar duplicados y añadir índice
unique_tipos = tipo_df['tipo_name'].drop_duplicates().reset_index(drop=True).reset_index()
# Renombrar columna index a tipo_id
unique_tipos = unique_tipos.rename(columns={'index': 'tipo_id'})

# Dividir la columna 'duration' en dos columnas separadas
df[['duration', 'duration_unit']] = df['duration'].str.split(' ', expand=True)
df = df.drop(columns=['duration_unit'])
df['duration'] = df['duration']

# Unimos con la tabla recién creada de Tipo
df = df.merge(unique_tipos, left_on='type', right_on='tipo_name')
# Quitamos las columnas que ya no sirven
df = df.drop(columns=['type', 'tipo_name'])

# Hacemos lo mismo con Rating, unimos con la tabla recién creada de Rating
df= df.merge(unique_ratings, left_on='rating', right_on='rating_name')
# Quitamos las columnas que ya no sirven
df = df.drop(columns=['rating', 'rating_name'])

# Ahora obtenemos los datos para la tabla Show_Actor
show_actor = df[['show_id', 'cast']]
# Separamos a los actores y los mostramos en forma vertical
show_actor = show_actor.assign(cast=show_actor['cast'].str.split(', ')).explode('cast').reset_index(drop=True)
# Cambiamos el nombre a la columna
show_actor = show_actor.rename(columns={'cast': 'actor_name'})
# Hacemos un merge con la tabla de actores únicos para obtener el id del actor
show_actor = show_actor.merge(unique_actors, left_on='actor_name', right_on='actor_name')
# Quitamos la columna de nombre
show_actor = show_actor.drop(columns=['actor_name'])

# Ahora obtenemos los datos para la tabla Show_Category
show_category = df[['show_id', 'listed_in']]
# Separamos a las categorías y los mostramos en forma vertical
show_category = show_category.assign(listed_in=show_category['listed_in'].str.split(', ')).explode('listed_in').reset_index(drop=True)
# Cambiamos el nombre a la columna
show_category = show_category.rename(columns={'listed_in': 'category_name'})
# Hacemos un merge con la tabla de categorías únicas para obtener el id de la categoría
show_category = show_category.merge(unique_categories, left_on='category_name', right_on='category_name')
# Quitamos la columna de nombre
show_category = show_category.drop(columns=['category_name'])

# Ahora obtenemos los datos para la tabla Show_Director
show_director = df[['show_id', 'director']]
# Separamos a los directores y los mostramos en forma vertical
show_director = show_director.assign(director=show_director['director'].str.split(', ')).explode('director').reset_index(drop=True)
# Cambiamos el nombre a la columna
show_director = show_director.rename(columns={'director': 'director_name'})
# Hacemos un merge con la tabla de directores únicos para obtener el id del director
show_director = show_director.merge(unique_directors, left_on='director_name', right_on='director_name')
# Quitamos la columna de nombre
show_director = show_director.drop(columns=['director_name'])

# Ahora obtenemos los datos para la tabla Show_Country
show_country = df[['show_id', 'country']]
# Separamos a los países y los mostramos en forma vertical
show_country = show_country.assign(country=show_country['country'].str.split(', ')).explode('country').reset_index(drop=True)
# Cambiamos el nombre a la columna
show_country = show_country.rename(columns={'country': 'country_name'})
# Hacemos un merge con la tabla de países únicos para obtener el id del país
show_country = show_country.merge(unique_countries, left_on='country_name', right_on='country_name')
# Quitamos la columna de nombre
show_country = show_country.drop(columns=['country_name'])

# Quitamos columnas del dataframe principal que no nos sirven
df = df.drop(columns=['director','cast','country', 'listed_in'])

# Guardar los datos limpios y transformados en nuevos archivo CSV
df.to_csv(crearRuta('cleaned_netflix_titles.csv'), index=False)
unique_actors.to_csv(crearRuta('actors.csv'), index=False)
unique_categories.to_csv(crearRuta('categories.csv'), index=False)
unique_directors.to_csv(crearRuta('directors.csv'), index=False)
unique_countries.to_csv(crearRuta('countries.csv'), index=False)
unique_ratings.to_csv(crearRuta('ratings.csv'), index=False)
unique_tipos.to_csv(crearRuta('types.csv'), index=False)
show_actor.to_csv(crearRuta('show_actor.csv'), index=False)
show_category.to_csv(crearRuta('show_category.csv'), index=False)
show_director.to_csv(crearRuta('show_director.csv'), index=False)
show_country.to_csv(crearRuta('show_country.csv'), index=False)

# Guardamos cada dataframe en una hoja en un excel
with pd.ExcelWriter(crearRuta('data.xlsx'), engine='xlsxwriter') as writer:
    netflix_titles.to_excel(writer, sheet_name='original', index=False)
    df.to_excel(writer, sheet_name='show', index=False)
    unique_actors.to_excel(writer, sheet_name='actor', index=False)
    unique_categories.to_excel(writer, sheet_name='category', index=False)
    unique_directors.to_excel(writer, sheet_name='director', index=False)
    unique_countries.to_excel(writer, sheet_name='country', index=False)
    unique_ratings.to_excel(writer, sheet_name='rating', index=False)
    unique_tipos.to_excel(writer, sheet_name='tipo', index=False)
    show_actor.to_excel(writer, sheet_name='show_actor', index=False)
    show_category.to_excel(writer, sheet_name='show_category', index=False)
    show_director.to_excel(writer, sheet_name='show_director', index=False)
    show_country.to_excel(writer, sheet_name='show_country', index=False)
    

# Cadena de conexión a la base de datos
engine = sqlalchemy.create_engine('mssql+pyodbc://VLIK/test?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server')

# Insertamos en la base de datos
df.to_sql(name='Show', con=engine, if_exists='replace', index=False)
unique_actors.to_sql(name='Actor', con=engine, if_exists='replace', index=False)
unique_categories.to_sql(name='Category', con=engine, if_exists='replace', index=False)
unique_directors.to_sql(name='Director', con=engine, if_exists='replace', index=False)
unique_countries.to_sql(name='Country', con=engine, if_exists='replace', index=False)
unique_ratings.to_sql(name='Rating', con=engine, if_exists='replace', index=False)
unique_tipos.to_sql(name='Tipo', con=engine, if_exists='replace', index=False)
show_actor.to_sql(name='Show_Actor', con=engine, if_exists='replace', index=False)
show_category.to_sql(name='Show_Category', con=engine, if_exists='replace', index=False)
show_director.to_sql(name='Show_Director', con=engine, if_exists='replace', index=False)
show_country.to_sql(name='Show_Country', con=engine, if_exists='replace', index=False)

# Cerramos la conexión
engine.dispose()
