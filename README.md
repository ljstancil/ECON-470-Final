# ECON 470 Final
## Introduction

## Market
### **Banks**
#### *Attributes*
#### **Location**
Each bank is assumed to have an office in $l_1, l_2, l_3$, however it is randomly decided how many/which of the remaining locations they operate in.
#### **Timeline**
Each bank offers their interns at the same time, however banks will offer at different times. In this instance, we have two types: early and late (t=0, t=1). It will be randomly decided at the beginning the types of each bank. This is privately held information.
#### **Sectors**
We can assign sectors to locations instead of banks. This way, if a bank occupies a location, then it has the sectors associated with that sector. The quotas will be randomly generated from 3-10.
#### **Prestige**
Prestige is influenced by others' beliefs about the bank. As such, we will generate a random number between 0 and 1 to serve as the mean for a truncated normal distribution from 0 to 1. This will allow us to simulate the idea that interns will have different ideas regarding the prestige of the banks, but the averages will be the same across interns.
#### **Advancement**
Beliefs about advancement opportunities will likely be generated from their prior interactions with the firm, not necessarily from publicly available information.

#### **Salary**
Prior to the start of the game/matching, each bank independently chooses a salary that they will offer to each of their interns. This is a customary practice. The salary is determined randomly between a range and then ranked accordingly.

### Firm Beliefs and Preferences
#### Resume
The firm's belief regarding the academic aptitude 

### **Interns**
#### *Independently Determined*
#### **Location**
An intern will form a set of locations where they would most want to work. It will be between 3-6, randomly. This is assumed to be known by the firms.
#### **Salary**
Salary rankings are determined by the firms. 
#### **Sectors**
Sector preferences are randomly generated. 
Anywhere from 3-6. This is assumed to be known by the firms.
#### *Firm-Dependent*
#### **Prestige**
Randomly determined for each firm. (no other factors except randomness at this time). Known only to the intern.
#### **Advancement Opportunities**
Randomly determined for each firm. (no other factors except randomness at this time)

## Matching/Assignment Process
### At $t=0$
1. Firms are assigned their locations and corresponding sectors. The quota for each sector is randomly generated $q \in \{ 3, \dots, 10 \}$.The salary for each firm is sampled from a truncated normal distribution in the range $[0,1]$. The firm's average prestige is sampled from the truncated normal distribution in the range $[0,1]$. The firm generates their "company culture" metric by sampling three integers from the uniform distribution on $[0,1000]$ and norming the numbers to sum to 1. Finally, the firm generates a utility function by sampling three integers from the uniform distribution on $[0,1000]$ and norming the numbers to sum to 1. These numbers represent the coefficient the firm assigns to an intern's "academics", "firm fit", and "interview performance".
2. Agents randomly sample an integer over the range $[0,6]$. This is the number of locations that the agent will find acceptable. The agent then randomly samples that number of locations from the list of all locations. Unlike the firms, the only requirement for locations preferences is that they must find at least one location acceptable. The intern then randomly reorders the sector list to determine their preferences over each sector. The agent then generates their beliefs regarding the firm. The agent's belief regarding the prestige of the firm is generated by sampling a truncated normal distribution over $[0,1]$ with $\mu = \rho_k$ where $\rho_k$ is the mean prestige for the firm $\pi_k$. The agent's belief regarding advancement at the firm is sampled from the truncated normal distribution over $[0,1]$ 
3. Banks then generate preferences over the set of interns. This will be randomly generated (not uniform, we want them to not be necessarily independent)

### **Process (Without Clearinghouse)**
#### Assumptions
- Firms can only make one offer for each intern. 
- Firms know an intern's rankings for sector and location, but do not know the intern's respective utility function (i.e. whether an intern values location or sector more).
    - We can assume that when a firm makes an offer, they choose the agent's most preferred location left and then select the most preferred sector remaining.
- Firms are location and sector-indfifferent.
- Agents accept their most valued offer at time t (which will be the first time they are offered)
    - This can be changed to a more realistic timeline, but I think it's easiest this way
    - we can think of this as multiple rounds of serial dictatorship consisting of the firms that offer at that time period.

#### At time $t$
