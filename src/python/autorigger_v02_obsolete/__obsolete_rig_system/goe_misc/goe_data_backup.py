'''
Created on Oct 22, 2014

@author: Emre
'''
"""
def save_objects(rigData):
    sd = ShapesIO()
 
    #--- save objects
    filepath = os.path.join(sd.asset_misc_path, 'puppet_objects.pickle')
    with open(filepath, 'w') as json_file:
        pickle.dump(rigData, json_file, pickle.HIGHEST_PROTOCOL)
#END save_objects()
 
def load_objects():
    sd = ShapesIO()
 
    #--- load objects
    filepath = os.path.join(sd.asset_misc_path, 'puppet_objects.pickle')
    objpath = os.path.join(sd.asset_data_path, 'obj.py')
    if os.path.exists(filepath):
        with open(filepath) as pickle_data:
            pickle_data = pickle.load(pickle_data)
            generator.obj_builder(objpath, pickle_data)
#END load_objects()
"""