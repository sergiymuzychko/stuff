#Enumerate security groups in the given regions; 
#search for SGs and rules opening any port except 22 for the unrestricted public access;
#replac such rules with the same kind opened to KBP1 office IPs instead of 0.0.0.0/0
import boto.ec2
import sys
aws_regions = ["us-east-1", "eu-west-1"]
anywhere = "[0.0.0.0/0]"
KBP1=str("X.X.X.X/XX")
SSH = str("22")

for region in aws_regions:
	print (region)
	conn = boto.ec2.connect_to_region(region,aws_access_key_id='',aws_secret_access_key='')
	sg_list  = []
	sg_list = conn.get_all_security_groups()
    for sg in sg_list:
		for rule in sg.rules :
			ip_access = str(rule.grants)
			startport = str(rule.from_port)
			endport = str(rule.to_port)
			protocol = str(rule.ip_protocol)
			if ip_access == anywhere and startport != SSH :
				try:
					sg.authorize(ip_protocol=protocol, from_port=startport, to_port=endport, cidr_ip=KBP1, dry_run=False)
					print("Creating replacement rule")
				except:
					print("Can not create replacement rule")
					sys.exc_info()
					sys.exit(0)
				sg.revoke(protocol, startport, endport, cidr_ip="0.0.0.0/0")
				print("unsecure rule deleted")
