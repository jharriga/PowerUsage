#!/usr/bin/python3
"""
rfNEWchassis.py
  Gathers the specified power metrics using HP's ilo REST library
  https://github.com/HewlettPackard/python-ilorest-library
  Based on 'examples/Redfish/get_powermetrics_average.py'

NOTE: there is namespace collision with the 'redfish' library
      remove prior to using with: '$ pip uninstall redfish'

PRE-REQ: $ pip3 install python-ilorest-library
         Successfully installed python-ilorest-library-4.6.0.0
         $ python --version       <-- python3

USAGE:   $ <file>.py 10.16.28.89 ADMIN ADMIN
       Required arguments: ipaddr, account, passwd
       Optional arguments: -st <sleepSec> 
OUTPUT:
    Read CFG file: rf_properties.cfg
    Searching for these Properties:
     ['AverageConsumedWatts', 'IntervalInMin', 'MaxConsumedWatts', 
      'MinConsumedWatts', 'PowerCapacityWatts', 'PowerOutputWatts', 'BOGUS']
    Chassis Power Data:
        AverageConsumedWatts 192
        IntervalInMin 0
        MaxConsumedWatts 192
        MinConsumedWatts 192
        PowerCapacityWatts 2000 2000
        PowerOutputWatts 88 80
    Properties skipped or not found = ['BOGUS']
"""

import sys
import os
import json
import argparse
import time            # used by def timing_generator
import inspect         # used by 'inspect.currentframe().f_code.co_name'
import statistics      # used to produce Summary
# Using python-ilorest-library (see PRE-REQs)
from redfish import RedfishClient
from redfish.rest.v1 import ServerDownOrUnreachableError

#
# BEGIN FUNCTIONS
def timing_decorator(func):
    # Any time you wrap function with this decorator, it will print
    # the name of the function and runtime duration / time.
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        original_return_val = func(*args, **kwargs)
        end = time.perf_counter()
        # Limiting to three significant digits
        print("time elapsed in ", func.__name__, ": ",
              "{0:.3g}".format(end - start), sep='')
        return original_return_val

    return wrapper

@timing_decorator
def get_chassisPower(_redfishobj, _property_list, _chassis_power_uri):

##    not_found = []              # return list of missing properties

    # /redfish/v1/Chassis/
    if _chassis_power_uri is None:
        # First call - do work to acquire URI (re-used on subsequent calls)
        chassis_members_uri = getMember_uri(_redfishobj, 'Chassis')
        chassis_members_response = _redfishobj.get(chassis_members_uri)
    # Typically returns '/redfish/v1/Chassis/Power/Self'
        chassis_power_uri = chassis_members_response.obj['Power']['@odata.id']
    else:
        # Re-use the URI passed to function
        chassis_power_uri = _chassis_power_uri

    if chassis_power_uri:
        # Returns a nested dict representing the parsed JSON
        chassis_power_data = _redfishobj.get(chassis_power_uri).dict
        print("Chassis Power Data:") 
#        print("DEBUG", chassis_power_uri)                          # DEBUG
#        print("DEBUG", json.dumps(chassis_power_data, indent = 4)) # DEBUG 
        # Iterate and search for keys within the resulting dict
##        for this_property in _property_list:
        # Returns a list of values which match 'this_property'
        this_property = "PowerConsumedWatts"
        values_list = list(findkeys(chassis_power_data, this_property))
        # only print if values were found
        if len(values_list) >= 1:
            print("\t", this_property, *values_list)
        else:
            print("\t not found:", this_property, *values_list)
##            not_found.append(this_property) 

##    return [not_found, chassis_power_uri]
    value = values_list[0]
    return [value, chassis_power_uri]

def findkeys(node, kv):
    # traverse 'dict' (node) searching for key-value (kv)
    # returns list of matching key values
    if isinstance(node, list):
        for i in node:
            for x in findkeys(i, kv):
               yield x
    elif isinstance(node, dict):
        if kv in node:
            yield node[kv]
        for j in node.values():
            for x in findkeys(j, kv):
                yield x

@timing_decorator
def get_DateTime(_redfishobj, _managers_uri):
    # Read timestamp from Redfish server
    # /redfish/v1/Managers/
    if _managers_uri is None:
        # First call - do work to acquire URI (re-used on subsequent calls)
        managers_uri = getMember_uri(_redfishobj, 'Managers')
    else:
        # Re-use the URI passed to function
        managers_uri = _managers_uri 

    if managers_uri:
        managers_data = _redfishobj.get(managers_uri).dict
#       print("DEBUG: ", json.dumps(managers_data, indent = 4))    # DEBUG

    # The current date and time (with UTC offset) that the Manager uses
    timestamp_list = list(findkeys(managers_data, 'DateTime'))

    return [timestamp_list, managers_uri]

# No need to time this - doesn't access Redfish Server
def getRoot_uri(R_obj, R_type):
    # Return URI for Redfish root object 'R_type': Chassis, Manager, ...
    R_uri = R_obj.root.obj[R_type]['@odata.id']

    return(R_uri)

# No need to time this - doesn't access Redfish Server
def getObject_uri(this_obj, this_type):
    # Return URI for Redfish object
    this_uri = this_obj[this_type]['@odata.id']

    return(this_uri)

@timing_decorator
def getMember_uri(M_obj, M_type):
    # Return URI for Redfish MEMBER object 'M_type'
    M_uri = M_obj.root.obj[M_type]['@odata.id']
    M_response = M_obj.get(M_uri)
    M_members_uri = next(iter(M_response.obj['Members']))['@odata.id']

    return(M_members_uri)

#
# END FUNCTIONS

if __name__ == "__main__":
    # Parse required ARGS: ipaddr, account, passwd
    parser = argparse.ArgumentParser()
    parser.add_argument('ipaddr', action='store',
                    type=str, help='REDFISH IP address (https)')
    parser.add_argument('account', action='store',
                    type=str, help='REDFISH login acct')
    parser.add_argument('passwd', action='store', 
                    type=str, help='REDFISH password')
    # Add optional arguments: -ns <numSamples> -st <sleepTime>
    #
    args = parser.parse_args()
    ipaddr = args.ipaddr
    account = args.account
    passwd = args.passwd

    # DEBUG: hardcode these for now
    num_samples = 3          # total number of samples to log
    sleep_time = 5           # delay between Redfish samples (in seconds)
    # DEBUG
    print(f"CMDLINE args: {ipaddr} {num_samples} {sleep_time}")

    # init empty lists
    property_list = []   
    telemInfo_list = []  
    dateTime_list = []     
    chassisPower_list = []           # returned from get_chassisPower
    missingProps_list = [] 
    configFile = 'rf_properties.cfg'    # text file w/properties to log
    readings_list = []            # wattage readings
    ptimes_list = []              # probe timing results
    total_rt = 0                  # Total runtime (in sec)

    # Read proprty_list Properties (pwr consumption) from CFG file
    if os.path.isfile(configFile):
        with open(configFile) as cfgfile:
            for line in cfgfile:
                line = line.strip()           # remove newline
                property_list.append(line)    # add to property_list
        cfgfile.close()
        print(f"\nRead CFG file: {configFile}")
        print(f"Searching for these Properties:\n {property_list}") 
    else:
        print(f"\nERROR unable to open file: {configFile} EXITING\n")
        sys.exit(1)

    try:
        # Create a Redfish client object
        REDFISHOBJ = RedfishClient(base_url = ipaddr,
                                   username = account, 
                                   password = passwd)
        # Login with the Redfish client
        REDFISHOBJ.login()
    except ServerDownOrUnreachableError as excp:
        sys.stderr.write("ERROR: Redfish server not reachable.\n")
        sys.exit()

    ##################################
    # Record and Print Redfish Metrics
    # Print opening message
    print("Hit Control-C <SIGINT> to end\n")
    cntr = 1
    # Continue monitoring until Interrupted
    begin_ts = time.perf_counter()

    try:
        while True:
            # First call. Need to probe Redfish for the URI.
            if cntr == 1:
                dt_uri = None
                cp_uri = None
            else:
                dt_uri = dateTime_list[1]             # re-use next call
                cp_uri = chassisPower_list[1]         # re-use next call

            print(f"\nSample #{cntr}")
            # WARNING this slow - remove
            # Report on Redfish Timestamp / DateTime value
            dateTime_list = get_DateTime(REDFISHOBJ, dt_uri)
            if len(dateTime_list[0]) >= 1:
                print("DateTime", *dateTime_list[0])
            else:
                print("DateTime not found") 

            # Record probe time for this Sample
            begin_mark = time.perf_counter()
            chassisPower_list = get_chassisPower(REDFISHOBJ,
                                                 property_list, cp_uri)
            end_mark = time.perf_counter()
            probe_rt = round((end_mark - begin_mark), 3)

            # Append to Summary stats for this Sample
            readings_list.append(float(chassisPower_list[0]))
            ptimes_list.append(float(probe_rt))

            missingProps_list = chassisPower_list[0]
## DEBUG Start
##            if len(missingProps_list) >= 1:
##                print(f"Properties skipped or not found = {missingProps_list}\n")
##            else:
##                print("All Properties found\n")
## DEBUG End

            time.sleep(sleep_time)               # delay the loop
            cntr = cntr + 1                      # incr counter

    except KeyboardInterrupt:
        print('Interrupted!')

    # DONE - cleanup and print SUMMARY w/AVGs
    final_ts = time.perf_counter()
    REDFISHOBJ.logout()

    # Calculate the Averages and report Summary
    avg_ptime = round(statistics.mean(ptimes_list), 2)
    min_reading = round(min(readings_list), 2)
    max_reading = round(max(readings_list), 2)
    avg_reading = round(statistics.mean(readings_list), 2)
    total_rt = round((final_ts - begin_ts), 1)
    print(f"Run Summary: ")
    print(f"> Total Samples: {cntr}")
    print(f"> MIN Reading: {min_reading}")
    print(f"> MAX Reading: {max_reading}")
    print(f"> AVG Reading: {avg_reading}")
    print(f"> AVG Probe Time: {avg_ptime}")
    print(f"> Total Runtime: {total_rt}")

    print("DONE")

# END __main__

