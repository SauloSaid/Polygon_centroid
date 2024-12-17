import geopandas as gpd
import pandas as pd

# Caminhos relativos para os arquivos
data_path = "data/"
output_path = "output/"

# Carregar o shapefile
gdf = gpd.read_file(f"{data_path}rj_setores_censitarios.shp")

# Certifique-se de que a geometria ativa está definida
if gdf.geometry.name != "geometry":
    gdf = gdf.set_geometry("geometry")

# Verifica e define o CRS, se necessário
if gdf.crs is None:
    gdf = gdf.set_crs(epsg=4326)  # WGS 84 (substitua se necessário)

# Reprojetar para um CRS projetado (necessário para cálculos corretos de centroides)
gdf = gdf.to_crs(epsg=3857)  # CRS projetado (Web Mercator como exemplo)

# Calcular centroides
gdf['centroid'] = gdf.geometry.centroid

# Definir a nova coluna 'centroid' como geometria ativa, se desejado
gdf = gdf.set_geometry("centroid")

# Opcional: Remover a coluna 'geometry' original
gdf = gdf.drop(columns=["geometry"])

# Salvar o GeoDataFrame em um novo shapefile
gdf.to_file(f"{output_path}censo_2010_setores_centroid.shp")

# Carregar a base de dados adicional
basico1 = pd.read_csv(
    f"{data_path}Basico_RJ.csv", 
    sep=";", 
    encoding="latin1", 
    decimal=','
)

# Exibir colunas do DataFrame
print(basico1.columns)

# Converter o código do setor para string
basico1['Cod_setor'] = basico1['Cod_setor'].astype(str)

# Mesclar com o GeoDataFrame
gdf = gdf.merge(basico1, left_on="CD_GEOCODI", right_on="Cod_setor", how='left')

# Exibir cabeçalho do GeoDataFrame
print(gdf.head())

# Salvar o GeoDataFrame atualizado em um novo shapefile
gdf.to_file(f"{output_path}censo_2010_setores_centroid.shp")

# Preencher NaN com 0 e converter colunas desejadas para inteiro
columns_convert = ['V001', 'V002', 'V003', 'V004', 'V005', 'V006', 'V007', 'V008', 'V009',
                   'V010', 'V011', 'V012']

basico1[columns_convert] = basico1[columns_convert].fillna(0).astype(int)

# Exibir o DataFrame atualizado
print(basico1)
