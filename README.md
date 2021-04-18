# simpy_simu
a past learning simpy's example
About 3 years ago. An accident chance,I came through simpy(a simulation framework).And at that time,I wrote a test to testify simpy's function.
Today,I recited the script and run in Pycharm.It works!So I put it into github.

一、Introduction of simpy
    SimPy is a process-based discrete-event simulation framework based on standard Python.
Processes in SimPy are defined by Python generator functions and may, for example, be used to model active components like customers, vehicles or agents. SimPy also provides various types of shared resources to model limited capacity congestion points (like servers, checkout counters and tunnels).
The behavior of active components (like vehicles, customers or messages) is modeled with processes. All processes live in an environment. They interact with the environment and with each other via events.
    Processes are described by simple Python generators. You can call them process function or process method, depending on whether it is a normal function or method of a class. During their lifetime, they create events and yield them in order to wait for them to be triggered.
When a process yields an event, the process gets suspended. SimPy resumes the process, when the event occurs (we say that the event is triggered). Multiple processes can wait for the same event. SimPy resumes them in the same order in which they yielded that event.
    For much more information, please visit https://simpy.readthedocs.io/en/latest/.
the information above is copied from simpy official website.

二、


