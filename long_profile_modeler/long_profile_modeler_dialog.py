# -*- coding: utf-8 -*-
"""
/***************************************************************************
 LongProfileModelerDialog
                                 A QGIS plugin
 Creates Long Profiles from lsdtt-network-tool outputs
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2022-08-24
        git sha              : $Format:%H$
        copyright            : (C) 2022 by Josie Welsh
        email                : welsh162@umn.edu
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os
import webbrowser
from .tool_generate_selected_channel_file import GenerateSelectedChannelFile
from .tool_drainage_area_slope import DrainageAreaSlope, LoadSelectedFile
from .tool_generate_long_profiles import GenerateLongProfiles

import pandas as pd
import geopandas as gpd
import numpy as np
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets
from qgis.gui import QgsFileWidget
from qgis.core import QgsVectorLayer, QgsProject

#for the figures!
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'long_profile_modeler_dialog_base.ui'))


class LongProfileModelerDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(LongProfileModelerDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.pbExit.clicked.connect(self.onpbExitclicked)

        #Page 1
        self.pbGenerateSelectedChannelFile.clicked.connect(self.onpbGenerateSelectedChannelFileclicked)
        self.fwSelectedChannelFileOutput.setStorageMode(QgsFileWidget.SaveFile)

        #Page 2
        self.pbLoadSelectedChannel.clicked.connect(self.onpbLoadSelectedChannelclicked)
        self.pbCalculateFit.clicked.connect(self.onpbCalculateFitclicked)
        self.fwSelectedChannelInput.filePath()

        #Page 3
        self.pbGenerateLongProfiles.clicked.connect(self.onpbGenerateLongProfilesclicked)


    def onpbGenerateSelectedChannelFileclicked(self):
        #setup input values to pass to the generate_selected_channel_file tool
        nodes_layer = self.mlcbNodes.currentLayer()
        segments_layer = self.mlcbSegments.currentLayer()
        input_segment_id = int(self.qleInputSegmentID.text())
        output_file_path = self.fwSelectedChannelFileOutput.filePath()

        print("Segments:", segments_layer)
        print("Nodes:", nodes_layer)
        print("Input Segment:", input_segment_id)
        print("Output File Path:", output_file_path)

        #instantiate and run tool
        tool = GenerateSelectedChannelFile(nodes_layer, segments_layer, input_segment_id, output_file_path)
        output = tool.generate_selected_channel_file()
               

    def onpbExitclicked(self):
        print("Plugin Closed")
        self.close()


    def onpbLoadSelectedChannelclicked(self):
        #selected_channel_layer = self.mlcbSelectedChannelInput.currentLayer()
        selected_channel_file = self.fwSelectedChannelInput.filePath()

        #instantiate and run tool
        tool = LoadSelectedFile(selected_channel_file)
        output = tool.load_selected_channel()

        
    def onpbCalculateFitclicked(self):
        selected_channel_file = self.fwSelectedChannelInput.filePath()
        sbMinValue = self.sbMinValue.value()
        sbMaxValue = self.sbMaxValue.value()
        sbMinExponent = self.sbMinExponent.value()
        sbMaxExponent = self.sbMaxExponent.value()
        qleKsValue = self.qleKsValue
        qleThetaValue = self.qleThetaValue
        cbShowFit = self.cbShowFit

        #instantiate and run tool
        tool = DrainageAreaSlope(selected_channel_file, sbMinValue, sbMaxValue, sbMinExponent, sbMaxExponent, qleKsValue, qleThetaValue, cbShowFit)
        output = tool.calculate_fit()


    def onpbGenerateLongProfilesclicked(self):
        selected_channel_file = self.fwSelectedChannelInput.filePath()
        cbIncludeSelectedChannelData = self.cbIncludeSelectedChannelData
        cbIncludeModeledData = self.cbIncludeModeledData
        qleLongProfileFigureTitle = self.qleLongProfileFigureTitle
        qleKsValue = self.qleKsValue
        qleThetaValue = self.qleThetaValue

        #instantiate and run tool
        tool = GenerateLongProfiles(selected_channel_file, cbIncludeSelectedChannelData, cbIncludeModeledData, qleLongProfileFigureTitle, qleKsValue, qleThetaValue)
        output = tool.generate_long_profiles()