 
# Polarization Experiment Simulation

A multi-agent simulation of the polarization process, especially for small groups. 


## The structure


```main.py``` The script containing the initialization of one round of simulation, e.g. the agent positions, etc., assigning the parameters to a single run given the user settings, handling the output folder initialization, and calling the simulation. 


```sim_dyn.py``` The influence dynamics are implemented in this script. The functions will be called from ```main.py```


```sim_utilities.py``` Containing the polarization metrics. The functions will be called by the other scripts. 


## Output 

The default run of ```main.py``` will output a tab-separated log file under the ```log/current/``` folder with the name formats: ```1080_3747_T_res_{partyDiff, std}``` where


* ```1080``` is the pid-process indentifier number

* ```3747``` is a random number in ```(0, 10000)``` (this is to avoid output clash for multiprocessing) 

* ```{partyDiff, std}``` indicates the polarization metric outputed. 

When the experiment of ```exo-shock''' is run, the output is of format:

```
T  polarization polarization_shock
----------------------------------
0	0.3674382783	0.3792893849

```
where the first column is the time step, ```0``` is the first step,
the second column is the current polarization metric value, 
the last column is the polarization on the first dimension of ```Z```. This value is only meaningful after the shock started, which is recorded in the file ```1080_3747_T_res_shockRecord```.

The code records the polarization change at every ```100``` steps. But the user could edit the code to increase/decrease the recording interval. 


## Usages

The default run of ```main.py``` will output the single run result for $\alpha=.5$, $\beta=.5$, $\gamma=.5$, and $\sigma=.4$ ($\sigma<.32$ will not be meaningful for the current initialization).

For other parameter settings, please modify the ```params``` dictionary list at the top of the ```__main__``` function. 

If you want to run multiple experiments on a range of parameters, you could comment out the multiprocessing section below the ```params``` dictionary list in the ```__main__``` function within ```main.py``` and add your list of parameters in ```params```.  



## Dependencies

Currently in this vanilla version, no other third party package needs to be installed except for ```Numpy```. Here is the author's environment for a reference:

```
Python 3.7

numpy=1.18.1

```

