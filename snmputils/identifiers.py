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

## OID for get neighbour information useful for the Organization
neighbour = {}
neighbour['address'] = 'iso.3.6.1.4.1.9.9.23.1.2.1.1.4'
neighbour['name'] =  'iso.3.6.1.4.1.9.9.23.1.2.1.1.6'
neighbour['model'] = 'iso.3.6.1.4.1.9.9.23.1.2.1.1.8'
## OID for get device information useful for the inventary
currentdevice = {}
currentdevice['name'] = 'iso.3.6.1.2.1.1.5'
currentdevice['serial'] = 'iso.3.6.1.2.1.47.1.1.1.1.11'
currentdevice['model'] =  '1.3.6.1.2.1.47.1.1.1.1.13'
## OID for get device information useful for about active hosts
activehost = {}
activehost['macAddress'] = 'iso.3.6.1.2.1.3.1.1.2'
activehost['ipAddress'] = 'iso.3.6.1.2.1.3.1.1.3'
## OID for get device information useful for interface identification
infoInterface = {}
infoInterface['local'] = 'iso.3.6.1.2.1.2.2.1.2'
infoInterface['id'] =  'iso.3.6.1.2.1.17.1.4.1.2'
infoInterface['status'] =  'iso.3.6.1.2.1.2.2.1.8'





patterkeys = ['Hex-STRING:', 'INTEGER:', 'STRING:']



