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

```
. env/bin/activate
nosetests
```

# Running

## The Liz Receiver

The receiver will both receive and summarize the reported data

### API endpoints

* `/api/perf/:host/:epoch` - Use this endpoint to `POST` data to the receiver.
* `/api/perf/:host/:label` - Use this endpoint to `GET` data from the
receiver.  The label parameter is optional, so if you don't provide
that it'll give you all the summarized data it has for the host.  If
you provide the label param, it will perform a case-insensitive
string-contains to determine if the summarized data should be returned.
An example of summarized data labels are: `summary:by-minute:mem` and
`summary:by-hour:cpu`.

### Run the Liz Receiver

```
. env/bin/activate
python bin/liz-receiver # defaults to port 8080
```
## Monitor your nodes

### Details that the Liz Monitor needs to be aware of

* What you call "this host".  This might be the hostname, or the
IP, asset id, or something else entirely.
* Where the receiver is that you would like to publish to.

### Run the Liz Monitor

```
. env/bin/activate
python bin/liz-monitor --this-host $(hostname) --publish http://localhost:8080/api/perf
```

Here's an example of what you'll see:

```
INFO:  Publish was successful to http://localhost:8080/api/perf/jarvis/1465001847
INFO:  Publish was successful to http://localhost:8080/api/perf/jarvis/1465001848
INFO:  Publish was successful to http://localhost:8080/api/perf/jarvis/1465001849
```

## Get performance reporting data

```
while true ; do curl -s http://localhost:8080/api/perf/$(hostname)/by-minute:cpu | python -m json.tool; sleep 2; clear; done;
```

Here's an example of what you'll see:

```
{
    "summary:by-minute:cpu": {
        "averages": [
            {
                "start-sec": 1465001760,
                "avg": 4.98,
                "interval-size-sec": 60,
                "end-sec": 1465001820,
                "num-samples": 5
            }
        ],
        "start": 1464998160,
        "end": 1465001814,
        "timeslice-size-sec": 60,
        "average-count": 1
    }
}
```

## Peg the system

Do this in one or more panes in your terminal on a Mac OS 10+ host.  Note, the instructions on [this page](http://osxdaily.com/2012/10/02/stress-test-mac-cpu/) advise you to background the stree test command.  I do not agree.  You probably want the ability to cancel/stop your stress test.  Sure, you can use killall, but its much easier to Ctrl+C each one, sending it an INT signal.

```
yes > /dev/null
```

# Scaling

* Use Redis, Elasticsearch (?), or Riak (?).
* Break receiver and summarization into two different services.
* Implement WSGI compliance and run behind Nginx
* Implement autoscaling group with terraform on AWS to build
this thing out.

# Further Testing

* Add web service tests to simulate a node reporting data to
ensure that the receiver is doing the right thing.
* Add unit tests for the Datastore class in the receiver.

# Features

* Improve logging across the two components.
* Change transport from HTTP => UDP + ZeroMQ, because metrics shouldn't have that much overhead.
* Dockerize all the things.
* Implement trust via certificate chains so that only trusted
sources can request and use token-based authorization which can
then be used to submit metrics.
