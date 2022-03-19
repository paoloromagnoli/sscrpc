import sys, re, argparse
from typing import Dict
from sseapiclient import APIClient

# basic function to read input params
def read_param(argv):
    # https://docs.python.org/3/library/argparse.html#module-argparse
    # return a dict with {'env': 'environment_name', 'role': 'role_name', 'write': True/False, 'delete': True/False, ['folder': 'folder_name']}

    parser = argparse.ArgumentParser(description='Grants SaltStack provided Role with RBAC permission access for files in Saltstack backend, either to all files in the specififed environment or to files in the optionally specified folder. By default assignes both Read and Discover grants.')
    parser.add_argument('host', nargs=1,
                        help='the RaaS url on your SaltStack instance provides as http:s//<FQDN> or https://<IP_ADDRESS>')
    parser.add_argument('username', nargs=1,
                        help='the SaltStack username')
    parser.add_argument('password', nargs=1,
                        help='the SaltStack password')
    parser.add_argument('env', nargs=1,
                        help='the SaltStack environment to be granted access to')
    parser.add_argument('role', nargs=1,
                        help='the SaltStack role to be granted access')
    parser.add_argument('-w' "--write", action='store_true',
                        help='assignes write permission')
    parser.add_argument('-d' "--delete", action='store_true',
                        help='assignes delete permission')
    parser.add_argument('-f', '--folder', metavar='folder', nargs=1,
                        help='grant access only to files in the specified folder')
    parser.add_argument('-v' "--verbose", action='store_true',
                    help='print alls files that have been granted access to')
    args = vars(parser.parse_args())

    param = {}
    param["host"] = args["host"][0]
    param["username"] = args["username"][0]
    param["password"] = args["password"][0]
    param["env"] = args["env"][0]
    param["role"] = args["role"][0]
    param["write"] = args["w__write"]
    param["delete"] = args["d__delete"]
    param["verbose"] = args["v__verbose"]
    if args["folder"] is not None:
        param["folder"] = args["folder"][0]
    
    return param

# variables
response = None
access = {}
grants = {'read': True, 'discover': True}

parameters = read_param(sys.argv[1:])

#connection info
ssc_host = parameters["host"]
username = parameters["username"]
password = parameters["password"]

# permissions
grants["write"]=parameters["write"]
grants["delete"]=parameters["delete"]
access[parameters["role"]]=grants


print("The role {} will granted with the following permissions:".format(parameters["role"]))
print(grants)

print('Connectiing to RaaS ...')
client = APIClient(ssc_host, username, password, ssl_validate_cert=False)

if client is None:
    print('Connection to RaaS failed')
else:
    print ('Connected to RaaS')
    response = client.api.fs.get_env(saltenv=parameters["env"])

    fs_files = response[1]

    if "folder" in parameters:
        print("Restrict grant to folder: ",parameters["folder"])
        for fs_file in fs_files:
            if fs_file["path"].startswith("/"+parameters["folder"]+"/"):
                client.api.fs.save_file_access(file_uuid=fs_file["uuid"], access_payload=access)
                if parameters["verbose"] : print('Applying permissions to file: {}'.format(fs_file["path"]))
    else:
        for fs_file in fs_files:
            client.api.fs.save_file_access(file_uuid=fs_file["uuid"], access_payload=access)
            if parameters["verbose"] : print('Applying permissions to file: {}'.format(fs_file["path"]))

print('Done')