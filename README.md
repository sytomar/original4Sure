# original4Sure

Project Setup
This will be the README for your project. For now, follow these instructions to get this project template set up correctly. Then, come back and replace the contents of this README with contents specific to your project.

Requirements:
	Python 2.7

Instructions:
1) Install python:
sudo apt install python2.7

2) Install pip for dependecy management:
sudo apt install python-pip

3) Install virtualenv for virtual box of python:
pip install virtualenv

4) Clone the template project, replacing my-project with the name of the project you are creating:
git clone https://github.com/sytomar/original4Sure.git /path/to/directory
cd /path/to/directory/
sudo chmod -R 0777 /path/to/directory/original4Sure

5) Create a virtual environment:
virtualenv /path/to/directory/env

6) Activate virtual environment that was setup in the previous step
source /path/to/directory/original4Sure/env/bin/activate

7) Install the project's development and runtime requirements:
cd /path/to/directory/original4Sure
pip install -r requirements.txt
	or
pip install numpy

8) Make a localhost entry in host file:
  sudo nano /etc/hosts, add host entry as: 127.0.0.1 localhost

Project setup is now complete!

Files involved:
-> helper.py
-> master_multi.py
-> racer.py
-> start_multi.sh
In this case there are master listening on 127.0.0.1:12340 which is listening all the request from the racers process and revert it accordingly.
Excecution:
In CLI:
cd /path/to/directory/original4Sure
sh start_multi.sh n (n is greater than 1 and it should be positive integer only which is number of racer).

This will excecute the all the three processes in the background and get exit. After all the 10 laps output will be stored in "/path/to/directory/original4Sure/multi_racer.csv"(It will overwrite after every fresh excecution) in comma seprated way as per CSV standards in the format [LapNumber,Lap,LapStart,LapEnd,TimeToCompletion,AverageLatencyR1,AverageLatencyR2] and the all the sending and receiving logs between the process is maintained in "/path/to/directory/original4Sure/nohop.out"(It will overwrite after every fresh excecution)





