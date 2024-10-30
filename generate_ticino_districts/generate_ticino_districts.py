import geopandas as gpd
import pandas as pd
import os

print('Reading in geojson file')

# Read the shapefile
gdf = gpd.read_file("data/swissboundaries3d_2024-01_2056_5728_as_WSG84.json")

#information taken from Ticino Municipalities excel (data folder)
region_districts = {
 'Bellinzona e Alto Ticino' : {
    'Leventia_Turismo' : ["Airolo","Bedretto","Bodio","Dalpe","Faido","Giornico","Personico","Pollegio","Prato (Leventina)","Quinto"],
    'Bellinzona_Turismo' : ["Arbedo-Castione","Bellinzona","Cadenazzo" ,"Lumino" ,"Sant'Antonino"],
    'Blenio_Turismo' : ["Acquarossa", "Blenio" ,"Serravalle" ],
    'Biasca_e_Riviera_Turismo': [ "Biasca", "Riviera"]
},

'Lago Maggiore e Valli' : {
    'Ente_Turistico_Tenero_e_Valle_Verzasca' : [ "Cugnasco-Gerra","Gordola","Lavertezzo","Mergoscia","Tenero-Contra","Verzasca"],
    'Gambarogno_Turismo': ["Gambarogno"],
    'Lago_Maggiore_Turismo': ["Ascona","Brione sopra Minusio","Brissago","Centovalli","Locarno","Losone","Minusio","Muralto","Onsernone","Orselina", "Ronco sopra Ascona","Terre di Pedemonte"],
    'Vallemaggia_Turismo': [ "Avegno Gordevio", "Bosco/Gurin", "Campo (Vallemaggia)","Cerentino","Cevio","Lavizzara","Linescio","Maggia" ]

},

'Lago di Lugano': {
    'Lugano_Turismo': [ "Bedano", "Cadempino","Canobbio","Capriasca","Collina d'Oro","Comano","Cureglia","Grancia","Gravesano","Isone","Lamone","Lugano","Manno","Massagno","Melide","Mezzovico-Vira",
                       "Monteceneri","Morcote","Muzzano","Origlio","Paradiso","Ponte Capriasca","Porza","Savosa","Sorengo","Torricella-Taverne","Vezia","Vico Morcote"],
    'Malcantone_Turismo': [ "Agno","Alto Malcantone","Aranno","Astano","Bedigliora","Bioggio","Cademario","Caslano","Curio","Magliaso","Miglieglia","Neggio","Novaggio","Tresa","Pura","Vernate"]
},

"Mendrisiotto" : {
    "Ente_Turistico_del_Mendrisiotto_e_Basso_Malcantone" : [ "Arogno", "Balerna", "Bissone","Breggia", "Brusino Arsizio", "Castel San Pietro", "Chiasso","Coldrerio","Mendrisio","Morbio Inferiore","Novazzano","Riva San Vitale","Stabio","Vacallo","Val Mara"]
}

}

# colors used to help with visualations (style property convention - works in some places)
district_color = {

    'Leventia_Turismo' : "#edb879",
    'Bellinzona_Turismo' : "#1979a9",
    'Blenio_Turismo' : "#e07b39",
    'Biasca_e_Riviera_Turismo': "#69bdd2",
    'Ente_Turistico_Tenero_e_Valle_Verzasca' : "#80391e",
    'Gambarogno_Turismo': "#cce7e8",
    'Lago_Maggiore_Turismo': "#042f66",
    'Vallemaggia_Turismo': "#b97455",
    'Lugano_Turismo': "#44bcd8",
    'Malcantone_Turismo': "#84aebe",
    "Ente_Turistico_del_Mendrisiotto_e_Basso_Malcantone" :"#f06f47",
}

list_of_districts=[]

#iterate through the regions
for region_name in region_districts:

    output_folder_name=f"output/{region_name}"
    if not os.path.exists(output_folder_name):
        os.makedirs(output_folder_name)
    district_municipalites = region_districts[region_name]


    #within each region iterate through the districts
    for district_name in district_municipalites:
        municip_list = district_municipalites[district_name]
        municip_gdf = gdf[ gdf ["NAME"].isin(municip_list)]
        print(f"For district {district_name} there are {len(municip_list)} municipalities listed: {municip_gdf.shape} municipalities found in geojson file")
        
        # check if all municipalities are detected in the Map
        if len(municip_list) != municip_gdf.shape[0]:
            municip_gdf_list = municip_gdf["NAME"].tolist()
            print(f"municipalities list: {municip_list}")
            print(f"municipalities found in geojson file : { municip_gdf_list }")
            
        # disolve the municipalities together to use the other border for the district border
        district_poly = municip_gdf.dissolve().explode(index_parts=True)
        
        #print(district_poly.info())

        #add some meta data to the dataframe
        district_poly = district_poly[["geometry"]].copy()
        district_poly['tourism_district'] = district_name
        district_poly['region'] = region_name
        district_poly['canton'] = 'Ticino'

        district_poly['title'] = f" {district_name} / {region_name} " 
        district_poly['fill'] = district_color[district_name] 
        district_poly['fill-opacity'] = 0.5

        #write each district polygon to its own file
        district_poly.to_file(f"{output_folder_name}/{district_name}.json", driver="GeoJSON")
    
        #keep track of the district polygons
        list_of_districts.append(district_poly)

# write all the district polygons to one file.
district_list_df = pd.concat(list_of_districts)
print(f"Shape of district list df {district_list_df.shape}")
district_list_df.to_file("output/Ticino_Tourism_districts.json", driver="GeoJSON")
        



