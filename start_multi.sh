#!bin/sh
current_path="$(pwd)"
cd "$current_path"
rm -rf nohup.out
source env/bin/activate

while true
do
	if ! lsof -i:12340
	then
		nohup python master_multi.py "$@" &
		read -t 2
		nohup python racer.py &
		break
	else
		badPid=$(lsof -i:12340 -t)
		echo $badPid
		kill -9 $badPid
		echo 12340 is occupied
	fi	
done

