# python-vsphere-rest-api
A method that makes use of the pyvmomi library to get the cpu, memory, and disk usage of an ESX host and a Flask REST api for getting that information as JSON. Great for versions of vshere that do not support REST (eg 6.0.0).

# How to use
Run `vsphere_api_rest.py` like so
```
python vsphere_api_rest.py username password ip
```

Where `username` and `password` are the credentials to log into your vsphere and `ip` is the ip-address that the program will listen on (usually the same address as the host machine)

## Making the rest call
Perform a `GET` request to the uri `<rest-server-ip-or-dns>:<port>/vm?host=<host>&name=<vm-name>` where `host` is the ip-address of the vsphere machine hosting the VM in question and `vm-name` is the name of VM exactly as it is called on the host. The server will return a JSON document that contains cpu and memory usage as a percentage (divide by 100) and disk space as a percentage (no divide). 
Eg 'mem':'266' -> using 2.66% of memory, 'disk': '58' -> using 58% of disk

An example of a GET request:
```
151.155.216.36:5000/vm?host=151.155.216.208&name=eDir-st8123
```

Example of JSON response:
```
{
    "mem": "4299",
    "disk": "55",
    "name": "eDir-st8123",
    "cpu": "4366"
}
```
