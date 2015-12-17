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
