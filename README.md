# A simpy simulator
Several  years ago. I came through simpy(a simulation framework).And at that time,I wrote a test to testify simpy's function.Today, by accidence I looked at the script and run in Pycharm.It works!
So I put it into github.Of course ,it is just a simulation.
## Introduction of Simpy
SimPy is a process-based discrete-event simulation framework based on standard Python.  

Processes in SimPy are defined by Python generator functions and may, for example, be used to model active components like customers, vehicles or agents. SimPy also provides various types of shared resources to model limited capacity congestion points (like servers, checkout counters and tunnels).
The behavior of active components (like vehicles, customers or messages) is modeled with processes. All processes live in an environment. They interact with the environment and with each other via events.  

Processes are described by simple Python generators. You can call them process function or process method, depending on whether it is a normal function or method of a class. During their lifetime, they create events and yield them in order to wait for them to be triggered.  
When a process yields an event, the process gets suspended. SimPy resumes the process, when the event occurs (we say that the event is triggered). Multiple processes can wait for the same event. SimPy resumes them in the same order in which they yielded that event.  

For much more information, please visit https://simpy.readthedocs.io/en/latest/.  

## Using simpy to simulate the production flow of toyoto
The following diagram is got from websit:  
https://journalofbusiness.org/index.php/GJMBR/article/download/1983/1885/.  
Attention please:Simulation is just simply simulating the base flow of the whole process.

### Input
Machinery（Container）：it means the main body of the toyota vehicle. It has a storage（Container）  
Components（Container）：main components to build a car. It has a storage(Container), too.  
### Activities
Assembly（Container）：it gets the Machinery and components from two containers and save in assembly container.   
Parts sequencing（process）：took several days (not hours) to make the Components to the right place.  
Setting up schedule（Process）：took several to build the scheduled plan.  
Production commence（Process）：begin to product vehicle.  
### Output
Quality check（process）：check quality of body and Components.  
Vehicle assembling(Process)：assemble the body and components.  
Dispatch zone(container)：store the vehicle which has been made.  
### Closure
Dispatch to dealer(process)：transport to the dealer.  
In order to get the instant information, we add a process which can monitor the whole process status.  
Process_monitor(process)：a process which monitor the whole flow.  

## Source code
Refer to the main.py  
## code architecture
Toyoto_Factory: The class for the wehicle.it has following attibutes and functions  
machinery:a container for storing machinery.  
machinery_control:process for machinery controlling.  
components:a container for storing components.  
components_control:process for components controlling.  
assembler:container for storing assembler.  
assembler_control:process for assembler controlling.  
dispatch:a container for storing production vehicles.  
dispatch_control:process for dispatch controlling.  
env_status_monitor:monitoring all the Toyoto_Factory.  
