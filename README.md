# Lizmon

This is a metrics gathering tool which performs summarization on a
by-minute for the last hour and then on a by-hour for the last day
basis.

# Requirements

* Python3
* Pyvenv
* nose==1.3.7
* psutil==4.2.0
* tornado==4.3

# Setup and installation

```
# create a python virtual environment
pyvenv ./env

# activate the environment for the current shell
. env/bin/activate

# install the requirements for this project
pip install -r requirements.txt
```

# Testing

## Report performance data

```
python bin/liz-monitor --this-host jarvis --publish http://localhost:8080/api/perf
```

## Get performance reporting data

```
while true ; do curl -s http://localhost:8080/api/perf/$(hostname)/by-minute:cpu | python -m json.tool; sleep 2; clear; done;
```

## Peg the system

Do this in one or more panes in your terminal on a Mac OS 10+ host.  Note, the instructions on [this page](http://osxdaily.com/2012/10/02/stress-test-mac-cpu/) advise you to background the stree test command.  I do not agree.  You probably want the ability to cancel/stop your stress test.  Sure, you can use killall, but its much easier to Ctrl+C each one, sending it an INT signal.

```
yes > /dev/null
```
