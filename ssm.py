import boto3


def getPasswords():
  ssm = boto3.client('ssm')
  passwrd = ssm.get_parameter(Name='/prod/nyp/snowflake-db/stack-user-pasword', WithDecryption=True)
  nyp_superset = passwrd['Parameter']['Value']
  return nyp_superset

def ssm_password_lookup(url):
  return getPasswords()
