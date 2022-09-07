# QGIS-LongProfileModel-Plugin
Code for a QGIS plugin that takes lsdtopotools-network-tool outputs and creates long profile and modeled long profiles.

## How to Use the Tool
### Download the Plugin
1. Download the plugin from this github repository. Once it has downloaded exctract the zip file and copy the folder labeled **long_profile_modeler**. We will be pasting this folder in a specific location in step 4. 

2. Open a QGIS window

3. In the **Menu Toolbar**, click on **Settings**. Within the **Settings** menu, hover over user profiles to expand the options, then select **Open Active Profile Folder**. This pulls up the location where QGIS looks for information.

4. Within the file explorer window that was opened in the previous step and open the **python** folder and within the python folder open the **plugins** folder. This folder contains all of your downloaded QGIS plugins, so this is where we would like to add our plugin folder. Paste the **long_profile_modeler** file that was copied in step 1 here.

5. Restart QGIS. Now that we have added our folder to the plugins folder, we need to restart QGIS in order for it to recognize the changes we have made. 

6. Now that QGIS has been restarted, we can finalize the installation of the plugin. In the **Menu Toolbar**, click on **Plugins**, then click on **Manage and Install Plugins...** from the sub-menu.
7. Search for **Long Profile Modeler** in the **All** tab and the plugin should show up. Click on the plugin in the list, then click **Install Plugin** to install it. Before closing the window, make sure that on the list of plugins, the checkbox next to the desired plugin it is checked. 

Now the plugin is installed and ready to be used!

### Preliminary Steps
1. Create a dataset for a single basin using LSDTopoTools. For detailed instructions on this step, see here.

2. Use the LSDTT Network Tool to create the preliminary datasets needed to run the long profile model plugin. FOr detailed instructions on this step, see here.

Once these steps are complete, you can start using the Long Profile Modeler. 

### Using the Tool
1. Open a QGIS window (if one is not yet open) and start a new project.

2. Load the layers created by the network tool into your project. This should include both a segments layer and a nodes layer. 

3. Navigate to the **Plugins** menu and select **Long Progile Modeler** within the sub-menu. This will open a new window for the user interface of the the Long Profile Modeler. The plugin is divided into 3 tabs, **Create Single Flowpath**, **Drainage Area - Slope**, and **Modeled Long Profile**. You will want to work through these tabs in the above order, as entered/calculated information from earlier tabs is used on later tabs. 

Starting with the **Create Single Flowpath** tab. What we will do on this tab is combine information from both of the layers from the lsdtt-network-tool and create a dataset of points that represent one flowpath.

4. From the drop down menus select the layers you loaded into QGIS. Ensure that the layers are under the correct label. Nodes layers will likely have  **_nodes** at the end of the file name. 

5. Enter the **Input Segment ID** for the flowpath that you are interested in looking at. How do I know what **Input Segment ID** is associated with my flowpath of interest? Generally speaking, when we are looking at river long profiles, we are interested in an entire flowpath, from the channel head to the mouth of the river. Without going into the nitty-gritty details, this plugin creates a flowpath by starting from a given point and working downstream until it finds the end of the network. So, whichever starting point you pick will be the furthest upstream point found for your flowpath. Because of this, we generally want to choose a channel head as our input node. Once you have identified a channel head or starting segment of interest, return to the main QGIS window. select the **Identify Features** button on the **Attributes Toolbar** at the top of the window. This will pull up a new panel called **Identify Results**. Make sure that the **segments** layer is selected in the layers list, then click on the segment of interest. Once a segment is selected, it will be highlighted in red and values will fill the **Identify Results** panel. The value labeled **id** is the number you should use for **Input Segment ID**.

6. The final step on this tab is to select a file name and location for the flowpath dataset that will be generated. Generally, keeping this data in the same place as the data from the lsdtt-network-tool is the simplest way to keep things organized.

7. Click the **Generate Selected File** button to create the new dataset. Once it has finished running, the new dataset will be loaded as a layer in the project. 

8. Proceed to the **Drainage Area - Slope** tab.

In the **Drainage Area - Slope** tab, we will be looking at the dataset generated in the previous step in slope vs. drainage area space. In this space we can fit a power law function to a portion of the data, allowing us to  generate models of historic long-profiles in following steps. 

9. The file generated in the previous step should have autopopulated the **Selected Channel File** box, but if not or if you already have a flowpath dataset ready, then you can use the **...** button to select a file.

10. Click **Load** to display the data in log(slope) vs. log(drainage area) space. This visualization can be used to identify which portion of data you would like to use for the fit. No figures are saved automatically, but all figures can be saved from the figure window by clicking the save button. 

11. Once you have chosen a portion of data, identify the minimum and maximum drainage area values, then enter them for the **minimum fit value** and **maximum fit value**, respectively.
     - For each value (min and max) there are two numbers that must be entered, a value and an exponent. 

12. Click the **Calculate Fit** value to generate a fit of that portion of data. This will generate ks and theta values, which will be used to generate a paleo- long profile in future steps. Checking the **Show Fit** box allows you to see the fit to the data so that you can make adjustments accordingly. Again, no figures are saved automatically, but all figures can be saved from the figure window by clicking the save button. 

13. Once you are satisfied with the fit, proceed to the **Modeled Long Profile** tab. 

The **Modeled Long Profile** tab serves two functions. The first is to generate a figure of the long profile of the flowpath/selected channel data created in the **Create Single Flowpath** tab. If this is the desired output, then the **Drainage Area - Slope** tab and steps 9 - 13 can be skipped. The second function is to generate and visualize a modeled long profile. This fuinction requires all steps to be followed. 

14. Check the box/boxes that you wish to include in your figure. These boxes are independent of one another, thus any combination of checked and unchecked boxes can work. If you just want a figure of the selected channel/flowpath as it is in the original data, then only check the **Selected Channel Long Profile** box. Add a figure title in the **Figure Title** text box if you would like. If this box is left blank, then the figure title will be left blank. 

15. Click the **Generate Long Profiles** button to view your figures! No figures are saved automatically, but all figures can be saved from the figure window by clicking the save button. 
