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
    
