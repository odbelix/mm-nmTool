########################################################################
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
import snmputils.identifiers as ids
import snmputils.parser as parser
import re


##Get List of Active Host from one device
def getHostActivityFromDevice(ip,listHostPublic):
    listOidData = []
    dictOidData = {}    
    command = "snmpwalk -v 1 -c public %s %s" % (ip,ids.activehost['macAddress'])
    output = commands.getstatusoutput(command)
    command = "snmpwalk -v 1 -c public %s %s" % (ip,ids.activehost['ipAddress'])
    output1 = commands.getstatusoutput(command)
    
    resultMacs = output[1].split("\n")
    resultIps =  output1[1].split("\n")
    
    dictHostAlive = {}
    
    for lineMac in resultMacs:
		if len(lineMac.split("Hex-STRING:")) == 2:
			data = parser.changeMacFormat(lineMac.split("Hex-STRING:")[1])
			OidData = lineMac.split("Hex-STRING:")[0].replace(ids.activehost['macAddress'],"")
			if data is not dictHostAlive.keys:
				dictHostAlive[data] = {}
			for lineIp in resultIps:
				if len(lineIp.split("IpAddress:")) == 2:
					if OidData in lineIp:
						ip = lineIp.split("IpAddress:")[1].replace(" ","")
						dictHostAlive[data]['ipAddress'] = ip
						if ip in listHostPublic.keys():
							dictHostAlive[data]['name'] = listHostPublic[dictHostAlive[data]['ipAddress']]
						else:
							dictHostAlive[data]['name'] = None
    return dictHostAlive


## Get List of Host in Public Network
def getListOfPublicIpHost(network,mask):
    listPublicIps = {}
    arryNetwork = network.split(".")
    command = "nmap -sP %s/%s | grep %s | awk -F' ' '{print $5','$6;}'" % (network,mask,arryNetwork[0])
    output = commands.getstatusoutput(command)
    if len(output) == 2:
        result = output[1].split("\n")
        list_ip = []
        for line in result:
            #print line
            if re.search('[a-zA-Z]',line) is not None:
                dataLine = line.replace("(","")
                dataLine = dataLine.replace(")","")
                dataArray = dataLine.split(" ")
                listPublicIps[dataArray[1]]=dataArray[0]
            else:
                listPublicIps[line.replace(" ","")]=None

    return listPublicIps           
	
	
		

## Get list of ip address from all switches in private network
def getListOfActiveIp(network,mask):
    arryNetwork = network.split(".")
    command = "nmap -sP %s/%s | grep '%s'" % (network,mask,arryNetwork[0])
    output = commands.getstatusoutput(command)
    if len(output) == 2:
        result = output[1].split("\n")
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
    else:
        sys.exit("We can get Host from the network, try again later")

##Getting name of device
def getDeviceName(ip):
    output = commands.getstatusoutput("snmpwalk -v 1 -c public %s %s" % (ip,ids.currentdevice["name"]))
    namedevice = parser.OutputToString(output[1])
    return namedevice


##Getting serial of device
def getDeviceSerial(ip):
    output = commands.getstatusoutput("snmpwalk -v 1 -c public %s %s" % (ip,ids.currentdevice["serial"]))
    outputlist = output[1].split("\n")
    for line in outputlist:
		if "STRING:" in line:
			serialdevice = parser.OutputToString(line)
			if len(serialdevice) > 5:
				return serialdevice

##Getting name of device
def getDeviceModel(ip):
    output = commands.getstatusoutput("snmpwalk -v 1 -c public %s %s" % (ip,ids.currentdevice["model"]))
    outputlist = output[1].split("\n")
    for line in outputlist:
		if "STRING:" in line:
			modeldevice = parser.OutputToString(line)
			if len(modeldevice) > 5:
				return modeldevice


def getInterfaceAlias(ip,idInterface):
    comm = "snmpwalk -v 1 -c public %s %s" % (ip, ids.infoInterface["alias"] + "." + idInterface)
    output = commands.getstatusoutput(comm)
    outputlist = output[1].split("\n")
    for line in outputlist:
        if "STRING:" in line:
            aliasInterface = parser.OutputToString(line)
            return aliasInterface
        else:
            return "Not define"

def getInterfaceName(ip,idInterface):
    output = commands.getstatusoutput("snmpwalk -v 1 -c public %s %s" % (ip,ids.infoInterface["local"]+"."+idInterface))
    outputlist = output[1].split("\n")
    for line in outputlist:
		if "STRING:" in line:
			nameInterface = parser.OutputToString(line)
			if len(nameInterface) > 4:
				return nameInterface

def getInterfaceIds(ip):
    output = commands.getstatusoutput("snmpwalk -v 1 -c public %s %s" % (ip,ids.infoInterface["id"]))
    outputlist = output[1].split("\n")
    listId = []
    for line in outputlist:
		if "INTEGER:" in line:
			idInterface = parser.OutputToStringFromInteger(line)
			listId.append(idInterface)
	
    return listId


def getInterfaceStatus(ip,idInterface):
    output = commands.getstatusoutput("snmpwalk -v 1 -c public %s %s" % (ip,ids.infoInterface["status"]+"."+idInterface))
    outputlist = output[1].split("\n")
    for line in outputlist:
		if "INTEGER:" in line:
			statusInterface = parser.OutputToStringFromInteger(line)
			return parser.OutputToInterfaceStatus(statusInterface)

##Get list of neighbours for one device
def getListOfNeighbours(ip):
    listOidData = []
    dictOidData = {}
    for oid in ids.neighbour:
        command = "snmpwalk -v 1 -c public %s %s" % (ip,ids.neighbour[oid])
        output = commands.getstatusoutput(command)
        outputlist = output[1].split("\n")
        for line in outputlist:
            if any(patter in line for patter in ids.patterkeys):
                oidData = line.split(" ")[0].replace(ids.neighbour[oid],"")
                if oidData not in listOidData:
                    listOidData.append(oidData)
                    dictOidData[oidData] = {}
                if oid == "address":
                    dictOidData[oidData][oid] =parser.HextoStringIp(line)
                else:
                    dictOidData[oidData][oid] =parser.OutputToString(line)
    result = {'list':listOidData,'dict':dictOidData}
    return result




def getActivityMacOfDevice(ip):
    result = " "

    result = result + "Device\n"
    result = result + "ipAddress:\t" + str(ip )+ "\n"
    result = result + "Name:\t" + getDeviceName(ip) + "\n"
    result = result + "Model:\t" + getDeviceModel(ip) + "\n"
    result = result + "Serial:\t" + getDeviceSerial(ip) + "\n\n\n"

    neighbours = getListOfNeighbours(ip)
    listOidData = neighbours["list"]
    dictOidData = neighbours["dict"]

    ####Getting names of localInterfaces where devices neihbours are connected
    for idData in listOidData:
        command = "snmpwalk -v 1 -c public %s %s%s" % (ip,ids.infoInterface["local"],idData[:idData[1:].index(".")-len(idData[1:])])
        output = commands.getstatusoutput(command)
        dictOidData[idData]["localInterface"] = parser.OutputToString(output[1])

    ####Getting traffic count for each interface
    command = "snmpwalk -v 1 -c public %s %s" % (ip,ids.infomactraffic["id"])
    output = commands.getstatusoutput(command)

    listInterfaces = {}
    for line in output[1].split("\n"):
        if "Error" not in line and any(patter in line for patter in ids.patterkeys):
            data =parser.OutputToStringFromInteger(line)
            if str(data) not in listInterfaces.keys():
                listInterfaces[data] = {}
                listInterfaces[data]["count"] = 1
            else:
                listInterfaces[data]["count"] =  listInterfaces[data]["count"] + 1


    ####Getting detail of localInterfaces what has irregular activity
    listSummaryInterfaces = {}
    for interface in listInterfaces:
        command = "snmpwalk -v 1 -c public %s %s%s" % (ip,ids.infoInterface["idinter"],"."+interface)
        output = commands.getstatusoutput(command)
        if len(output[1]) is not 0:
            idInterface =parser.OutputToStringFromInteger(output[1])
            listSummaryInterfaces[idInterface] = {}
            listSummaryInterfaces[idInterface]["idInterface"] = interface
                #### Diferent name for Interface
                ###command = "snmpwalk -v 1 -c public %s %s%s" % (ip_device,"1.3.6.1.2.1.31.1.1.1.1","."+str(OutputToStringFromInteger(output[1])))
            command = "snmpwalk -v 1 -c public %s %s%s" % (ip,ids.infoInterface["local"],"."+str(parser.OutputToStringFromInteger(output[1])))
            output = commands.getstatusoutput(command)
            if len(output[1]) is not 0:
                #### Creating a new list with the summary of traffic mac for each interface
                listSummaryInterfaces[idInterface]["count"] = listInterfaces[interface]["count"]
                listSummaryInterfaces[idInterface]["name"] =parser.OutputToString(output[1])
            else:
                listSummaryInterfaces.pop(idInterface)


        ####Printing summary detail of device and traffic irregular
        ### print "Device connected to device:%s : %s" % (namedevice,ip)
        ### print "####################################################################"
    #for idData in dictOidData:
    #    key = idData[1:idData[1:].index(".")-len(idData[1:])]
    #    if key in listSummaryInterfaces.keys():
    #        if "SEP" in dictOidData[idData]["name"]:
    #             if listSummaryInterfaces[idData[1:idData[1:].index(".")-len(idData[1:])]]["count"] <= 2:
    #                listSummaryInterfaces.pop(idData[1:idData[1:].index(".")-len(idData[1:])])
    #        else:
    #            listSummaryInterfaces.pop(idData[1:idData[1:].index(".")-len(idData[1:])])


            ### for indexData in dictOidData[idData]:
            ###     print indexData + " : " + dictOidData[idData][indexData]
            ### print "####################################################################"
    for interface in listSummaryInterfaces:
        if listSummaryInterfaces[interface]["count"] > 2:
            result = result + "\033[0;31m%s = %s\033[0m\n" %(listSummaryInterfaces[interface]["name"],listSummaryInterfaces[interface]["count"])
        else:
            result = result + "%s = %s\n" %(listSummaryInterfaces[interface]["name"],listSummaryInterfaces[interface]["count"])

    return result