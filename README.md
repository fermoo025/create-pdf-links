The project is complete.
This project uses GAS and Python and has many settings.
1. GAS must be deployed.
In the GAS editing window, click Deploy/Manage Deployments and deploy as a Web App. You must set the execution permission to Any to connect from Python.
Copy the Deployment ID in the last window. Use this as the App ID.
3. Install Python and install the relevant modules.
4. Run form.py.

The execution requirements are as follows.
Enter App ID, Folder ID, Sub Folders (separated by commas), Sheet ID, and Sheet Tab Name.
Folder ID is the ID of the 2025 holder.
The reason for specifying Sub Folders is that if there are many partial registrations in the 2025 holder, it will take a long time to convert the entire thing. Enter the partial holders separated by commas.
I think you can figure out the Sheet ID and Sheet Tab Name.

When you press Submit at the end, it sends a command to the GAS project specified in the App ID to start the conversion. GAS searches for partial holders and converts all PDFs to TXT and saves them. 
At about 8 per minute, it will take about 40 minutes for 300. When finished, the results are saved in the Sheet.
