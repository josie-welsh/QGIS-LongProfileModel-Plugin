import pandas as pd
import geopandas as gpd
import numpy as np
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt
from qgis.core import QgsVectorLayer, QgsProject

class LoadSelectedFile:
    def __init__(self,selected_channel_file):
        self._selected_channel_file = selected_channel_file

    def load_selected_channel(self):          
        dfpath_nodes = gpd.read_file(self._selected_channel_file)
        print (dfpath_nodes)

        #create a list of drainage areas for slope-area analysis
        drainage_area_as = []
        for i in range(len(dfpath_nodes)):
            da = float(dfpath_nodes['drainage_area_m2'][i])
            drainage_area_as.append(da)

        #create a list of slopes
        slope = []
        for i in range(len(dfpath_nodes)):
            sl = float(dfpath_nodes['slope'][i])
            slope.append(sl)

        #Plot in log-log space using matplotlib
        fig, ax = plt.subplots()
        plt.xscale("log")
        plt.yscale("log")
        plt.scatter(drainage_area_as, slope, label = 'Selected Channel')
        ax.set_xlabel("Drainage Area (m2)")
        ax.set_ylabel("Slope")
        leg = ax.legend()
        fig.show()

class DrainageAreaSlope:
    def __init__(self, selected_channel_file, sbMinValue, sbMaxValue, sbMinExponent, sbMaxExponent, qleKsValue, qleThetaValue, cbShowFit) -> None:

        self._selected_channel_file = selected_channel_file
        self._sbMinValue = sbMinValue
        self._sbMaxValue = sbMaxValue
        self._sbMinExponent = sbMinExponent
        self._sbMaxExponent = sbMaxExponent
        self._qleKsValue = qleKsValue
        self._qleThetaValue = qleThetaValue
        self._cbShowFit = cbShowFit

    def calculate_fit(self):
        
        #import the chosen drainage path from the file
        dfpath_nodes = gpd.read_file(self._selected_channel_file)
        #print (dfpath_nodes)

        #create fit range values from user inputs
        min = self._sbMinValue * (10**self._sbMinExponent)
        max = self._sbMaxValue * (10**self._sbMaxExponent)
        print('Min:', min)
        print('Max:', max)

        #create lists for all points for drainage area and slope
        drainage_area = []
        for i in range(len(dfpath_nodes)):
            da = float(dfpath_nodes['drainage_area_m2'][i])
            drainage_area.append(da)

        #create a list of slopes
        slope = []
        for i in range(len(dfpath_nodes)):
            sl = float(dfpath_nodes['slope'][i])
            slope.append(sl)

        #create a list of drainage areas for slope-area analysis
        drainage_area_as = []
        for i in range(len(dfpath_nodes)):
            if dfpath_nodes['drainage_area_m2'][i] <= max and dfpath_nodes['drainage_area_m2'][i] >= min:
                da = float(dfpath_nodes['drainage_area_m2'][i])
                drainage_area_as.append(da)

        #create a list of slopes
        slope_as = []
        for i in range(len(dfpath_nodes)):
            if dfpath_nodes['drainage_area_m2'][i] <= max and dfpath_nodes['drainage_area_m2'][i] >= min:
                sl = float(dfpath_nodes['slope'][i])
                slope_as.append(sl)

        ##############################
        #Find values for ks and theta#
        ##############################
        #power law:
        def power_law(drainage_area, ks, theta):
            slope = ks*(drainage_area**(-theta))
            return slope

        #find trendline in log-log space
        # Fit the dummy power-law data
        pars, cov = curve_fit(f=power_law, xdata=drainage_area_as, ydata=slope_as, p0=[0, 0], bounds=(-np.inf, np.inf))

        ks = pars[0]
        theta = pars[1]

        

        self._qleKsValue.setText(str(ks))
        self._qleThetaValue.setText(str(theta))

        #Plot both the raw data and the fit in log-log space using matplotlib
        if self._cbShowFit.isChecked():
            fig, ax = plt.subplots()
            plt.xscale("log")
            plt.yscale("log")
            plt.scatter(drainage_area, slope, label = 'Selected Channel')
            ax.plot(drainage_area_as, power_law(drainage_area_as, *pars), linestyle='--', linewidth=2, color='black')
            ax.set_xlabel("Drainage Area (m2)")
            ax.set_ylabel("Slope")
            leg = ax.legend()
            fig.show()
