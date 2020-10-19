from usgs import api


def submit_where_query():

    # USGS uses numerical codes to identify queryable fields
    # To see which fields are queryable for a specific dataset,
    # send off a request to dataset-fields

    fields = api.dataset_fields('LANDSAT_8', 'EE', api_key="RLvkdNZCbaPBqGykxdrqJPgHHMjdBkDx")

    for field in fields:
        print(field)

    # WRS Path happens to have the field id 10036
    where = {
        10036: '043'
    }
    scenes = api.search('LANDSAT_8', 'EE', where=where, start_date='2015-04-01', end_date='2015-05-01', max_results=10, extended=True)

    print(scenes)

    for scene in scenes:
        print(scene)

submit_where_query()

# from usgs import api

# # Set the EarthExplorer catalog
# node = 'EE'# this indicates earth explorer website

# # Set the Hyperion and Landsat 8 dataset
# hyperion_dataset = 'EO1_HYP_PUB'
# landsat8_dataset = 'LANDSAT_8'

# # Set the scene ids
# hyperion_scene_id = 'EO1H1820422014302110K2_SG1_01'
# landsat8_scene_id = 'LC80290462015135LGN00'

# # Submit requests to USGS servers
# api.metadata(hyperion_dataset, node, [hyperion_scene_id])
# api.metadata(landsat8_dataset, node, [landsat8_scene_id])