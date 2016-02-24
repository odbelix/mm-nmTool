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

##Global VARIABLE
dictStatus = {}
dictStatus["1"] = "up"
dictStatus["2"] = "down"
dictStatus["3"] = "testing"
dictStatus["4"] = "unknown"
dictStatus["5"] = "dormant"
dictStatus["6"] = "notPresent"
dictStatus["7"] = "lowerLayerDown"
    



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
    if len(result) == 2:
    	result = result[1][1:-1]
    	return result.replace("\"","").lstrip()
    else:
    	print outputName
    	return None

def OutputToStringFromInteger(outputName):
    result = outputName.split("INTEGER:")
    result = result[1].replace(" ","")
    return result

def OutputToInterfaceStatus(outputInt):
    global dictStatus
    return dictStatus[outputInt]
    
