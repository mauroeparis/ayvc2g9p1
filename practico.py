# %%
import matplotlib.pyplot as plt
import numpy
import pandas
import seaborn

import io
import requests


# %%
url = 'https://object.cato.org/sites/cato.org/files/human-freedom-index-files/human-freedom-index-2019.csv'
req_content = requests.get(url).content
dataset = pandas.read_csv(
    io.StringIO(req_content.decode('utf-8'))
)

# %%
score_cols = [col for col in dataset.columns if 'pf_identity' in col] + [
    'pf_score', # Personal Freedom (score)
    'pf_rank', # Personal Freedom (rank)
    'ef_score', # Economic Freedom (score)
    'ef_rank', # Economic Freedom (rank)
    'hf_score', # Human Freedom (score)
    'hf_rank', # Human Freedom (rank)
]

important_cols = ['year', 'ISO_code', 'countries', 'region'] + score_cols

# %%
dataset = dataset[important_cols].replace('-', numpy.nan)
for score_col in score_cols:
    dataset[score_col] = pandas.to_numeric(dataset[score_col])

# %%
"""
Parte 1
=======

Luego de las clases del primer fin de semana, ya tenemos las herramientas
para responder las siguientes preguntas:
"""
# %%
"""
1. Estadísticos descriptivos
----------------------------

1. Para comenzar con un pantallazo de los datos, calcular el rango de las
   variables.
"""

# %% 1. calcular el rango de las variables.
max_series = dataset[important_cols].max(numeric_only=True)
min_series = dataset[important_cols].min(numeric_only=True)

min_max_df = pandas.concat(
    [max_series, min_series],
    axis=1,
    names=['max', 'min']
)

min_max_df.columns = ['max', 'min']
min_max_df

# %%
"""
2. Para cada país, tenemos varias realizaciones para cada variable
   `pf_identity` y `hf_score`. Si queremos comparar un país con otro, ¿cuál es
   la manera adecuada de hacerlo? Por ejemplo, ¿nos quedamos con un único
   valor? ¿o comparamos todos los valores? ¿usamos el promedio? ¿usamos la
   mediana?
"""

# %%
"""
Existen muchas cosas que debemos tener en cuenta al momento de comparar dos
paises entre sí. No podemos quedarnos solamente con un único valor.

Para hacer una comparación podriamos ver la mediana y el promedio para tener
un primer acercamiento. Sin embargo, es importante observar la evolucion año a
año de cada país. Esto puede ser complicado según los datos con los que
dispongamos dado a que el dataset no tiene los valores de todos lo años para
todos los paises.
"""

# %%
"""
3. Obtener media, mediana y desviación estándar de las variables `pf_identity`
   y `hf_score` en el mundo y compararla con la de Latinoamérica y el caribe.
   Usar la respuesta del punto anterior para justificar si la comparación es
   válida o no.
"""
# %%
world = dataset
latam = dataset['Latin America & the Caribbean' == dataset['region']]

data = [
    [world['pf_identity'].mean(), latam['pf_identity'].mean()],
    [world['pf_identity'].median(), latam['pf_identity'].median()],
    [world['pf_identity'].std(), latam['pf_identity'].std()]
]
pandas.DataFrame(
    data,
    columns=['world', 'latam'],
    index=['mean', 'median', 'standart deviation']
)

# %%
data = [
    [world['hf_score'].mean(), latam['hf_score'].mean()],
    [world['hf_score'].median(), latam['hf_score'].median()],
    [world['hf_score'].std(), latam['hf_score'].std()]
]
pandas.DataFrame(
    data,
    columns=['world', 'latam'],
    index=['mean', 'median', 'standart deviation']
)


# %%
"""
La comparación no es válida porque no tiene en cuenta la evolución año a año,
pone a todos los paises (o a una region grande de ellos) en la misma bolsa,
no contempla la diferencia en cantidad de datos.
"""

# %%
"""
4. ¿Tiene sentido calcular la moda?
"""
# %%
"""
No, dado a que son valores continuos y no discretos. Quizás pasar los datos
a enteros y calcular la moda sobre eso podria brindarnos un panorama sobre los
valores más usuales.
"""

# %%
# TODO:
"""
5. ¿Cómo pueden sanearse los valores faltantes?
"""

# %%
"""
6. ¿Encuentra outliers en estas dos variables? ¿Qué método utiliza para
   detectarlos? Los outliers, ¿son globales o por grupo? ¿Los eliminaría del
   conjunto de datos?
"""

# %%
"""
Existen outliners en la variable `hf_score` como podemos ver en este boxplot.
Los outliners no son globales y la mayoría se encuentra en Lationamerica.
"""
# %%
ax = seaborn.boxplot(x='region', y='hf_score', data=dataset)

ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
plt.tight_layout()
plt.show()

# %%
"""
Debería ser muy cuidadoso al eliminar outliners dado a que pueden contener
información importante. Por ejemplo, en Latinoamérica todos los valores de
Venezuela pueden ser considerados outliners.
"""
# %%
ax = seaborn.boxplot(x='countries', y='hf_score', data=latam)

ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
plt.tight_layout()
plt.show()
# %%
"""
Pienso que para eliminar los outliners primero se debe estudiar qué los
ocasiona y el impácto que puede tener quitarlos al hacer analisis sobre el
dataset.
"""

# %%
"""
2. Agregación de datos
----------------------
"""
# %%
"""
1. Grafiquen la media de la variable `pf_identity` y `hf_score` a través
   de los años.
"""
# %%
# Defino un a funcion para solo tener que pasar el dataset de la region
def plt_median(dt, region):
    pf_identity_graph = seaborn.lineplot(
        y='pf_identity', x='year',
        data=dt,
        estimator=numpy.median,
        label='pf_identity'
    )
    hf_score_graph = seaborn.lineplot(
        y='hf_score', x='year',
        data=dt,
        estimator=numpy.median,
        label='hf_score'
    )
    hf_score_graph.set(ylabel='', xlabel='Year')
    hf_score_graph.set_title(region)
    plt.show()

# %%
plt_median(world, 'Global')


# %%
"""
2. Realicen los mismos gráficos, pero separando por regiones (Cada variable
   en un gráfico distinto, sino no se ve nada). ¿La tendencia observada, es
   la misma que si no dividimos por regiones?
"""

# %%
plt_median(latam, 'Latin America & the Caribbean')

# %%
east_eu = dataset['Eastern Europe' == dataset['region']]

plt_median(east_eu, 'Eastern Europe')

# %%
middle_east_north_af = dataset[
    'Middle East & North Africa' == dataset['region']
]

plt_median(middle_east_north_af, 'Middle East & North Africa')

# %%
sub_sahara_af = dataset['Sub-Saharan Africa' == dataset['region']]

plt_median(middle_east_north_af, 'Sub-Saharan Africa')

# %%
cau_central_as = dataset['Caucasus & Central Asia' == dataset['region']]

plt_median(cau_central_as, 'Caucasus & Central Asia')

# %%
oceania = dataset['Oceania' == dataset['region']]

plt_median(oceania, 'Oceania')

# %%
wes_eu = dataset['Western Europe' == dataset['region']]

plt_median(wes_eu, 'Western Europe')

# %%
south_as = dataset['South Asia' == dataset['region']]

plt_median(south_as, 'South Asia')

# %%
north_am = dataset['North America' == dataset['region']]

plt_median(north_am, 'North America')

# %%
east_as = dataset['East Asia' == dataset['region']]

plt_median(east_as, 'East Asia')

# %%
"""
Como podemos ver la libertad de identidad personal (`pf_identity`) sufre un
declive en el año 2014 globalmente a mayor o menor escala.

Por otra parte `hf_score`, a pesar de no tener saltos abruptos en ninguna
región no tiene una tendencia mundial.
"""


# %%
"""
3. Si lo consideran necesario, grafiquen algunos países de Latinoamerica para
   tratar de explicar la tendencia de la variable `pf_identity` en la región.
   ¿Cómo seleccionarion los países relevantes a esa tendencia?

> **Pista:** hay gráficos de seaborn que permiten generar visualizaciones para
> cada valor de una variable categórica, en este caso, las distintas regiones.
"""


"""
Sólo por curiosidad, graficar la tendencia de `hf_score` y `ef_score` a
través de los años. ¿Tienen alguna hipótesis para este comportamiento?
"""
