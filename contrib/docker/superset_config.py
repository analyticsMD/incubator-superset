# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
import os
import boto3
from celery.schedules import crontab


def get_env_variable(var_name, default=None):
    """Get the environment variable or raise exception."""
    try:
        return os.environ[var_name]
    except KeyError:
        if default is not None:
            return default
        else:
            error_msg = 'The environment variable {} was missing, abort...'\
                        .format(var_name)
            raise EnvironmentError(error_msg)

def getSecretKey():
    ssm = boto3.client('ssm')
    key = ssm.get_parameter(Name='/devops/superset/secret_key', WithDecryption=True)
    secret_key = key['Parameter']['Value']
    return secret_key

def getMapBoxKey():
    ssm = boto3.client('ssm')
    key = ssm.get_parameter(Name='/devops/superset/map_key', WithDecryption=True)
    map_key = key['Parameter']['Value']
    return map_key

MYSQL_USER = get_env_variable('MYSQL_USER')
MYSQL_PASSWORD = get_env_variable('MYSQL_PASSWORD')
MYSQL_HOST = get_env_variable('MYSQL_HOST')
MYSQL_PORT = get_env_variable('MYSQL_PORT')
MYSQL_DB = get_env_variable('MYSQL_DB')

# The SQLAlchemy connection string.
SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s:%s/%s?autocommit=1' % (MYSQL_USER,
                                                           MYSQL_PASSWORD,
                                                           MYSQL_HOST,
                                                           MYSQL_PORT,
                                                           MYSQL_DB)

REDIS_HOST = get_env_variable('REDIS_HOST')
REDIS_PORT = get_env_variable('REDIS_PORT')


class CeleryConfig(object):
    BROKER_URL = 'redis://%s:%s/0' % (REDIS_HOST, REDIS_PORT)
    CELERY_IMPORTS = (
        'superset.sql_lab',
        'superset.tasks',
    )
    CELERY_RESULT_BACKEND = 'redis://%s:%s/1' % (REDIS_HOST, REDIS_PORT)
    CELERYD_LOG_LEVEL = 'DEBUG'
    CELERYD_PREFETCH_MULTIPLIER = 10
    CELERY_ACKS_LATE = True
    CELERY_ANNOTATIONS = {
        'sql_lab.get_sql_results': {
            'rate_limit': '100/s',
        },
        'email_reports.send': {
            'rate_limit': '1/s',
            'time_limit': 120,
            'soft_time_limit': 150,
            'ignore_result': True,
        },
    }
    CELERYBEAT_SCHEDULE = {
        'email_reports.schedule_hourly': {
            'task': 'email_reports.schedule_hourly',
            'schedule': crontab(minute=1, hour='*'),
        },
    }


CELERY_CONFIG = CeleryConfig

#CACHE_CONFIG = {
#    'CACHE_TYPE': 'redis',
#    'CACHE_DEFAULT_TIMEOUT': 60 * 60 * 24, # 1 day default (in secs)
#    'CACHE_KEY_PREFIX': 'superset_results',
#    'CACHE_REDIS_URL': 'redis://%s:%s/0' % (REDIS_HOST, REDIS_PORT),
#}

from werkzeug.contrib.cache import RedisCache
RESULTS_BACKEND = RedisCache(
    host=REDIS_HOST, port=REDIS_PORT, key_prefix='superset_results')

WEBDRIVER_BASEURL = 'https://0.0.0.0:8088/'
# Enable / disable scheduled email reports
ENABLE_SCHEDULED_EMAIL_REPORTS = True

# If enabled, certail features are run in debug mode
# Current list:
# * Emails are sent using dry-run mode (logging only)
SCHEDULED_EMAIL_DEBUG_MODE = False

# Email reports - minimum time resolution (in minutes) for the crontab
EMAIL_REPORTS_CRON_RESOLUTION = 15

# Email report configuration
# From address in emails
EMAIL_REPORT_FROM_ADDRESS = 'noreply@qventus.com'

# Send bcc of all reports to this address. Set to None to disable.
# This is useful for maintaining an audit trail of all email deliveries.
EMAIL_REPORT_BCC_ADDRESS = None

# User credentials to use for generating reports
# This user should have permissions to browse all the dashboards and
# slices.
# TODO: In the future, login as the owner of the item to generate reports
EMAIL_REPORTS_USER = 'admin'
EMAIL_REPORTS_SUBJECT_PREFIX = '[Report] '

# The webdriver to use for generating reports. Use one of the following
# firefox
#   Requires: geckodriver and firefox installations
#   Limitations: can be buggy at times
# chrome:
#   Requires: headless chrome
#   Limitations: unable to generate screenshots of elements
EMAIL_REPORTS_WEBDRIVER = 'firefox'
# smtp server configuration
EMAIL_NOTIFICATIONS = True # all the emails are sent using dryrun
SMTP_HOST = 'smtp.sendgrid.net'
SMTP_STARTTLS = False
SMTP_SSL = True
SMTP_USER = 'analyticsmd'
SMTP_PORT = 465 #465 , 587
SMTP_PASSWORD = 'D0ndeMail'
SMTP_MAIL_FROM = 'superset@superset.com'
SECRET_KEY = getSecretKey()
ROW_LIMIT = 100
SQL_MAX_ROW = 500
VIZ_ROW_LIMIT = 500
# max rows retrieved by filter select auto complete
FILTER_SELECT_ROW_LIMIT = 1000
# Maximum number of rows returned from a database
# in async mode, no more than SQL_MAX_ROW will be returned and stored
# in the results backend. This also becomes the limit when exporting CSVs
SQL_MAX_ROW = 10000

# Default row limit for SQL Lab queries
DEFAULT_SQLLAB_LIMIT = 100

DISPLAY_MAX_ROW = 500
SUPERSET_WORKERS = 4

# Timeout duration for SQL Lab synchronous queries
SQLLAB_TIMEOUT = 600

# The MAX duration (in seconds) a query can run for before being killed
# by celery.
SQLLAB_ASYNC_TIME_LIMIT_SEC = 60 * 60

SUPERSET_WEBSERVER_TIMEOUT = 1200

SUPERSET_WEBSERVER_PORT = 8088
# Flask-WTF flag for CSRF
WTF_CSRF_ENABLED = True
# Add endpoints that need to be exempt from CSRF protection
WTF_CSRF_EXEMPT_LIST = []
# A CSRF token that expires in 1 year
WTF_CSRF_TIME_LIMIT = 60 * 60 * 24 * 365
# Set this API key to enable Mapbox visualizations
MAPBOX_API_KEY = getMapBoxKey()