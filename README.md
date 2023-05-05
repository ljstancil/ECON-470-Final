
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.7/dist/katex.min.css" integrity="sha384-3UiQGuEI4TTMaFmGIZumfRPtfKQ3trwQE2JgosJxCnGmQpL/lJdjpcHkaaFwHlcI" crossorigin="anonymous">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.7/dist/katex.min.js" integrity="sha384-G0zcxDFp5LWZtDuRMnBkk3EphCK1lhEf4UEyEM693ka574TZGwo4IWwS6QLzM/2t" crossorigin="anonymous"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.7/dist/contrib/auto-render.min.js" integrity="sha384-+VBxd3r6XgURycqtZ117nYw44OOcIax56Z4dCRWbxyPt0Koah1uHoK0o4+/RRE05" crossorigin="anonymous"
        onload="renderMathInElement(document.body);"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.11.1/katex.min.js"
        integrity="sha256-F/Xda58SPdcUCr+xhSGz9MA2zQBPb0ASEYKohl8UCHc=" crossorigin="anonymous">
</script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/pseudocode@latest/build/pseudocode.min.css">
<script src="https://cdn.jsdelivr.net/npm/pseudocode@latest/build/pseudocode.min.js">
</script>
  <pre id="algo" class="pseudocode" style="display:hidden;">

\usepackage{algorithm2e}
\begin{algorithm}
\For {$t\in \{1,2\}$}{
$\Pi_t \gets \{ \pi_k: \tau(\pi) = t, \pi_k \in \Pi\}$ \\
\For {$\pi_k \in \Pi_t$}
{
$\{x_i\}_{i=1}^N  \gets u_t(\pi_k)$ \;
$i \gets 0$ \;
\While{$|Q(\pi_k)|\geq |\mu(\pi_k)|$ \textbf{or} $u_t(\pi_k) \neq \emptyset$}{
$\mu (x_i) \gets \max (\{\pi_{k, \lambda, \sigma}: \pi_k \in \Pi_t, \lambda, \sigma \in Q(\pi_k) \backslash \mu(\pi_k) \})$ \;
\eIf{ $\mu(x_i) \neq x_i$ }{
$u_t(\pi_k) \gets u_t(\pi_k) \backslash x_i \forall \pi_k \in \Pi$ \;
} {
$u_t(\pi_k) \gets u_t(\pi_k) \backslash x_i \forall \pi_k \in \Pi_t$ \;
}


}

}
} 
\end{algorithm}
</pre>
<script>
    pseudocode.renderElement(document.getElementById("algo"));
</script>



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
2. Agents randomly sample an integer over the range $[0,6]$. This is the number of locations that the agent will find acceptable. The agent then randomly samples that number of locations from the list of all locations. Unlike the firms, the only requirement for locations preferences is that they must find at least one location acceptable. The intern then randomly reorders the sector list to determine their preferences over each sector. The agent then generates their beliefs regarding the firm. The agent's belief regarding the prestige of the firm is generated by sampling a truncated normal distribution over $[0,1]$ with $\mu = \rho_k$ where $\rho_k$ is the mean prestige for the firm $\pi_k$. The agent's belief regarding advancement at the firm is sampled from the truncated normal distribution for each firm. We then generate the attributes for the agent.The agent's "academic performance" is randomly sampled from the truncated normal distribution. The agent generates their "behavior" by sampling three integers from the uniform distribution on $[0,1000]$ and norming the numbers to sum to 1. This will be used to determine "firm fit". Finally, the firm generates a utility function by sampling three integers from the uniform distribution on $[0,1000]$ and norming the numbers to sum to 1. Finally, the agent generates a utility function by sampling five integers from the uniform distribution on $[0,1000]$ and norming the numbers to sum to 1.
3. Firms now generate their beliefs about the agents. An intern's "firm fit" is found through the following operation: $$\phi_{k,n} = 1 - \sum \limits_{i = 1}^3 |c_i^{(k) - c_i^{(n)}}|_1$$ where $c_i$ represents the $i-th$ quality. A firm's belief about an agent's "interview performance" is randomly sampled from the truncated normal distribution and is indepedent of any other firm's beliefs.

4. Firms and agents generate their preference lists according to their utility function and beliefs. Firms generate a preference list over all interns (every intern is acceptable). Interns generate a preference list over tuples $(\pi_k, \lambda_i, \sigma_j)$ (we only rank the tuples that exist in this instance of the simulation), and they may not find every combination of firm, location, and sector acceptable.

### **Process (Without Clearinghouse)**
#### Assumptions
- Firms can only offer each intern once.
- Firms know an intern's rankings for sector and location, but do not know the intern's respective utility function (i.e. whether an intern values location or sector more).
    - When a firm makes an offer, they offer whatever the most preferred sector is in the most preferred available sector (i.e. they assume that the location is valued more than the sector)
- Firms are location and sector-indfifferent.
- Agents accept their most valued offer at time $t$ and cannot retract that offer or be offered again at time $t + 1$. We only consider an offer when it is acceptable to the intern.
    - We can think of each round as a subgame where the set of available interns $\Pi_{t+1} \sub \Pi_t$

#### Algorithm
The following algorithm is used to determine the outcome of the mechanism:
<script>
    pseudocode.renderClass("pseudocode");
</script>
