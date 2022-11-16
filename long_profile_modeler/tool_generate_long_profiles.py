import pandas as pd
import geopandas as gpd
import numpy as np
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt
from qgis.core import QgsVectorLayer, QgsProject

class GenerateLongProfiles:
    def __init__(self, selected_channel_file, cbIncludeSelectedChannelData, cbIncludeModeledData, qleLongProfileFigureTitle, qleKsValue, qleThetaValue) -> None:
        self._selected_channel_file = selected_channel_file
        self._cbIncludeSelectedChannelData = cbIncludeSelectedChannelData
        self._cbIncludeModeledData = cbIncludeModeledData
        self._qleLongProfileFigureTitle = qleLongProfileFigureTitle
        self._qleKsValue = qleKsValue
        self._qleThetaValue = qleThetaValue

    def generate_long_profiles(self):
            
        dfpath_nodes = gpd.read_file(self._selected_channel_file)
        #print (dfpath_nodes)

        def power_law(drainage_area, ks, theta):
            slope = ks*(drainage_area**(-theta))
            return slope

        #create a list of drainage areas for modeling purposes
        drainage_area = []
        for i in range(len(dfpath_nodes)):
            da = float(dfpath_nodes['drainage_area_m2'][i])
            drainage_area.append(da)

        #model slopes 
        ks = float(self._qleKsValue.text())
        theta = float(self._qleThetaValue.text())

        slope_model = []
        for i in range(len(dfpath_nodes)):
            sm = power_law(drainage_area[i], ks, theta)
            slope_model.append(sm)

        #Use modeled slopes to model elevation at each point
        #use the function y = mx + b to calculate the elevation using slope, distance and initial point.

        #find initial elevation:
        initial_elevation = dfpath_nodes['elevation_m'][0]

        #create a list of distances between each point
        distance = []
        for i in range(len(dfpath_nodes)):
            if i + 1 == len(dfpath_nodes):
                print('Done finding distances between nodes')
            else:
                di = dfpath_nodes['flow_distance_m'][i] - dfpath_nodes['flow_distance_m'][i+1]
                distance.append(di)

        #create a list of elevation changes for each point
        elevation_change = []
        for i in range(len(distance)):
            ec = distance[i] * slope_model[i]
            elevation_change.append(ec)

        #model elevation at each point
        elevation = []
        for i in range(len(elevation_change)):
            if i == 0:
                el = initial_elevation
            else:
                el = elevation[i-1] - elevation_change[i]
            
            elevation.append(el)
        elevation.append(el)

        
        #Now for the plotting
        fig, ax = plt.subplots()
        ax.set_xlabel("Distance Upstream (km)")
        ax.set_ylabel("Elevation Above Mouth (m)")
        ax.legend()
        ax.set_title(self._qleLongProfileFigureTitle.text())

        if self._cbIncludeSelectedChannelData.isChecked():
            plt.scatter(dfpath_nodes['flow_distance_m']/1000, dfpath_nodes['elevation_m'], label = 'Selected Channel Long Profile')
        
        if self._cbIncludeModeledData.isChecked():
            plt.scatter(dfpath_nodes["flow_distance_m"]/1000, elevation, label = 'Modeled Long Profile Pre-Disturbance')

        fig.show()