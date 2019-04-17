from qventus_conf import fetch_secrets

# TODO: modify function to take in sqla.engine.url. See https://superset.incubator.apache.org/installation.html#external-password-store-for-sqlalchemy-connections

def ssm_password_lookup(url):
  environment = 'prod'
  # TODO: generate stack and secret from sqla.engine.url
  stack = 'stanford'
  secret = '/amd-db/superset/password'
  secrets = [secret, ]
  fetch_secrets(environment, stack, secrets)
  return 'secret'