#!/usr/bin/python
import re
from collections import Counter

# open file in read mode
def read_file(path):
  with open(path,'r') as f:
    output = f.readlines()
  f.close()
  return output

def main():
  path = './auth.log'
  ips = getips(path)
  uniq = list(set(ips))
  for ip in uniq:
    print ip
# Counter gives a list of tuples of the form [(ip,freq)]
# most_common function gives up the top elements from the output of the counter
# in the form of list of tuples of the form [(ip,freq)]
  highest_occuring = Counter(ips).most_common(1)[0][0]
  frequency = Counter(ips).most_common(1)[0][1]
  print "Highest Occuring: %s Frequency: %s" % (highest_occuring, frequency)
  print "Highest Occuring: " + highest_occuring + " Frequency: " + str(frequency)

#get the list of IP's in the log file
def getips(path):
  ips = []
  lines = read_file(path)
  for line in lines:
    ip_list=re.findall("[0-9]+(?:\.[0-9]+){3}", line)
    if len(ip_list) > 0:
       ips.extend(ip_list)
  return ips

if __name__ == '__main__':
  main()
  
