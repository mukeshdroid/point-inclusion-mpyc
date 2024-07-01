# Implementation of Point Inclusion Problem using MPyC.

Author: Mukesh Tiwari
Supervisor: Dr. Gokul KC

This work was done as the part of final year thesis in BSc. Computational Mathematics at Department of Mathematics, Kathmandu University. 
---

### Instructions to run:

  1. Install MPyC by following the instructions at its official repo : https://github.com/lschoe/mpyc
  2. Navigate to the folder and run the following command based on your role
 
#### To run on locally: 
```
#In terminal 0 (trusted user)
python3 millionaire-problem.py -M2 -I0
```

```
#In terminal 1 (Alice or party with point)
python3 millionaire-problem.py -M2 -I0
```

```
#In terminal 2 (Bob or party with polygon)
python3 millionaire-problem.py -M2 -I0
```

### To run on differnet computers:

```
#In terminal 0 (trusted user)
python3 millionaire-problem.py -P localhost -P <IP:PORT of device 1> -P <IP:PORT of device 2> -I0
```

```
#In terminal 1 (Alice or party with point)
python3 millionaire-problem.py -P <IP:PORT of device 0> -P localhost -P <IP:PORT of device 2> -I0
```

```
#In terminal 2 (Bob or party with polygon)
python3 millionaire-problem.py -P <IP:PORT of device 0>  -P <IP:PORT of device 1> -P localhost -I0
```


