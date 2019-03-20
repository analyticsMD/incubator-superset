from qventus_conf import fetch_secrets

def ssm_password_lookup(url):
  environment = 'prod'
  stack = 'stanford'
  secret = '/amd-db/superset/password'
  secrets = [secret, ]
  fetch_secrets(environment, stack, secrets)
  return 'secret'