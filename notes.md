Programming Challenge
=====================

ServerTrack
-----------

Take 2-4 hours to complete the exercise. When you are
done feel free to push your code to a personal Github
Repository, or send me a zip file with your work. You
can use any programming language/framework. Since I
might not be familiar with your particular technology
choice, please include instructions on how to run the
program.

There is no one right answer to this problem and we
are specifically looking at how you might shape an API,
how you handle concurrency, memory, ambiguity etc.

Expectations
------------

- Compiles and runs

- Has a simple, maintainable design that meets the functional
  specification (no need to cram in any unnecessary technologies)

- Can be proven to implement the specification correctly

- Is written with the performance characteristics listed below
  in mind

Please approach this as if it was a real project that you will
be deploying to production. I’m looking to get an insight into
your critical thinking process as well as what your bar is for
quality code. This specific challenge is called ServerTrack and
allows you to demonstrate how you might implement a basic server
monitoring system.

1.  Two web API endpoints are necessary. They are:

2.  Record load for a given server.  This should take a:

  - server name (string)
  - CPU load    (double)
  - RAM load    (double)

And apply the values to an in-memory model used to provide the
data in endpoint #2.

2. Display loads for a given server.  This should return data
   (if it has any) for the given server:

  - A list of the average load values for the
    last 60 minutes broken down by minute

  - A list of the average load values for the
    last 24 hours broken down by hour

    Assume these endpoints will be under a continuous
    load being called for thousands of individual
    servers every minute.

There is no need to persist the results to any permanent
storage, just keep the data in memory to keep things simple.

1.  agent for monitoring each node
      - uses psutil to gather cpu data from the localhost
          `psutil.cpu_percent(interval=None)`
      - use pickle + gzip library to serialize and compress the data
        for transmission.
      - transmits the cpu, ram, ipaddress via zeromq pub/sub as
        the connected publisher.

    data_point = {
      fqdn: node01.corp.internal
      ts: epoch # double
      ip: [ipaddress1, ipaddress2], # strings
      cpu: float
      ram: float,
    }

2.  load reciever service that recieves performance data from each node
      - setup reciever on the monitoring host
      - make a single call each second to load aggregator to give new data of updates from nodes
      - estimating that recieving doesn't need multithreading since its cpu-bound and most cpus
        are pretty fast.  the io for input here is super fast, from experience.
      - this service should store its data in a time-series db.  I don't know which one, but I think
        redis would be a good solution since it supports TTL and it has a list construct

    # Use sorted dict for the timestamp fields
    stats[node]['raw'][timestamp][data]

2.  load aggregator service that aggregates the load values for configured time slices

    for each node:
      for each metric in the last hour:
        track a sum and a count of metrics where the raw data point is within the last 60mins
      compute the average for this node and store it in the last hour
      for each hour

    stats[node]['last-hour'][hour_start_epoch] = {
      cpu: float,
      ram: float,
    }
