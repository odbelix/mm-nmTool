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

import snmputils.collector as collector


generalContAP = 0
generalContSEP = 0
idSons = 0
deep = 0
text = ""
hostsScanned = []
lengthFather = 0
listDevices = []


def hostToCSV(dictHosts):
    cont = 1
    textResponse = "#,mac,name,ipaddress\n"
    for k in dictHosts.keys():
        textResponse = textResponse + ("%s;%s;%s;%s\n" % (str(cont),str(k),str(dictHosts[k]['name']),str(dictHosts[k]['ipAddress'])))
        cont = cont + 1
    return textResponse

def deviceToCSV(dictDevices):
    contLine = 1
    textResponse = "#;ip;name;serial;model;interfaces;phones;aps;neighbours\n"
    for k in dictDevices.keys():
        textResponse = textResponse + ("%s;%s;%s;%s;%s;%s;%s;%s;%s\n" % ( str(contLine),str(k),str(dictDevices[k]['name']),str(dictDevices[k]['serial']),str(dictDevices[k]['model']),str(dictDevices[k]['interfaces']),str(dictDevices[k]['phones']),str(dictDevices[k]['aps']),str(dictDevices[k]['neighbours'])))
        contLine = contLine + 1
    return textResponse
    

def getDeviceCurrentState(ip):
    namedevice = collector.getDeviceName(ip)
    modeldevice = collector.getDeviceModel(ip)
    serialdevice = collector.getDeviceSerial(ip)
    
    #Getting Neighbours
    neighbours = collector.getListOfNeighbours(ip)
    dictOidData = neighbours["dict"]
    listOidData = neighbours["list"]

    line = ""
    line = line + "Ip:\t" + ip + "\n"
    line = line + "Name:\t" + namedevice + "\n"
    line = line + "Serial:\t" + serialdevice + "\n"
    line = line + "Model:\t" + modeldevice + "\n\n\n"

    contDown = 0
    contAp = 0
    contSep = 0
    contLink = -1


    listInterfacesId = collector.getInterfaceIds(ip)
    for intId in listInterfacesId:
        status = collector.getInterfaceStatus(ip,intId)
        if status == "down":
            contDown += 1
        line = line + collector.getInterfaceName(ip,intId) + " :\t"+status
        lenTemp = len(line)
        for idInterface in listOidData:
            if intId == idInterface.split(".")[1]:
                line = line + "(" + dictOidData[idInterface]['name']
                if "address" in dictOidData[idInterface].keys():
                    line = line + ":" + dictOidData[idInterface]['address'] + ")\n"
                else:
                    line = line + ")\n"
                if "ap" in dictOidData[idInterface]['name']:
                    contAp += 1
                if "SEP" in dictOidData[idInterface]['name']:
                    contSep += 1
                if "rsw" in dictOidData[idInterface]['name'] or "sw" in dictOidData[idInterface]['name']:
                    contLink += 1
        
        if lenTemp == len(line):
            line = line + "\n"
        
    line = line + "\n\n"
    line = line + "NotCon:\t%d\n" % contDown
    line = line + "AP:\t%d\n" % contAp
    line = line + "TIP:\t%d\n" % contSep
    line = line + "LINKS:\t%d\n" % contLink
    
    return line


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

    #print "hola"
    
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
                
    return text    

def treeOfHostsHTML(ip,deep,parent):
    global hostsScanned
    global lengthFather
    global text
    #global idParent
    global idSons
    global generalContAP
    global generalContSEP
    global listDevices
    
    
    contAP = 0
    contSEP = 0
     
    hostsScanned.append(ip)
    namedevice = collector.getDeviceName(ip)
    serialdevice = collector.getDeviceSerial(ip)
    modeldevice = collector.getDeviceModel(ip)
    
    
    #Getting Neighbours
    neighbours = collector.getListOfNeighbours(ip)
    dictOidData = neighbours["dict"]
    
    listOidData = neighbours["list"]

    idParent = 0
     
    if deep == 0:
        text = "<!DOCTYPE html>\n"
        text = text + """<html lang="en-US">\n"""
        text = text + "<head>\n<title>ROOT: " +ip+ "</title>\n"
        text = text + "<style>a { color: blue;}</style>\n"
        text = text + """<script src="http://code.jquery.com/jquery-1.12.0.min.js"></script>\n"""
        text = text + """<script>$( document ).ready(function() {$('.list > li a').click(function() {$(this).parent().find('ul').toggle();}); $('.list > li a').each(function(){$(this).parent().find('ul').toggle();}); $(function () { $('[data-toggle="popover"]').popover() }); });</script>"""
        text = text + """<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">"""
        text = text + """<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js" integrity="sha384-0mSbJDEHialfmuBBQP6A4Qrprq5OVfW37PRR3j5ELqxss1yVqOtnepnHVP9aJ7xS" crossorigin="anonymous"></script>"""
        text = text + "</head>"
        text = text + """<body><div class="container"><div class="page-header"><h1>%s</h1><p class="lead">%s</p></div>""" % (ip,namedevice)
        text = text + """<table class="table table-bordered"><tr><th>Device TREE</th></tr><tr><td>"""
        text = text + """<ul  class="list">\n"""
    
    
    idSons = idSons + 1
    
    ###device for the table
    device = {}
    device["name"] = namedevice
    device["serial"] = serialdevice
    device["model"] = modeldevice
    device["ipaddress"] = ip
    device["link"] = "device%d" % (idSons)
    
    listDevices.append(device)
    
    
    line = """<li id="device-%d" parent="%d" deep="%d" ><a class="btn btn-info btn-xs">%s</a>[%s]""" % (idSons,parent,deep,ip,namedevice)
    popover = """<button type="button" class="btn btn-xs btn-default" data-toggle="popover" title="Device: %s" """ % (ip)
    detail = "%s | %s | %s " % (namedevice,serialdevice,modeldevice)
    popover = popover + """ data-content="%s"><span class="glyphicon glyphicon-expand" aria-hidden="true"></span></button> """ % detail
    
    line = line + popover

    
    
    idParent = idSons
    text=text + ("\t"*deep) + line + "\n"
    
    if len(listOidData) > 1:
        text = text + ("\t"*deep) + "<ul>" + "\n"
    
        for son in dictOidData.keys():
            if ("AIR" not in dictOidData[son]['model'] and "hone" not in dictOidData[son]['model']):
                if 'address' in dictOidData[son].keys():
                    if dictOidData[son]['address'] not in hostsScanned:
                        treeOfHostsHTML(dictOidData[son]['address'],deep+1,idParent)
                else:
                    idSons = idSons + 1
                    line = """<li id="%d" parent="%d" deep="%d">[%s|%s]</li>""" % (idSons,idParent,deep,"no ip address",dictOidData[son]['name'])
                    text=text + ("\t"*(deep+1)) + line + "\n"
            else:
                idSons = idSons + 1
                if 'address' in dictOidData[son].keys():
                    if 'SEP' in dictOidData[son]['name']:
                        contSEP = contSEP + 1
                        line = """<li id="%d" parent="%d" deep="%d"><a href="http://%s" target="_blank" class="btn btn-primary btn-xs"><span class="glyphicon glyphicon-phone-alt" aria-hidden="true"></span> %s</a> [%s]</li>""" % (idSons,idParent,deep,dictOidData[son]['address'],dictOidData[son]['address'],dictOidData[son]['name'])
                    elif 'ap-' in dictOidData[son]['name']:
                        contAP = contAP + 1
                        line = """<li id="%d" parent="%d" deep="%d"><a class="btn btn-success btn-xs" aria-label="Left Align"><span class="glyphicon glyphicon-signal" aria-hidden="true"></span> %s</a> [%s]</li>""" % (idSons,idParent,deep,dictOidData[son]['address'],dictOidData[son]['name'])
                    else:
                        line = """<li id="%d" parent="%d" deep="%d">[%s|%s]</li>""" % (idSons,idParent,deep,dictOidData[son]['address'],dictOidData[son]['name'])
                else:
                    if 'SEP' in dictOidData[son]['name']:
                        contSEP = contSEP + 1
                        line = """<li id="%d" parent="%d" deep="%d"><a href="http://%s" target="_blank" class="btn btn-primary btn-xs"><span class="glyphicon glyphicon-phone-alt" aria-hidden="true"></span> %s</a> [%s]</li>""" % (idSons,idParent,deep,"no ip address","no ip address",dictOidData[son]['name'])
                    elif 'ap-' in dictOidData[son]['name']:
                        contAP = contAP + 1
                        line = """<li id="%d" parent="%d" deep="%d"><a class="btn btn-success btn-xs" aria-label="Left Align"><span class="glyphicon glyphicon-signal" aria-hidden="true"></span> %s</a> [%s]</li>""" % (idSons,idParent,deep,"no ip address",dictOidData[son]['name'])
                    else:    
                        line = """<li id="%d" parent="%d" deep="%d">[%s|%s]</li>""" % (idSons,idParent,deep,"no ip address",dictOidData[son]['name'])
                
                text=text + ("\t"*(deep+1)) + line + "\n"
            
        generalContAP = generalContAP + contAP
        generalContSEP = generalContSEP + contSEP
        
        text = text + ("\t"*deep) + "</ul>\n" 
    
        text = text + """<div class="btn btn-default btn-xs"><span class="glyphicon glyphicon-signal"> %s </span>""" % str(contAP)
        text = text + """ | <span class="glyphicon glyphicon-phone-alt" > %s </span></div>""" % str(contSEP)
        
        text = text + ("\t"*deep) + "</li>" + "\n"
    else:
        for son in dictOidData.keys():
            if dictOidData[son]['address'] not in hostsScanned:
                idSons = idSons + 1
                line = """<li id="%d" parent="%d" deep="%d">[%s|%s]</li>""" % (idSons,idParent,deep,dictOidData[son]['address'],dictOidData[son]['name'])
                text=text + ("\t"*deep) + line + "\n"
    
    if deep == 0:            
        text = text + "</ul>\n"
        text = text + "</td></tr></table>"
        text = text + """<div ><table class="table table-bordered"><tr><th>Type</th><th>Quantity</th></tr>"""
        text = text + """<tr><td>AP <span class="glyphicon glyphicon-signal" aria-hidden="true"></span></td><td> %s </td></tr>""" % str(generalContAP)
        text = text + """<tr><td>TIP <span class="glyphicon glyphicon-phone-alt" aria-hidden="true"></span></td><td> %s </td></tr>""" % str(generalContSEP)
        text = text + """</table></div>"""
                
        #Table with DEVICE INVENTORI
        text = text + """<div><table class="table table-bordered"><tr><th>#</th><th>Name</th><th>Ip</th><th>Serial</th><th>Model</th></tr>"""
        iddevice = 1
        tabletext = ""
        for device in listDevices:
            tabletext = tabletext + """<tr><td>%d</td><td><a href="#%s">%s</a></td><td>%s</td><td>%s</td><td>%s</td></tr>""" % (iddevice,device["link"],device["name"],device["ipaddress"],device["serial"],device["model"])
            iddevice = iddevice + 1
        
        tabletext = tabletext + """</table></div>"""
        text = text + tabletext
        
        text = text + "</div>\n"
        text = text + "</body>\n"
        text = text + "</html>\n"
    return text    

