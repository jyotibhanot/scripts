#!/bin/bash
#Author: Jyoti Bhanot <jyoti.bhanot30@gmail.com>
#This script ubdivide a given CIDR /24 and smaller subnets into a pre-defined number of smaller subnets.
#After division IP addresses shouldn't be wasted, i.e. accumulation of your subdivisions should make up the divided subnet.
#Every subnet has 3 IP addresses reserved and not usable by hosts: network, broadcast, gateway.
#Show network/broadcast address, number of hosts and assign gateway. Gateway should be first IP available in divided subnet. Examples:
#INPUT: ./subnetter.sh 192.168.0.0/24 3
#OUTPUT:
#subnet=192.168.0.0/25 network=192.168.0.0 broadcast=192.168.0.127 gateway=192.168.0.1 hosts=125
#subnet=192.168.0.128/26 network=192.168.0.128 broadcast=192.168.0.191 gateway=192.168.0.129 hosts=61
#subnet=192.168.0.192/26 network=192.168.0.192 broadcast=192.168.0.255 gateway=192.168.0.193 hosts=61


display_usage() { 
  echo "Usage: ./subnetter.sh <CIDR> <SUBNET_COUNT>" 
} 

if [ $# -ne 2 ] 
then 
  display_usage
  exit 1
fi
 
cidr=$1
total_subnets=$2
nw_addr=`echo $cidr | awk -F'/' '{ print $1 }'` # retrieving network IP from input 1
nw_mask=`echo $cidr | awk -F'/' '{ print $2 }'` # retrieving network mask from input 1
last_octet=`echo $nw_addr | awk -F'.' '{ print $4 }'` # retrieving the D-bit from network ( A.B.C.D )
first_three_octets=`echo $nw_addr | awk -F'.' 'BEGIN {OFS = ""}{print $1,".",$2,".",$3 }'` # retrieving A.B.C bits from n/w address

change_bit=$(( 32 - $nw_mask)) 
total_addrs=$(( 2 ** $change_bit)) # calculating total addresses available in the network that can be subdivided
first_dbit=$last_octet  # value of first dbit

# A function to calculate the least power of 2 that is equal or greater than the argument
least_greater_power_of_two()
{
power_to_two=2
power=1
avail_addrs=$1
while [ $power_to_two -lt $avail_addrs ]; do
 power=$(($power+1))
 power_to_two=$(( 2 ** $power))
done
}

#initializing loop variables
remaining_addrs=$total_addrs # remaining addresses to be divided among remaining subnets
subnet_last_dbit=$last_octet # last dbit of current division
total_subnet_addr=0
starting_dbit=$last_octet
i=$total_subnets


while [ $i -gt 0 ]; do
  starting_dbit=$(( $starting_dbit + $total_subnet_addr )) #Finding the starting D bit of the subnet

  #finding the total number of addresses in the subnet 
  avail_addrs=$(( $remaining_addrs /  $i )) 
  least_greater_power_of_two $avail_addrs
  total_subnet_addr=$power_to_two
  
  subnet_last_dbit=$(( $subnet_last_dbit + $total_subnet_addr )) #Finding the ending D bit of the subnet
  remaining_addrs=$(( $remaining_addrs - $total_subnet_addr ))  # Remaining addresses left to be assigned to the other subnets

  last_dbit=$(( $subnet_last_dbit - 1)) #calculating last D bit in the subnet range
  subnet_mask=$(( $change_bit - $power + $nw_mask )) #calculating the subnet mask
  gateway_dbit=$(( $starting_dbit + 1 )) # calculating the Gateway D bit
  total_hosts=$(( $total_subnet_addr - 3 )) # calculating the Total-hosts in the network
  echo "subnet=$first_three_octets.$starting_dbit/$subnet_mask network=$first_three_octets.$starting_dbit broadcast=$first_three_octets.$last_dbit gateway=$first_three_octets.$gateway_dbit hosts=$total_hosts"
  i=$(($i-1)) # updating loop variable

done
