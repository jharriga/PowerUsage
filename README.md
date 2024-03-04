# PowerUsage
Collection of scripts for monitoring system power usage <br>
Comments in Python code include USAGE details <br>
*_STDOUT.txt files show sample console output <br>

## POWER SCRIPTS (require Redfish IPaddr and login credentials)
rfChassis.py - probes Redfish URI /redfish/v1/Chassis for PowerConsumedWatts property<br>
> - rfChassis_STDOUT.txt - sample console output<br>

PRO3Xmultiple.py - probes Redfish URI /redfish/v1/PowerEquipment for per Outlet Wattage used<br>
> - PRO3Xdicts_json.txt - additional documentation on dictonary structures<br>
> - PRO3Xmultiple_OUTFILE.json - sample JSON output file<br>

universal_resources.py - function definitions required by PRO3Xmultiple.py<br>
<br>
Ansible/ - folder with playbook and supporting scripts.<br>
> - Coordinates Power Script and Workload processes<br> 
