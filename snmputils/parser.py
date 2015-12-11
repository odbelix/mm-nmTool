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
