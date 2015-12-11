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

list_oid_neighbour = {'address': 'iso.3.6.1.4.1.9.9.23.1.2.1.1.4',
'name': 'iso.3.6.1.4.1.9.9.23.1.2.1.1.6',
'model': 'iso.3.6.1.4.1.9.9.23.1.2.1.1.8'}

list_oid_interfaces = {'localInterface':'iso.3.6.1.2.1.2.2.1.2' , 'idInterface' : 'iso.3.6.1.2.1.17.1.4.1.2' }
list_oid_mactraffic = {'idInterface':'iso.3.6.1.2.1.17.4.3.1.2'}
list_oid_currentdevice = {'name':'iso.3.6.1.2.1.1.5', 'serial':'iso.3.6.1.2.1.47.1.1.1.1.11', 'model':'1.3.6.1.2.1.47.1.1.1.1.13' }
list_patter_keys = ['Hex-STRING:', 'INTEGER:', 'STRING:']


## Change format of Mac, From SNMP format to HexaFormat
def changeMacFormat(macaddress):
    result = macaddress.replace(" ",":")
    result = result.replace("\"","")
    result = result.rstrip(":")
    result = result.lstrip(":")
    result = result.lower()
    return result

def HextoStringIp(hexString):
    result = hexString.split("Hex-STRING:")[1]
    result = result[1:-1].split(" ")
    stringIp = ""
    for strData in result:
         stringIp += str(int(strData, 16)) + "."
    return stringIp[:-1]

def OutputToString(outputName):
    result = outputName.split("STRING:")#[1]
    result = result[1][1:-1]
    return result.replace("\"","").lstrip()

def OutputToStringFromInteger(outputName):
    result = outputName.split("INTEGER:")
    result = result[1].replace(" ","")
    return result

def getStringIpFromScan(output):
    result = output.split("\n")
    list_ip = []
    for line in result:
        if len(line) > 50:
            start = line.index("(")
            end = line.index(")")
            list_ip.append(line[start+1:end])
        if len(line) > 25 and len(line) < 50:
            start = line.index("1")
            end = len(line)-1
            list_ip.append(line[start:end+1])
    return list_ip

## Get list of ip address from all switches in private network
def getListOfActiveIp():
    
    output = commands.getstatusoutput("nmap -sP 192.168.13.0/24 | grep '192'")
    #output = commands.getstatusoutput("nmap -sP 172.17.1.0/24 | grep '172'")
    #output = commands.getstatusoutput("nmap -sP 10.3.1.0/24 | grep '10.3'")
    #output = commands.getstatusoutput("nmap -sP 172.18.1.0/24 | grep '172'")
    #output = commands.getstatusoutput("nmap -sP 172.19.1.0/24 | grep '172'")
    #output = commands.getstatusoutput("nmap -sP 10.1.1.0/24 | grep '10.1'")
    listIp = getStringIpFromScan(output[1])
    return listIp

##Getting name of device
def getDeviceName(ip):
    output = commands.getstatusoutput("snmpwalk -v 1 -c public %s %s" % (ip,list_oid_currentdevice["name"]))
    namedevice = OutputToString(output[1])
    return namedevice

##Getting name of device
def getDeviceSerial(ip):
    output = commands.getstatusoutput("snmpwalk -v 1 -c public %s %s" % (ip,list_oid_currentdevice["serial"]))
    outputlist = output[1].split("\n")
    for line in outputlist:
		if "STRING:" in line:
			serialdevice = OutputToString(line)
			if len(serialdevice) > 5:
				return serialdevice
    
##Getting name of device
def getDeviceModel(ip):
    output = commands.getstatusoutput("snmpwalk -v 1 -c public %s %s" % (ip,list_oid_currentdevice["model"]))
    outputlist = output[1].split("\n")
    for line in outputlist:
		if "STRING:" in line:
			modeldevice = OutputToString(line)
			if len(modeldevice) > 5:
				return modeldevice

##Get list of neighbours for one device
def getListOfNeighbours(ip):
    listOidData = []
    dictOidData = {}
    for oid in list_oid_neighbour:
        command = "snmpwalk -v 1 -c public %s %s" % (ip,list_oid_neighbour[oid])
        output = commands.getstatusoutput(command)
        outputlist = output[1].split("\n")
        for line in outputlist:
            if any(patter in line for patter in list_patter_keys):
                oidData = line.split(" ")[0].replace(list_oid_neighbour[oid],"")
                if oidData not in listOidData:
                    listOidData.append(oidData)
                    dictOidData[oidData] = {}
                if oid == "address":
                    dictOidData[oidData][oid] = HextoStringIp(line)
                else:
                    dictOidData[oidData][oid] = OutputToString(line)
    result = {'list':listOidData,'dict':dictOidData}
    return result

# if len(sys.argv) is not 2:
#     sys.exit("Proble with parameter")
#
# ip_device = sys.argv[1]

#detectedDeviceWithIrregularActivity
WarningDevices = ['192.168.13.4','192.168.13.11','192.168.13.12','192.168.13.13','192.168.13.19','192.168.13.35','192.168.13.52','192.168.13.72','192.168.13.80','192.168.13.87','192.168.13.110','192.168.13.111','192.168.13.159','192.168.13.167','192.168.13.169','192.168.13.170','192.168.13.193','192.168.13.227','192.168.13.230','192.168.13.233']

notValidIp = ['192.168.13.171','172.17.1.26','172.17.1.27','172.17.1.250','172.18.1.250','172.19.1.1','10.3.1.1','10.1.1.3']

OutNetwork13 = ['192.168.30.100','192.168.15.200','192.168.30.150','192.168.60.239','192.168.20.173','192.168.17.213','192.168.17.212',
'192.168.17.211','192.168.80.241','192.168.15.200','192.168.20.251','192.168.20.249',
'192.168.1.241','192.168.1.242','192.168.1.243','192.168.90.199','192.168.1.244','192.168.1.240']

############ X,X,GW-Sede-Curico,VG-Sede-Curico
problems = ['192.168.13.31','192.168.13.170','172.17.1.26','172.17.1.27']
print "#,ip,name,serial,model,interfaces,phones,ap,neighbours"
cont = 1
for ip in getListOfActiveIp():
#for ip in OutNetwork13:
	if ip not in notValidIp:
		namedevice = getDeviceName(ip)
		serialdevice = getDeviceSerial(ip)
		modeldevice = getDeviceModel(ip)
		poe = ""
		interface = ""
		if modeldevice is not None:
			if "24" in modeldevice:
				interface = "24"
			elif "48" in modeldevice:
				interface = "48"		
			if "P" in modeldevice:
				poe = "POE"
			else:
				poe = ""
		
		
		neighbours = getListOfNeighbours(ip)
		dictOidData = neighbours["dict"]
		listOidData = neighbours["list"]
		contPhone = 0
		contAp = 0
		contNeighbours = 0
		for idData in listOidData:
			if "Phone" in dictOidData[idData]["model"]:
				contPhone = contPhone + 1
			if "AIR" in dictOidData[idData]["model"]:
				contAp = contAp + 1	
			contNeighbours = contNeighbours + 1
			
		print "%s,%s,%s,%s,%s,%s,%s,%s,%s" % (ip,namedevice,serialdevice,modeldevice,interface,poe,str(contPhone),str(contAp),str(contNeighbours))
		cont = cont + 1
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
            #dictOidData[idData]["localInterface"] = OutputToString(output[1])

        ###Getting traffic count for each interface
        #command = "snmpwalk -v 1 -c public %s %s" % (ip,list_oid_mactraffic["idInterface"])
        #output = commands.getstatusoutput(command)

        #listInterfaces = {}
        #for line in output[1].split("\n"):
            #if "Error" not in line and any(patter in line for patter in list_patter_keys):
                #data = OutputToStringFromInteger(line)
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
                #idInterface = OutputToStringFromInteger(output[1])
                #listSummaryInterfaces[idInterface] = {}
                #listSummaryInterfaces[idInterface]["idInterface"] = interface
                ### Diferent name for Interface
                ##command = "snmpwalk -v 1 -c public %s %s%s" % (ip_device,"1.3.6.1.2.1.31.1.1.1.1","."+str(OutputToStringFromInteger(output[1])))
                #command = "snmpwalk -v 1 -c public %s %s%s" % (ip,list_oid_interfaces["localInterface"],"."+str(OutputToStringFromInteger(output[1])))
                #output = commands.getstatusoutput(command)
                #if len(output[1]) is not 0:
                    ### Creating a new list with the summary of traffic mac for each interface
                    #listSummaryInterfaces[idInterface]["count"] = listInterfaces[interface]["count"]
                    #listSummaryInterfaces[idInterface]["name"] = OutputToString(output[1])
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
