# Files and scripts useful for Perf Co-Pilot and power usage metrics  
# OpenMetrics/  
 
**Openmetrics PMDA Files**
> These files extend the openmetrics PMDA to access the Redfish power usage
> metrics, from Chassis and Smart PDUs
> 
> The values in **'RFvars.cfg'** must be set for your environment:
> 1) Redfish device IP addresses
> 2) Redfish server User account name and password
> 3) Redfish URLs for both Chassis Power and Smart PDU readings 

After editing the 'RFvars.cfg' file with your local Redfish server info, the  
files should be copied to the '/var/lib/pcp/pmdas/openmetrics/config.d'  
directory and the '.sh' files should be made executable  
>    
**The Metrics can be verified and the Readings viewed**  
> $ pminfo openmetrics | grep watts  
> openmetrics.RFpdu2.watts  
> openmetrics.RFchassis.watts  
> openmetrics.RFpdu1.watts  
>
> $ pmrep openmetrics.RFchassis openmetrics.RFpdu1 openmetrics.RFpdu2  
>   o.R.watts  o.R.watts  o.R.watts  
>  
>    352.000    185.000    179.000  
>    352.000    186.000    182.000  
>    352.000    185.000    181.000  

For more info on PMDA-OPENMETRICS see the man page

**test.sh is a utility that continously echoes Redfish Chassis & PDU power readings to screen, without requiring use of Perf CoPilot** 
> Requires vars in 'RFvars.cfg' to be configured for URLs and Credentials  
> By default the repeat loop delay is 5 seconds  

# DeviceTesting/  


