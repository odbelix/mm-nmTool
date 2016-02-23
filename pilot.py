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


#listPublicHosts = collector.getListOfPublicIpHost('190.110.100.0',24)
#listPublicHosts2 = collector.getListOfPublicIpHost('190.110.101.0',24)
#ListHost = dict(listPublicHosts.items() + listPublicHosts2.items())
#dictHosts = collector.getHostActivityFromDevice('192.168.30.100',ListHost)

#result = export.hostToCSV(dictHosts)
#print result
deep = 0
hostsScanned = ['192.168.30.100','192.168.30.150']
lengthFather = 0
text = ""
def treeOfHosts(ip,deep):
	global hostsScanned
	global lengthFather
	global text
	hostsScanned.append(ip)
	namedevice = collector.getDeviceName(ip)
	#Getting Neighbours
	neighbours = collector.getListOfNeighbours(ip)
	dictOidData = neighbours["dict"]
	listOidData = neighbours["list"]

			
	line = "[%s|%s]" % (ip,namedevice)
	text=text + ("\t"*deep) + line + "\n"
	
	if len(listOidData) > 1:
		for son in dictOidData.keys():
			if dictOidData[son]['address'] not in hostsScanned:
				if ("AIR" not in dictOidData[son]['model'] and "hone" not in dictOidData[son]['model']):
					treeOfHosts(dictOidData[son]['address'],deep+1)
				else:
					line = "[%s|%s]" % (dictOidData[son]['address'],dictOidData[son]['name'])
					text=text + ("\t"*(deep+1)) + line + "\n"
	else:
		for son in dictOidData.keys():
			if dictOidData[son]['address'] not in hostsScanned:
				line = "[%s|%s]" % (dictOidData[son]['address'],dictOidData[son]['name'])
				text=text + ("\t"*deep) + line + "\n"
		
		
treeOfHosts("172.17.1.1",0)
print text



########for ip in getListOfActiveIp():
#dictInventory = {}
#for ip in collector.getListOfActiveIp('192.168.13.0',24):
########for ip in OutNetwork13:
	#if ip not in notValidIp:
		#dictInventory[ip] = {}
		#namedevice = collector.getDeviceName(ip)
		#serialdevice = collector.getDeviceSerial(ip)
		#modeldevice = collector.getDeviceModel(ip)
		#dictInventory[ip]['name']=namedevice
		#dictInventory[ip]['serial']=serialdevice
		#dictInventory[ip]['model']=modeldevice
		#poe = ""
		#interface = ""
		#if modeldevice is not None:
			#if "24" in modeldevice:
				#interface = "24"
			#elif "48" in modeldevice:
				#interface = "48"
			#if "P" in modeldevice:
				#poe = "POE"
			#else:
				#poe = ""

		#dictInventory[ip]['interfaces']=interface
		#dictInventory[ip]['poe']=poe
		#neighbours = collector.getListOfNeighbours(ip)
		#dictOidData = neighbours["dict"]
		#listOidData = neighbours["list"]
		#contPhone = 0
		#contAp = 0
		#contNeighbours = 0
		#for idData in listOidData:
			#if "Phone" in dictOidData[idData]["model"]:
				#contPhone = contPhone + 1
			#if "AIR" in dictOidData[idData]["model"]:
				#contAp = contAp + 1
			#contNeighbours = contNeighbours + 1
		#dictInventory[ip]['phones']=contPhone
		#dictInventory[ip]['aps']=contAp
		#dictInventory[ip]['neighbours']=contNeighbours		
#print export.deviceToCSV(dictInventory)


		#print "%s,%s" % (ip,namedevice)
#for ip in problems:
    #if ip not in notValidIp:
        #print "Device(" + ip,
        #namedevice = getDeviceName(ip)
        #print "," + namedevice + ")"
        #neighbours = getListOfNeighbours(ip)
        #listOidData = neighbours["list"]
        #dictOidData = neighbours["dict"]

        ###Getting names of localInterfaces where devices neihbours are connected
        #for idData in listOidData:
            #command = "snmpwalk -v 1 -c public %s %s%s" % (ip,list_oid_interfaces["localInterface"],idData[:idData[1:].index(".")-len(idData[1:])])
            #output = commands.getstatusoutput(command)
            #dictOidData[idData]["localInterface"] =parser.OutputToString(output[1])

        ###Getting traffic count for each interface
        #command = "snmpwalk -v 1 -c public %s %s" % (ip,list_oid_mactraffic["idInterface"])
        #output = commands.getstatusoutput(command)

        #listInterfaces = {}
        #for line in output[1].split("\n"):
            #if "Error" not in line and any(patter in line for patter in ids.patterkeys):
                #data =parser.OutputToStringFromInteger(line)
                #if str(data) not in listInterfaces.keys():
                    #listInterfaces[data] = {}
                    #listInterfaces[data]["count"] = 1
                #else:
                    #listInterfaces[data]["count"] =  listInterfaces[data]["count"] + 1


        ###Getting detail of localInterfaces what has irregular activity
        #listSummaryInterfaces = {}
        #for interface in listInterfaces:
            #command = "snmpwalk -v 1 -c public %s %s%s" % (ip,list_oid_interfaces["idInterface"],"."+interface)
            #output = commands.getstatusoutput(command)
            #if len(output[1]) is not 0:
                #idInterface =parser.OutputToStringFromInteger(output[1])
                #listSummaryInterfaces[idInterface] = {}
                #listSummaryInterfaces[idInterface]["idInterface"] = interface
                ### Diferent name for Interface
                ##command = "snmpwalk -v 1 -c public %s %s%s" % (ip_device,"1.3.6.1.2.1.31.1.1.1.1","."+str(OutputToStringFromInteger(output[1])))
                #command = "snmpwalk -v 1 -c public %s %s%s" % (ip,list_oid_interfaces["localInterface"],"."+str(OutputToStringFromInteger(output[1])))
                #output = commands.getstatusoutput(command)
                #if len(output[1]) is not 0:
                    ### Creating a new list with the summary of traffic mac for each interface
                    #listSummaryInterfaces[idInterface]["count"] = listInterfaces[interface]["count"]
                    #listSummaryInterfaces[idInterface]["name"] =parser.OutputToString(output[1])
                #else:
                    #listSummaryInterfaces.pop(idInterface)


        ###Printing summary detail of device and traffic irregular
        ## print "Device connected to device:%s : %s" % (namedevice,ip)
        ## print "####################################################################"
        #for idData in dictOidData:
            #key = idData[1:idData[1:].index(".")-len(idData[1:])]
            #if key in listSummaryInterfaces.keys():
                #if "SEP" in dictOidData[idData]["name"]:
                    #if listSummaryInterfaces[idData[1:idData[1:].index(".")-len(idData[1:])]]["count"] <= 2:
                        #listSummaryInterfaces.pop(idData[1:idData[1:].index(".")-len(idData[1:])])
                #else:
                    #listSummaryInterfaces.pop(idData[1:idData[1:].index(".")-len(idData[1:])])


            ## for indexData in dictOidData[idData]:
            ##     print indexData + " : " + dictOidData[idData][indexData]
            ## print "####################################################################"
        #for interface in listSummaryInterfaces:
            #if listSummaryInterfaces[interface]["count"] > 2:
                #print "\033[0;31m%s = %s\033[0m" %(listSummaryInterfaces[interface]["name"],listSummaryInterfaces[interface]["count"])
            #else:
                #print "%s = %s" %(listSummaryInterfaces[interface]["name"],listSummaryInterfaces[interface]["count"])
