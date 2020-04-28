#!/bin/bash
# Author: jyoti.bhano30t@gmail.com
# Description: Provides access to the user on NAT servers for one hour


# e - exits at any error
# u - consider an unset variable an error
# x - prints out each line as it is run
#set -eu #x
set -u

# Run as roothttps://github.com/jyotibhanot30/scripts
if [ "$UID" -ne 0 ]
then
  echo "Must be root to run this script."
  exit 1
fi

username=${1:?Username argument expected.}
password="$(openssl rand -base64 10)"
sha512pw="$(openssl passwd -1 -salt foobar "$password")"

# Check if user already exists.
if getent passwd "${username%@*}"  >/dev/null
        then
            echo "User $username does already exist."
            echo "please choose another username."
            exit 1
fi
useradd -p "${sha512pw}" "${username%@*}" &&
    echo "userdel -r ${username%@*}" | at now + 1 hour

echo "Linux user created."
echo "Username:   ${username%@*}"
echo "Password:   $password"
