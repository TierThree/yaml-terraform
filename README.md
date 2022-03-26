# YAML TO HCL for VSPHERE
This code is designed to convert a YAML configuration into HCL.
Basic usage is as follows:
```
python3 main.py --yaml {{ some_file }}.yml
```
or
```
python3 main.py -y {{ some_file }}.yml
```

## TODO Items:
These are the items left to work on:
1. Allow for multiple disks and networks
2. Allow for shorthand of certain fields
3. Allow for customize options in the clone field
4. Allow for clone using count for multiple VMs
5. Possibly add a 'kind' to manage more than just VMs
6. Allow for vm creation without using a clone

## Example YAML
The below YAML excerpt will provide a foundation for building with this:
_NOTE: Read the TODO items first, some functionality is finnicky._

```
---
provider: 
  name: vsphere

metadata:
  name: {{ name of the vm }}
  folder: {{ full vcenter folder path to vm }}

spec:
  datacenter: {{ name of the datacenter }}
  cluster: {{ name of the cluster }}
  cpu: {{ cpus as just a number }}
  memory: {{ memory in MB as just a number }}

  network:
  - name: {{ some descriptive name, no spaces }}
    portgroup: {{ name of the portgroup }}

  disks:
  - name: {{ some descriptive name }}
    size: {{ size as just a number }}
    datastore: {{ name of the datastore }}

  clone:
    template: {{ name of the vm to clone }}
```