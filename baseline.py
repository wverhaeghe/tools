### test test
#!/usr/bin/python

import os, sys
from xml.dom import minidom

config_file='bp.xml'
result_file='runme.exp'
cprompt="(Cisco Controller) >"

xmlconf = minidom.parse(config_file)
security_list = xmlconf.getElementsByTagName('security_cmd')
cleanair_list = xmlconf.getElementsByTagName('cleanair_cmd')
mdns_list = xmlconf.getElementsByTagName('mdns_cmd')
radio_exb_list = xmlconf.getElementsByTagName('radio_exb_cmd')
radio_incb_list = xmlconf.getElementsByTagName('radio_incb_cmd')
qos_list = xmlconf.getElementsByTagName('qos_cmd')
rf_list = xmlconf.getElementsByTagName('rf_cmd')
multicast_list = xmlconf.getElementsByTagName('multicast_cmd')

def write_start_expect(f):
   f.write('#!/usr/bin/expect'+ os.linesep)
   f.write('set timeout 20'+ os.linesep)
   f.write('set ip [lindex $argv 0]'+ os.linesep)
   f.write('set loginUser [lindex $argv 1]'+ os.linesep)
   f.write('set loginPassword [lindex $argv 2]'+ os.linesep)
   f.write('set prompt "'+cprompt+'"'+ os.linesep)
   f.write('log_user 0'+ os.linesep)
   f.write('spawn ssh -l $loginUser $ip'+ os.linesep)
   f.write('expect_after eof {exit 0}'+ os.linesep)
   f.write('send_user "\[\+\] Logged in...\\n"'+ os.linesep) 
   f.write('expect "User:" {send "$loginUser\\r"}'+ os.linesep)
   f.write('expect "Password:" {send "$loginPassword\\r"}'+ os.linesep)
   f.write('expect $prompt {}'+ os.linesep)

def write_end_expect(f):
   f.write('send_user "\[\+\] Done\\n"'+ os.linesep)
   f.write('expect $prompt {}'+ os.linesep) 
   f.write('exit'+ os.linesep)
   f.close()

def write_baseline(f):
   f.write('send_user "\[\+\] Adding security...\\n"'+ os.linesep)
   for s in security_list:
      f.write('send "'+ s.attributes['name'].value+'\\r"'+ os.linesep)

   f.write('send_user "\[\+\] Adding Cleanair...\\n"'+ os.linesep)
   for s in cleanair_list:
      f.write('send "'+ s.attributes['name'].value+'\\r"'+ os.linesep)
 
   f.write('send_user "\[\+\] Adding mDNS...\\n"'+ os.linesep)
   for s in mdns_list:
      f.write('send "'+ s.attributes['name'].value+'\\r"'+ os.linesep)		
   
   f.write('send_user "\[\+\] Adding Multicast...\\n"'+ os.linesep)
   for s in multicast_list:
      f.write('send "'+ s.attributes['name'].value+'\\r"'+ os.linesep)	

   f.write('send_user "\[\+\] Adding QOS...\\n"'+ os.linesep)
   for s in qos_list:
      f.write('send "'+ s.attributes['name'].value+'\\r"'+ os.linesep)		

   f.write('send_user "\[\+\] Adding RF...\\n"'+ os.linesep)
   for s in rf_list:
      f.write('send "'+ s.attributes['name'].value+'\\r"'+ os.linesep)		



def syslog_ap_logging(f,syslog_server):
   f.write('send_user "\[\+\] Adding Global Syslog...\\n"'+ os.linesep)
   f.write('send "config ap syslog host global '+syslog_server+'\\r"'+ os.linesep)

def multicast_multicast(f,multicast_address):
   f.write('send_user "\[\+\] Adding Multicast-Multicast...\\n"'+ os.linesep)
   f.write('send "config network multicast mode multicast '+multicast_address+'\\r"'+ os.linesep)
   f.write('send "config mobility multicast-mode enable '+multicast_address+'\\r"'+ os.linesep)

def disable_radio(f):
   f.write('send_user "\[\+\] Disabling radios...\\n"'+ os.linesep)
   f.write('send "config 802.11a disable network\\r"'+ os.linesep)
   f.write('expect "*(y/n)" {send "y\\r"}'+ os.linesep)
   f.write('send "config 802.11b disable network\\r"'+ os.linesep)
   f.write('expect "*(y/n)" {send "y\\r"}'+ os.linesep)   

def enable_gradio(f):
   f.write('send_user "\[\+\] Enabling G Radio...\\n"'+ os.linesep)
   f.write('send "config 802.11b 11gSupport enable\\r"'+ os.linesep)
   f.write('expect "*(y/n)" {send "y\\r"}'+ os.linesep)   

def enable_radio(f):
   f.write('send_user "\[\+\] Enabling Radios...\\n"'+ os.linesep)
   f.write('send "config 802.11b enable network\\r"'+ os.linesep)
   f.write('send "config 802.11a enable network\\r"'+ os.linesep)

os.system('clear')
print ("===================================")
print ("=   Wireless Config Generator     =")
print ("= wim.verhaeghe@dimensiondata.com =")
print ("===================================")
print ("[1] Generate baseline with b")
print ("[2] Generate baseline without b")
print ("[3] Section")
print ("===================================")

x = input('Choice:') 
x = int(x)

if x == 1:
   syslog_server = input('Syslog server:') 
   multicast_address = input('Multicast address:')
   with open(result_file, 'w') as f:
       
      write_start_expect(f)
      disable_radio(f)
      write_baseline(f)
      syslog_ap_logging(f,syslog_server)
      multicast_multicast(f,multicast_address)
      enable_gradio(f)

      f.write('send_user "\[\+\] Adding Radio with b...\\n"'+ os.linesep)
      for s in radio_incb_list:
         f.write('send "'+ s.attributes['name'].value+'\\r"'+ os.linesep)		
      
      enable_radio(f)
      write_end_expect(f)

if x == 2:
   syslog_server = input('Syslog server:') 
   multicast_address = input('Multicast address:')
   with open(result_file, 'w') as f:
       
      write_start_expect(f)
      disable_radio(f)
      write_baseline(f)
      syslog_ap_logging(f,syslog_server)
      multicast_multicast(f,multicast_address)	
      enable_gradio(f)

      f.write('send_user "\[\+\] Adding Radio without b...\\n"'+ os.linesep)
      for s in radio_exb_list:
         f.write('send "'+ s.attributes['name'].value+'\\r"'+ os.linesep)		
      
      enable_radio(f)
      write_end_expect(f)

if x==3:
   os.system('clear')
   print ("===================================")
   print ("=   Wireless Config Generator     =") 
   print ("= wim.verhaeghe@dimensiondata.com =")
   print ("===================================")
   print ('[1] Multicast')
   print ('[2] mDNS')
   print ('[3] Cleanair')
   print ('[4] Security')
   print ('[5] QOS')
   print ('[6] Radio b')
   print ('[7] Radio g')
   print ('===================================')
   x = input('Choice:') 
   x = int(x)
   
   if x == 1:
      with open(result_file, 'w') as f:
         write_start_expect(f)
         f.write('send_user "\[\+\] Adding Multicast...\\n"'+ os.linesep)

         for s in multicast_list:
            f.write('send "'+ s.attributes['name'].value+'\\r"'+ os.linesep)
         
         write_end_expect(f)

   if x == 2:
      with open(result_file, 'w') as f:
         write_start_expect(f)
         f.write('send_user "\[\+\] Adding mDNS...\\n"'+ os.linesep)

         for s in mdns_list:
            f.write('send "'+ s.attributes['name'].value+'\\r"'+ os.linesep)		
        
         write_end_expect(f)   

   if x == 3:
      with open(result_file, 'w') as f:
         write_start_expect(f)
         disable_radio(f)

         f.write('send_user "\[\+\] Adding Cleanair...\\n"'+ os.linesep)

         for s in cleanair_list:
            f.write('send "'+ s.attributes['name'].value+'\\r"'+ os.linesep)
         
         enable_radio(f)
         write_end_expect(f)

   if x == 4:
      with open(result_file, 'w') as f:
         write_start_expect(f)
	 
         f.write('send_user "\[\+\] Adding Security...\\n"'+ os.linesep)

         for s in security_list:
            f.write('send "'+ s.attributes['name'].value+'\\r"'+ os.linesep)

         write_end_expect(f)

   if x == 5:
      with open(result_file, 'w') as f:
         write_start_expect(f)
         disable_radio(f)

         f.write('send_user "\[\+\] Adding QOS...\\n"'+ os.linesep)

         for s in qos_list:
            f.write('send "'+ s.attributes['name'].value+'\\r"'+ os.linesep)

         enable_radio(f)
         write_end_expect(f)

   if x == 6:
      with open(result_file, 'w') as f:
         write_start_expect(f)
         disable_radio(f)
         enable_gradio(f)

         f.write('send_user "\[\+\] Adding Radio b...\\n"'+ os.linesep)

         for s in radio_incb_list:
            f.write('send "'+ s.attributes['name'].value+'\\r"'+ os.linesep)

         enable_radio(f)
         write_end_expect(f)

   if x == 7:
      with open(result_file, 'w') as f:
         write_start_expect(f)
         disable_radio(f)
         enable_gradio(f)

         f.write('send_user "\[\+\] Adding Radio g...\\n"'+ os.linesep)

         for s in radio_exb_list:
            f.write('send "'+ s.attributes['name'].value+'\\r"'+ os.linesep)

         enable_radio(f)
         write_end_expect(f)
