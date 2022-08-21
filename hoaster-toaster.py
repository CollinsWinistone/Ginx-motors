#!/usr/bin/env python3

import argparse
import os

HOSTS_PATH_TO_FILE="/etc/hosts"

parser = argparse.ArgumentParser(description="hsing args", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

group = parser.add_mutually_exclusive_group()
group.add_argument("-i", action="store_true", help="Append ips to /etc/hosts")
group.add_argument("-m", action="store_true", help="Modify ips to /etc/hosts")
parser.add_argument("file", help="Target file")

config = vars(parser.parse_args())
# print(config)


def readFile(file):
    '''
        Reads the file
    '''
    with open(file, "r") as f:
        contents = {}
        for line in f.readlines():
            if line[0] != "#" and line[0] != "\n":
                splitted = line.split()
                contents[splitted.pop(0)] = splitted

    return contents

def main():
    current_HOSTS_PATH_TO_FILE = readFile(HOSTS_PATH_TO_FILE)
    target_HOSTS_PATH_TO_FILE = readFile(config["file"])

    # Check if no option was given
    if not config["i"] and not config["m"]:
        # Create backup of /etc/hosts to /etc/hosts.bak to be safe
        os.system(f"cp {HOSTS_PATH_TO_FILE} {HOSTS_PATH_TO_FILE}.bak")
        # Remove old /etc/hosts
        os.system(f"rm {HOSTS_PATH_TO_FILE}")
        # Copy target file to /etc/hosts
        os.system(f"cp {config['file']} {HOSTS_PATH_TO_FILE}")
    # Check if -m was given as an option
    elif config["m"]:
        for ip, host in target_HOSTS_PATH_TO_FILE.items():
            # Check if ip in provided file exists in /etc/hosts
            if ip in current_HOSTS_PATH_TO_FILE.keys():
                # If it does then add the hostnames to the existing ip in /etc/hosts
                current_HOSTS_PATH_TO_FILE[ip] += host
            else:
                # Else add the ip and corresponding hostnames to /etc/hosts
                current_HOSTS_PATH_TO_FILE[ip] = host
    # Check if -i was given as an option
    elif config["i"]:
        for ip, host in target_HOSTS_PATH_TO_FILE.items():
            # Add or replace ip and corresponding hostnames from provided file to /etc/hosts
            current_HOSTS_PATH_TO_FILE[ip] = host

    
    with open(HOSTS_PATH_TO_FILE, "w") as f:
        for k, v in current_HOSTS_PATH_TO_FILE.items():
            # Create the string the will be written to the file
            line = k + " " + " ".join(v)
            # Write the string
            f.write(line)
            # Write a newline character
            f.write("\n")

    print("Contents of ==== /etc/hosts")
    print("----------")
    os.system("cat /etc/hosts") 

if __name__ == '__main__':
    main() 
