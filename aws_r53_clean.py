import re
import boto
from boto import ec2
from boto.route53.record import ResourceRecordSets
from itertools import chain

ec2a = boto.ec2.connect_to_region('us-east-1',
                                  aws_access_key_id='',
                                  aws_secret_access_key='')
ec2b = boto.ec2.connect_to_region('eu-west-1',
                                  aws_access_key_id='',
                                  aws_secret_access_key='')
r53 = boto.connect_route53(aws_access_key_id='',
                           aws_secret_access_key='')
searchTemplate = ""
dnsZone = "Z39S22SCRHJER4"
publicIPs = []
dnsAvalues = []
recordIP = ""
# get DNS RRs and available ec2 instances
rrsets = r53.get_all_rrsets(dnsZone)
reservationsA = ec2a.get_all_instances()
reservationsB = ec2b.get_all_instances()
instancesA = [i for r in reservationsA for i in r.instances]
instancesB = [i for r in reservationsB for i in r.instances]
changes = ResourceRecordSets(r53, dnsZone)
# Write ec2 instance public IP to the list publicIPs, if present
for i in chain(instancesA, instancesB):
    if i.ip_address is not None:
        publicIPs.append(i.ip_address)


# Check if A records with name containing searchTemplate string are in existing IP addresses list
number = 0
for record in rrsets:
    if searchTemplate in record.name:
        recordIP = str(record).split(':')[3]
        recordIP = re.sub('>$', '', recordIP)
        recordHostname = str(record.name).split('.')[0]
        if recordIP not in publicIPs:
            number += 1
            print("Instance", recordHostname, "with IP ", recordIP, "does not exists, removing number", number)
            change = changes.add_change("DELETE", record.name, "A", ttl=record.ttl)
            print(change)
            change.add_value(recordIP)
changes.commit()


