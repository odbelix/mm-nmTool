#!/usr/bin/env python
########################################################################
# <mnTool, Get information from Switches for network tracking irregularity
# activities and othe kind of information>
# Copyright (C) 2015  Manuel Moscoso Dominguez manuel.moscoso.d@gmail.com
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA
########################################################################
# Manuel Moscoso Dominguez <manuel.moscoso.d@gmail.com>
########################################################################
import commands
import sys
import snmputils.parser as parser
import snmputils.identifiers as ids
import snmputils.collector as collector
import snmputils.export as export
import snmputils.defaulttext as dtext
import snmputils.validation as validation

import argparse

	

##REMOVE
import time
import textwrap

list_oid_interfaces = {'localInterface':'iso.3.6.1.2.1.2.2.1.2' , 'idInterface' : 'iso.3.6.1.2.1.17.1.4.1.2', 'statusInterfaces':'iso.3.6.1.2.1.2.2.1.8' }
list_oid_mactraffic = {'idInterface':'iso.3.6.1.2.1.17.4.3.1.2'}
		
    #for oid in ids.neighbour:
        #command = "snmpwalk -v 1 -c public %s %s" % (ip,ids.neighbour[oid])
        #output = commands.getstatusoutput(command)
        #outputlist = output[1].split("\n")
        #for line in outputlist:
            #if any(patter in line for patter in ids.patterkeys):
                #oidData = line.split(" ")[0].replace(ids.neighbour[oid],"")
                #if oidData not in listOidData:
                    #listOidData.append(oidData)
                    #dictOidData[oidData] = {}
                #if oid == "address":
                    #dictOidData[oidData][oid] =parser.HextoStringIp(line)
                #else:
                    #dictOidData[oidData][oid] =parser.OutputToString(line)
    #result = {'list':listOidData,'dict':dictOidData}
    #return result


# if len(sys.argv) is not 2:
#     sys.exit("Proble with parameter")
#
# ip_device = sys.argv[1]

#detectedDeviceWithIrregularActivity
WarningDevices = ['192.168.13.4','192.168.13.11','192.168.13.12','192.168.13.13'
,'192.168.13.19','192.168.13.35','192.168.13.52','192.168.13.72','192.168.13.80'
,'192.168.13.87','192.168.13.110','192.168.13.111','192.168.13.159',
'192.168.13.167','192.168.13.169','192.168.13.170','192.168.13.193',
'192.168.13.227','192.168.13.230','192.168.13.233']

notValidIp = ['192.168.13.171','172.17.1.26','172.17.1.27','172.17.1.250',
'172.18.1.250','172.19.1.1','10.3.1.1','10.1.1.3']

OutNetwork13 = ['192.168.30.100','192.168.15.200','192.168.30.150',
'192.168.60.239','192.168.20.173','192.168.17.213','192.168.17.212',
'192.168.17.211','192.168.80.241','192.168.15.200','192.168.20.251',
'192.168.20.249','192.168.1.241','192.168.1.242','192.168.1.243',
'192.168.90.199','192.168.1.244','192.168.1.240']

############ X,X,GW-Sede-Curico,VG-Sede-Curico
problems = ['192.168.13.31','192.168.13.170','172.17.1.26','172.17.1.27']


##### INFORMATION ABOUT HOST
#listPublicHosts = collector.getListOfPublicIpHost('190.110.100.0',24)
#listPublicHosts2 = collector.getListOfPublicIpHost('190.110.101.0',24)
#ListHost = dict(listPublicHosts.items() + listPublicHosts2.items())
#dictHosts = collector.getHostActivityFromDevice('192.168.30.100',ListHost)
#result = export.hostToCSV(dictHosts)
#print result


########################################################################

parser = argparse.ArgumentParser(
formatter_class=argparse.RawDescriptionHelpFormatter,
description="mm-nmTool - Options",
epilog=".....................\n.....................")

#Set arguments
parser.add_argument("-state", help="Get state of device of specific IP", metavar='ip')
parser.add_argument("-tree", help="Create tree of devices with the device (ip) like root",metavar='ip')
parser.add_argument("-treeHTML", help="Create tree (HTML format) of devices with the device (ip) like root. Output is a IP.html file",metavar='ip')
parser.add_argument("-checkmac", help="Check MAC Address Activity in each Interface of device",metavar='ip')

parser.add_argument("-up", help="Insert bw up rom 'iddevice,idplan,pathfile' args")
parser.add_argument("-downrrd", help="Insert bw down from 'iddevice,idplan,pathfile' to rrd DB",action="store_true")
parser.add_argument("-uprrd", help="Insert bw up from 'iddevice,idplan,pathfile' to rrd DB",action="store_true")
parser.add_argument("-I", help="Create images png",action="store_true")
parser.add_argument("-cd", help="Get Configutarion of devices",action="store_true")
parser.add_argument("-db", help="Get database infotrmation",action="store_true")
parser.add_argument("-R", help="Create report for previous month",action="store_true")
parser.add_argument("-query", help="Execute query")
	
#Parse argv to args 
args = parser.parse_args()


#Workflow for arguments selection
#
#List of devices
if args.state:
	##
	ip = args.state 
	if validation.checkIpAddres(ip):
		result = export.getDeviceCurrentState(ip)
		print result 
	else:
		sys.exit(dtext['ipvalue'])
elif args.tree:
	ip = args.tree
	if validation.checkIpAddres(ip):
		result = export.treeOfHosts(ip,0)
		print result 
	else:
		sys.exit(dtext['ipvalue'])
		
elif args.treeHTML:
	ip = args.treeHTML
	if validation.checkIpAddres(ip):
		result = export.treeOfHostsHTML(ip,0,0)
		foutput = open('%s.html' % (ip),'w')
		foutput.write(result)
		foutput.close()
		print "Output %s.html was created" % (ip)
	else:
		sys.exit(dtext['ipvalue'])

elif args.checkmac:
    ip = args.checkmac
    if validation.checkIpAddres(ip):
        result = collector.getActivityMacOfDevice(ip)
        print result
    else:
        sys.exit(dtext['ipvalue'])

else:
	#No set any argument
	parser.print_help()
