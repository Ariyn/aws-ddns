#! /usr/bin/python3
import os, json, subprocess
import argparse
import pprint

datas = json.loads(open("datas", "r").read())
credientials = json.loads(open("datas-credientials", "r").read())
instanceInfo = json.loads(open("datas-instanceInfo", "r").read())


hostedZone = datas["hostedZone"]
jsonFilePath = datas["jsonFilePath"]

tmpJsonPath = "/tmp/route53.json"
jsonFileData = open(jsonFilePath, "r").read()

result = subprocess.check_output("%s aws ec2 describe-instances --instance-ids %s --region %s" % (credientials["instance"], instanceInfo["id"], instanceInfo["region"]), shell=True)
result = json.loads(result.decode("utf-8"))

instance = result["Reservations"][0]["Instances"][0]
publicIp = instance["PublicIpAddress"]
open(tmpJsonPath, "w").write(jsonFileData%publicIp)


result = subprocess.check_output("%s aws route53 change-resource-record-sets --hosted-zone-id %s --change-batch file://%s" % (credientials["route53"], hostedZone, tmpJsonPath), shell=True)
result = json.loads(result.decode("utf-8"))
pp = pprint.PrettyPrinter()
pp.pprint(result)