#!bin/sh
current_path="$(pwd)"
cd "$current_path"
rm -rf nohup.out
source env/bin/activate

while true
do
	if ! lsof -i:12341
	then
		nohup python racer1.py &

		read -t 2
		
		while true
		do
			if ! lsof -i:12342
			then
				nohup python racer2.py &
				read -t 2
				nohup python master.py &
				break
			else
				badPidTwo=$(lsof -i:12342 -t)
				kill -9 $badPidTwo
				echo 12342 is occupied
			fi	
		done
		break
	else
		badPidOne=$(lsof -i:12341 -t)
		kill -9 $badPidOne
		echo 12341 is occupied
	fi	
done


