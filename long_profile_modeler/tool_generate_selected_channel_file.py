import pandas as pd
import geopandas as gpd
import numpy as np
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt
from qgis.core import QgsVectorLayer, QgsProject

class GenerateSelectedChannelFile:
    def __init__(self, nodes_layer, segments_layer, input_segment_id, output_file_path) -> None:
        self._nodes_layer = nodes_layer
        self._segments_layer = segments_layer
        self._input_segment_id = input_segment_id
        self._output_file_path = output_file_path


    def generate_selected_channel_file(self):

        #Creating a df with important attributes from segments
        #First some lists of data that is important
        id = []
        slope = []
        toseg = []

        #Now lets fill these lists
        for segment in self._segments_layer.getFeatures():
            #print("Node ID:", segment.id())
            attrs = segment.attributes()
            #print(attrs)
            id.append(attrs[1])
            slope.append(attrs[5])
            toseg.append(attrs[2])

        #put the lists into a dictionary and then into a dataframe    
        data_from_segs = {'segment_id': id, 'slope': slope, 'toseg': toseg}

        dfsegs = pd.DataFrame(data_from_segs)
        #print(dfsegs)

        #Creating a df with important attributes from nodes
        lat = []
        long = []
        elevation_m = []
        flow_distance_m = []
        drainage_area_m2 = []
        segment_id = []

        for node in self._nodes_layer.getFeatures():
            attrs = node.attributes()
            lat.append(attrs[4])
            long.append(attrs[5])
            elevation_m.append(attrs[7])
            flow_distance_m.append(attrs[8])
            drainage_area_m2.append(attrs[9])
            segment_id.append(attrs[18])

        #put the lists into a dictionary and then into a dataframe    
        data_from_nodes = {'lat': lat, 'long': long, 'elevation_m': elevation_m, 'flow_distance_m': flow_distance_m,
                                     'drainage_area_m2': drainage_area_m2, 'segment_id': segment_id}

        dfnodes = gpd.GeoDataFrame(data_from_nodes, geometry = gpd.points_from_xy(data_from_nodes['long'], data_from_nodes['lat']))
        #print(dfnodes['geometry'])

        ########################
        # Start Using The Data #
        ########################
        
        #Find out if the input segment is in the segments dataframe.
        input_segment_id_found = False
        for seg_id in dfsegs['segment_id']:
            if seg_id == self._input_segment_id:
                input_segment_id_found = True
                print("Segment ID found.")

            if not input_segment_id_found:
                print("Error: No segment with the given ID")

        ###############
        #GENERATE PATH#
        ###############

        #Begin to generate path.

        #Look up user input seg id, create column is_input w/true and false
        dfsegs['is_input'] = np.where(dfsegs['segment_id']== self._input_segment_id, True, False)

        #Create new df called dfpath that is populated by all the true values.
        dfpath = dfsegs[dfsegs['is_input'] == True]

        #Create the path
        #Set input_toseg to the self._input_segment_id
        #Does this generate a duplicate of the first segment?
        input_toseg = self._input_segment_id
        while input_toseg != -1:
            #find relevant toseg
            input_toseg=dfpath.loc[dfpath['segment_id']== self._input_segment_id, 'toseg']
            #convert to int
            input_toseg=int(input_toseg)
            #query dfsegs to find the segment with the same id as toseg
            dfsegs['is_input'] = np.where(dfsegs['segment_id']== input_toseg, True, False)
            #take this line and append it to dfpath
            dfpath = dfpath.append(dfsegs[dfsegs['is_input'] == True])
            self._input_segment_id = input_toseg
            #print(dfpath)
            
        #Begin pulling required nodes from segments
        #Create list of relevant segments
        queried_segments = []
        queried_segments_idx = []
        for seg_id in dfpath['segment_id']:
            queried_segments.append(seg_id)
            queried_segments_idx.append(dfsegs.index[dfsegs['segment_id'] == seg_id][0])

        # Approach with nodes already printed
        path_nodes=[]
        for _id in queried_segments:
            path_nodes.append(dfnodes[dfnodes['segment_id'] == _id] )

        #Create a df with relevant nodes in path
        dfpath_nodes = pd.concat(path_nodes, ignore_index=True)
        #print(dfpath_nodes)

        #Add the slopes from the segments to the path_nodes in a new gpd df called merged
        merged = dfpath_nodes.merge(dfpath, on='segment_id', how='left')

        #Test print
        #print("Path Nodes:", merged)

        #print to gpkg
        merged.to_file(self._output_file_path, layer='selected_channel', driver='GPKG', overwrite = 'YES')

        vlayer = QgsVectorLayer(self._output_file_path, "Selected Channel", "ogr")
        QgsProject.instance().addMapLayer(vlayer)

        print('Done!')