# Document to generate a pure gauge configuration

Suppose we have the input file "ini.xml", in which we named the configuration as "pure_gauge", and we set the output file as "out.xml" then we will get the following files:

* out.xml
* pure_gauge.lime1
* pure_gauge.ini.xml


## XML input

For now, 16^4 is the possible volumn on this machine.


The index to start with
```
    <StartUpdateNum>0</StartUpdateNum>
```
How many times to update in the warm up stage
```
    <NWarmUpUpdates>10</NWarmUpUpdates>  
```
How many times to update in the production stage (upper limit)
```
    <NProductionUpdates>1000</NProductionUpdates>
```
How many times to update in this run, should be less than the production stage
```
    <NUpdatesThisRun>50</NUpdatesThisRun>
```
The interval to save the configuration
```
    <SaveInterval>50</SaveInterval>
```


## XML output

measurement results will be stored here. 


## Configuration file

The configuration file will be generated in the current directory, named with ".lime1" extension.

The "cfg_type" of the configuration will be in the 