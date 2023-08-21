#!/bin/sh 
# check to insure the entry does not already exist 
exists=0
crontab -l | grep "python3 /home/${USER}/pyscada-lite/pyscada-lite-back/manage.py get_all_variables_devices"  && exists=1 || exists=0
if [ $exists -eq 1 ]
then
echo "cronjob exist"
exit;
fi
# copy the contents of the current crontab to a temporary file 
crontab -l >/tmp/crontab.tmp 
# add the new entry to the end of the temporary file 
echo "* * * * * python3 /home/${USER}/pyscada-lite/pyscada-lite-back/manage.py get_all_variables_devices" >> /tmp/crontab.tmp 
#update crontab with the contents of the temporary file 
crontab /tmp/crontab.tmp 
# delete the temporary file 
rm /tmp/crontab.tmp 
