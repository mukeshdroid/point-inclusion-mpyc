# Implementation of Point Inclusion Problem using MPyC.

Author: Mukesh Tiwari

Supervisor: Dr. Gokul KC

> This work was done as the part of final year thesis in BSc. Computational Mathematics at Department of Mathematics, Kathmandu University. 
---

### Instructions to run:

  1. Install MPyC by following the instructions at its official repo : https://github.com/lschoe/mpyc
  2. Navigate to the folder and run the following command based on your role
 
#### To run on locally: 

- In terminal 0 (trusted user)
```
python3 millionaire-problem.py -M2 -I0
```

- In terminal 1 (Alice or party with point)
```
python3 millionaire-problem.py -M2 -I0
```

-In terminal 2 (Bob or party with polygon)
```
python3 millionaire-problem.py -M2 -I0
```

### To run on differnet computers:

- In terminal 0 (trusted user)
```
python3 millionaire-problem.py -P localhost -P <IP:PORT of device 1> -P <IP:PORT of device 2> -I0
```

- In terminal 1 (Alice or party with point)

```
python3 millionaire-problem.py -P <IP:PORT of device 0> -P localhost -P <IP:PORT of device 2> -I0
```

- In terminal 2 (Bob or party with polygon)
```
python3 millionaire-problem.py -P <IP:PORT of device 0>  -P <IP:PORT of device 1> -P localhost -I0
```

---

### Providing Inputs

Number of participants that can participate in this protocol must be greater than 2.
The following roles are predefined:
| Party   | Role  | Input |
| :---:   | :---: | :---: |
| 0 | Trusted Helper   | None   |
| 1 | Alice   | Point   |
| 2 | Bob   | Polygon   |

#### Providing Point
The point should be input in the file point.csv in the data directory. Only 2d points are acceptible.

#### Providing Polygon
The polygon should be placed in the file polygon.csv in the data directory. The polygon is assumed to have the following properties:
     * the first entry is leftmost point. 
     * the points are in cyclic order
     * the first m points belong to lower boundary

The third entry in each row of polygon.csv corrsponds to the edges and are labelled as follows:
     * 1 means edge is in lower boundary
     * -1 means edge is in the upper boundary
The edge is defined using the current point and the next one.


     
         

