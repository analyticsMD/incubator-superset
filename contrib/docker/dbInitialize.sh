#!/bin/bash

sleep 5
mysql -u $MYSQL_USER -p $MYSQL_ROOT_PASSWORD << eof
alter table slice_user_version modify column id int(11) AUTO_INCREMENT
eof
