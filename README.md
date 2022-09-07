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

4. Starting with the **Create Single Flowpath** tab. What we will do on this tab is combine information from both of the layers from the lsdtt-network-tool and create a dataset of points that represent one flowpath.
