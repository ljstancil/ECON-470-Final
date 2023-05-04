'''
© Luke Stancil, 2023 for the purposes of the Market Design ECON 470 class at Rice University. 
'''


import pickle
import random as r
from collections import defaultdict as dd

import openpyxl
import pandas as pd
import scipy.stats as stats

# define locations as tuples with a number and sectors
# sectors/industries can be defined as Agriculture, Consumer Goods (technology),
#  Energy, Financial Services, Retail, and Transportation
r.seed(10)


# initialize locations
std_locations = [(1,['A','C','E','F','R','T']),(2,['C','E','F','R','T']),(3,['A','C','F','R'])] # these locations and sectors are present for each firm
new_locations = [(4, ['A','R','T']),(5, ['C','E','T']),(6, ['A','E','R'])]
# initialize sectors (this will be for interns to create their preferences)
sectors = ['A', 'C', 'E', 'F', 'R', 'T']
# all_locations = std_locations+new_locations
all_locations = [1, 2, 3, 4, 5, 6]

class Intern:
    def generatePreferences(self, banks):
        '''
        We want to generate preferences over every combination of offers.
        This will save us computation time on the backend and make it easier to compare answers
        '''
        mult_s, mult_p, mult_a, mult_l, mult_i = self.util_fxn
        poss_offers = []
        # we loop through the banks and each possible offer
        salary_rank_list = sorted(banks, key=lambda bank: bank.salary)
        prestige_rank_list = sorted(banks, key=lambda bank: self.prestige_dict[bank])
        advance_rank_list = sorted(banks, key=lambda bank: self.advance_dict[bank])
        location_rank_list = self.locations
        sector_rank_list = self.sectors
        for bank in banks:
            salary_rank = salary_rank_list.index(bank) + 1
            prestige_rank = prestige_rank_list.index(bank) + 1
            advance_rank = advance_rank_list.index(bank) + 1
            score = mult_s/salary_rank + mult_p/prestige_rank + mult_a/advance_rank
            for ind, location in bank.loc_dict.items():
                if ind in location_rank_list:
                    location_rank = location_rank_list.index(ind) + 1
                    loc_score = score + mult_l/location_rank
                    for sector_ind in location.sectors:
                        sector_rank = sector_rank_list.index(sector_ind) + 1
                        total_score = loc_score + mult_i/sector_rank
                        poss_offers.append((total_score, (bank, ind, sector_ind)))
        ranked_offers = sorted(poss_offers, key=lambda offer:offer[0])
        return [offer[1] for offer in ranked_offers]
    
    def __init__(self, banks, name) -> None:
        self.name = f'I{name}'
        # generate the locations where the intern is willing to work
        # note: r.sample() will return in a random order, so a shuffle is not needed.
        self.locations = r.sample(all_locations, r.randint(3,6)) # 
        # we assume that an intern is willing to work in every sector, but they will rank
        self.sectors = r.sample(sectors, len(sectors))
        # generate beliefs about prestige
        prestige_dict = {}
        for bank in banks:
            prestige = stats.truncnorm.rvs(0, 1, loc = bank.prestige_mean)
            prestige_dict[bank] = (prestige)
        self.prestige_dict = prestige_dict
        # generate beliefs about advancement opportunities
        advance_dict = {}
        for bank in banks:
            belief = stats.truncnorm.rvs(0, 1, loc = 0.5)
            advance_dict[bank] = belief
        self.advance_dict = advance_dict
        # generate details about student's academic performance
        self.academics = stats.truncnorm.rvs(0,1)
        # generate "qualities" that firms can turn into their belief about firm fit
        g, h, i = r.sample(range(0,1000), 3)
        # generate a candidates "personality"
        self.qualities = (g/(g+h+i), h/(g+h+i), i/(g+h+i))
        # generate list of coefficients to multiply by 1/ordinal to compare offers for 
        # interns 
        a,b,c,d,e = r.sample(range(0,1000), 5)
        u_sum = a+b+c+d+e
        # we do this to ensure they sum to 1
        self.util_fxn = (a/u_sum, b/u_sum, c/u_sum, d/u_sum, e/u_sum)
        self.accepted = False
        self.preferences = self.generatePreferences(banks)
        self.placement = [(None, None)]*31
        self.agent_daa = None
        self.firm_daa = None           

class Bank:
    def __init__(self, name):
        # set a name for the bank (this is for analysis purpose and does
        # not reflect anything about the banks in general)
        # have three locations be with every bank
        # three locations randomly select how many they
        # have & which 
        self.name = name
        locations = list(std_locations)
        new_loc = r.sample(new_locations, r.randint(0,3))
        # concatenate locations with new locations
        locations += new_loc
        locations.sort()
        loc_dict = {}
        for ind, sectors in locations:
            loc_dict[ind] = self.Location(ind, sectors)
        self.loc_dict = loc_dict
        # randomly select the stage t = 0,..., 5 where they offer.
        self.offer_period = None
        # salary is generated just to rank
        self.salary = r.random()
        # generate mean for prestige (truncated normal, but should it be?)
        self.prestige_mean = stats.truncnorm.rvs(0, 1)
        a, b, c = r.sample(range(0,1000), 3)
        # generate standards for their "culture" the differences of these will
        # determine how good a fit a candidate is
        self.culture_norms = (a/(a+b+c), b/(a+b+c), c/(a+b+c))
        # generate utility function
        d,e,f = r.sample(range(0,1000), 3)
        self.u_fxn = (d/(d+e+f), e/(d+e+f), f/(d+e+f))
        self.total_quota = sum([location.total_quota for ind, location in self.loc_dict.items()])
        self.total_hired = 0
        self.ranking = None

    class Location:
            def __init__(self, ind,sectors) -> None:
                self.sectors = {}
                # for each sector, generate a quota
                total_quota = 0
                for sector in sectors:        
                    new_sector = self.Sector(sector)        
                    self.sectors[sector] = (new_sector)
                    total_quota += new_sector.quota
                self.total_quota = total_quota
                self.hired = 0
            class Sector:
                def __init__(self, name) -> None:
                    self.name = name
                    self.quota = r.randint(3,10)
                    self.interns = dd(list)
                    self.agent_daa = None
                    self.firm_daa = []

    def rankInterns(self, interns):
        ranking = []
        c1, c2, c3 = self.culture_norms
        u1, u2, u3 = self.u_fxn
        for intern in interns:
            i1, i2, i3 = intern.qualities
            fit = 1 - abs(c1-i1) - abs(c2-i2) - abs(c3-i3)
            interview_score = stats.truncnorm.rvs(0,1)
            total_score = u1*intern.academics + u2*interview_score + u3*fit
            ranking.append((total_score, intern))
        self.ranking = sorted(ranking, reverse=True)


    def __repr__(self):
        loc_string = '\n'.join([f'{ind}: {loc}' for ind, loc in self.loc_dict.items()])
        sec_string = f'\n {loc_string} \n Salary: {self.salary} \n Prestige: {self.prestige_mean} \n Offer Timeline: {self.offer_period}'
        return f'Bank: {self.name}'
    # def __str__(self) -> str:
    #     return f'Bank Str: {self.name}'

def makeOffer(bank, intern, s):
    offers = []
    pref_sectors = intern.sectors
    pref_locations = intern.locations
    #bank_locs = {ind:loc for ind,loc in bank.loc_dict.items() if loc.total_quota > loc.hired}
    bank_locs = bank.loc_dict
    for location in pref_locations:
        try:
            bank_loc = bank_locs[location]
            if bank_loc.total_quota != bank_loc.hired:
                available_sectors = {name:sector_info for name, sector_info in bank_loc.sectors.items() if sector_info.quota > len(sector_info.interns[s])}
                for sector in pref_sectors:
                    if sector in available_sectors:
                        return (bank, location, sector)
            else:continue
        except:continue
  
def generateInternsBanks():
    bank_names = ['Goldman Sachs', 'JP Morgan', 'Citi', 'Morgan Stanley', 'Bank of America']
    banks = []

    # generate banks
    for name in bank_names:
        bank = Bank(name)
        banks.append(bank)
    # generate interns
    interns = []
    intern_num = range(10000)
    interns = [Intern(banks, i) for i in intern_num]

    for bank in banks:
        bank.rankInterns(interns)
    tot_quot = 0
    for bank in banks:
        for ind, location in bank.loc_dict.items():
            for sector_ind, sector in location.sectors.items():
                tot_quot += sector.quota

    # clean set
    # Q = tot_quot
    # init_rejects = set()
    # for bank in banks:
    #     bank_lower = bank.ranking[Q+1:]
    #     bank_rejects = set([int_tup[1] for int_tup in bank_lower])
        
    #     if len(init_rejects) > 0:
    #         init_rejects = init_rejects.intersection(bank_rejects)
    #     else:
    #         init_rejects = bank_rejects
    # rejects = set.intersection(init_rejects)
    # for bank in banks:
    #     bank.ranking = [int_tup for int_tup in bank.ranking if int_tup[1] not in rejects]
    return banks, interns

def placement(banks, s):
    '''
    Generate a placement assignment for the firms and interns given their respective preferences and assigned types
    
    '''
    for t in range(0,2):
        banks_list = [bank for bank in banks if bank.offer_period == t]
        # we can go through the top intern for each bank and compare offers
        banks_pref = {bank: bank.ranking.copy() for bank in banks_list}
        for init_bank in banks_list:
            while init_bank.total_hired != init_bank.total_quota:
                proposal_num = init_bank.total_quota - init_bank.total_hired
                preferred_interns = banks_pref[init_bank]
                available_interns = [intern for intern in preferred_interns if not intern[1].accepted][:proposal_num]
                for intern in available_interns:
                    intern_preferences = intern[1].preferences
                    offers = []
                    for bank in banks_list:
                        ind_preferred_interns = banks_pref[bank]
                        ind_available_interns = [intern for intern in ind_preferred_interns if not intern[1].accepted][:(bank.total_quota - bank.total_hired)]
                        if intern in ind_available_interns:
                            offer = makeOffer(bank,intern[1], s)
                            if offer != None:
                                offers.append(offer)
                        else:continue
                    if len(offers) > 0:
                        best_offer = max([(intern_preferences.index(offer), offer) for offer in offers], key=lambda offer:offer[0])
                        # update bank information
                        winning_offer = best_offer[1]
                        winning_bank = winning_offer[0]
                        winning_bank.total_hired += 1
                        loc_index = winning_offer[1]
                        sec_index = winning_offer[2]
                        winning_location = winning_bank.loc_dict[loc_index]
                        winning_location.hired += 1
                        winning_location.sectors[sec_index].interns[s].append(intern)
                        intern[1].accepted = True
                        intern[1].placement[s-1] = (best_offer)
                        if winning_bank.total_hired == winning_bank.total_quota:break
                        else:continue
                    else:
                        banks_pref[winning_bank].remove(intern)

def agentProposing(agents:list([Intern]), firms):
    '''
    This function determines the agent-optimal Gale-Shapley matching
    for agents
    '''
    agent_proposals = {agent: agent.preferences.copy() for agent in agents}
    firm_proposals = {}
    for firm in firms:
        bank_locs = firm.loc_dict
        for loc_ind, location in bank_locs.items():
            for sector_ind, sector in location.sectors.items():
                firm_proposals[(firm, loc_ind, sector_ind)] = {'quota': sector.quota, 'interns':[], 'new_proposals': []}

    proposing_agents = agents.copy()
    t = 0
    while len(proposing_agents) != 0:
        print("AGENT PROPOSING DAA ROUND: " + str(t))
        t += 1
        new_agents = []
        for agent in proposing_agents:
            # go from their top choices
            agent_preferences = agent_proposals[agent]
            new_proposal = agent_preferences.pop(0)
            firm_proposals[new_proposal]['new_proposals'].append(agent)
        for details, option in firm_proposals.items():
            firm = details[0]
            poss_agents = []
            new_proposals = option['new_proposals']
            option['new_proposals'] = []
            if len(new_proposals) > 0:
                ranking = [intern_tup[1] for intern_tup in firm.ranking]
                current_interns = option['interns']
                for intern in new_proposals:
                    rank_ind = ranking.index(intern)
                    rank = firm.ranking[rank_ind]
                    poss_agents.append(rank)
                quota = option['quota']
                
                current_ranking = current_interns + poss_agents

                if len(current_ranking) > 0:
                    new_interns = [intern_obj for intern_obj in sorted(current_ranking, key=lambda tup:tup[0])][-quota:]
                    rejects = list(set(current_ranking)- set(new_interns))
                else:
                    new_interns = []
                    rejects = []
                option['interns'] = new_interns
                for reject in rejects:
                    if len(agent_proposals[reject[1]]) > 0:
                        new_agents.append(reject[1])
        proposing_agents = new_agents
    
    # finish them
    for details, option in firm_proposals.items():
        firm = details[0]
        location = firm.loc_dict[details[1]]
        sector = location.sectors[details[2]]
        matched_interns = option['interns']
        sector.agent_daa = matched_interns
        for intern in matched_interns:
            intern[1].agent_daa = details

        
                    
            # else:continue

def firmProposing(agents, firms):
    '''
    A function to determine the Gale-Shapley matching for firms with multiple locations.
    Firms made their first 
    
    '''
    # firm_proposals = {agent: agent.preferences.copy() for agent in firms}
    proposing_firms = {}
    for firm in firms:
        bank_locs = firm.loc_dict
        for loc_ind, location in bank_locs.items():
            for sector_ind, sector in location.sectors.items():
                proposing_firms[(firm, loc_ind, sector_ind)] = {'quota': sector.quota, 'interns':[], 'preferences': firm.ranking.copy()}
    proposing_agents = {agent:{'preferences': agent.preferences, 'new_proposals': [], 'current_firm': None} for agent in agents}
    firms_to_propose = proposing_firms
    t = 0
    while len(firms_to_propose) != 0:
        print("FIRM PROPOSING DAA ROUND: " + str(t))
        t += 1
        new_firms = {}
        for firm, details in firms_to_propose.items():
            # go from their top choices
            firm_preferences = details['preferences']
            # calculate the amount of proposals they will be making in this round
            remaining_spots = details['quota'] - len(details['interns'])
            new_proposals = firm_preferences[:remaining_spots]
            del firm_preferences[:remaining_spots]
            for proposal in new_proposals:
                proposing_agents[proposal[1]]['new_proposals'].append(firm)
        for agent, details in proposing_agents.items():
            new_proposals = details['new_proposals'].copy()
            details['new_proposals'] = []
            if len(new_proposals) > 0:
                rejects = []
                current_firm = details['current_firm']
                ranking = []
                if current_firm != None: ranking.append(current_firm)
                for firm in new_proposals:
                    if firm in agent.preferences:
                        rank = agent.preferences.index(firm)
                        ranking.append((rank, firm))
                    else:
                        rejects.append(firm)
                if len(ranking) > 0:
                    best_firm = min(ranking, key=lambda tup: tup[0])
                    if current_firm == None:
                        details['current_firm'] = best_firm
                        proposing_firms[best_firm[1]]['interns'].append(agent)
                        rejects.extend([firm for firm in new_proposals if firm != best_firm])
                        for reject in rejects:
                            firm = proposing_firms[reject]
                            if firm['quota'] - len(firm['interns']) > 0:
                                new_firms[reject] = firm
                    elif best_firm[0] < current_firm[0]:
                        details['current_firm'] = best_firm 
                        proposing_firms[current_firm[1]]['interns'].remove(agent)
                        proposing_firms[best_firm[1]]['interns'].append(agent)
                        rejects = [firm for firm in new_proposals if firm != best_firm]
                        rejects.append(current_firm[1])
                        for reject in rejects:
                            firm = proposing_firms[reject]
                            if firm['quota'] - len(firm['interns']) > 0:
                                new_firms[reject] = firm

                    else:
                        rejects = new_proposals.copy()
                        for reject in rejects:
                            firm = proposing_firms[reject]
                            if firm['quota'] - len(firm['interns']) > 0:
                                new_firms[reject] = firm
                else:
                    for reject in rejects:
                            firm = proposing_firms[reject]
                            if firm['quota'] - len(firm['interns']) > 0:
                                new_firms[reject] = firm
            
            else:continue

        firms_to_propose = new_firms
    
    for details, option in proposing_firms.items():
        firm = details[0]
        location = firm.loc_dict[details[1]]
        sector = location.sectors[details[2]]
        matched_interns = option['interns']
        ranking = [intern_tup[1] for intern_tup in firm.ranking]
        for intern in matched_interns:

            rank_ind = ranking.index(intern)
            rank = firm.ranking[rank_ind]
            sector.firm_daa.append(rank)
        #sector.firm_daa = matched_interns
        for intern in matched_interns:
            intern.firm_daa = details

def run_test():        
    banks, interns =  generateInternsBanks()       
    s = 1
    for t1 in [0, 1]:
        for t2 in [0,1]:
            for t3 in [0, 1]:
                for t4 in [0,1]:
                    for t5 in [0, 1]:
                        if s == 32:break
                        else:
                            print("Placement Iteration " + str(s))
                            banks[0].offer_period = t1
                            banks[1].offer_period = t2
                            banks[2].offer_period = t3
                            banks[3].offer_period = t4
                            banks[4].offer_period = t5
                            banks.sort(key= lambda bank:bank.offer_period)
                            placement(banks, s)
                            for bank in banks:
                                print(bank)
                                print(bank.offer_period)
                                print(bank.total_quota)
                                print(bank.total_hired)
                                bank.total_hired = 0
                                bank_locs = bank.loc_dict
                                for loc_ind, location in bank_locs.items():
                                    location.hired = 0
                            for intern in interns:
                                intern.accepted = False
                            s+=1


    agentProposing(interns, banks)

    firmProposing(interns, banks)

    num_col = 0
    for bank in banks:
        for ind, location in bank.loc_dict.items():
            num_col += len(location.sectors)

    num_firm_col = len(banks[0].ranking)
    df = pd.DataFrame(columns= ['Intern', 'Without Clearinghouse', 'Agent DAA', 'Firm DAA'])
    intern_attr_df = pd.DataFrame(columns= ['Intern', ])
    pref_df = pd.DataFrame(columns = ['Intern'] + list(range(1, num_col + 1)))
    firm_pref_df = pd.DataFrame(columns = ['Bank'] + list(range(1, num_firm_col + 1)))
    intern_placement_df = pd.DataFrame(columns = ['Intern'] + list(range(1, 32)))
    bank_placement_df = pd.DataFrame(columns = ['Bank'] + list(range(1, 32)))
    bank_daa_df = pd.DataFrame(columns = ["Bank", "Agent-Proposing", "Firm-Proposing"])

    print("Calculating Ranks")
    with open('intern_obj', 'wb') as dump_file:
    # Step 3
        pickle.dump(interns, dump_file)
    with open('bank_obj', 'wb') as dump_file:
    # Step 3
        pickle.dump(banks, dump_file)
    # export data to dataframes
    for intern in interns:
        print(intern.name)
        preferences = intern.preferences
        pref = [intern.name] + preferences
        pref_row = pd.Series(pref)
        pref_df.loc[len(pref_df)] = pref_row
        if len(intern.placement) > 0:
            util = 0
            place_row = [intern.name]
            for place in intern.placement:
                place_row.append(place)
                if place[0] == None:
                    continue
                else:
                    util += 1/((place[0]+1)*31)
            intern_placement_df.loc[len(intern_placement_df)] = place_row
            placement_rank = util
        else:
            placement_rank = None
        if intern.agent_daa != None:    
            pref_ind = preferences.index(intern.agent_daa) + 1
            int_agent_rank = (1/pref_ind, intern.agent_daa)
        else:
            int_agent_rank = None
        if intern.firm_daa != None:
            pref_ind = preferences.index(intern.firm_daa) + 1
            int_firm_rank = (1/pref_ind, intern.firm_daa)
        else:
            int_firm_rank = None
        row_to_add = [intern.name, placement_rank, int_agent_rank, int_firm_rank]
        df.loc[len(df)] = row_to_add
    firm_df = pd.DataFrame(columns= ['Bank', 'Without Clearinghouse', 'Agent DAA', 'Firm DAA'])
    daa_df = pd.DataFrame(columns = ['Bank', "Agent-Proposing", "Firm-Proposing"])
    for bank in banks:
        print(bank.name)
        preferences = bank.ranking
        preferences_row = [bank.name] + preferences
        pref_row = pd.Series(preferences_row)
        firm_pref_df.loc[len(firm_pref_df)] = pref_row
        placement_sum = 0
        agent_results = []
        firm_results = []
        
        bank_agent_rank = 0
        bank_firm_rank = 0
        bank_locs = bank.loc_dict
        placement_s = dd(dd(list))
        for loc_ind, location in bank_locs.items():
            for sector_ind, sector in location.sectors.items():
                for s, interns in sector.interns.items():
                    for intern in interns:
                        pref_ind = preferences.index(intern) + 1
                        placement_s[s].append((pref_ind, intern[1].name))
                        placement_sum += 1/(pref_ind*31)
                for intern in sector.agent_daa:
                    pref_ind = preferences.index(intern) + 1
                    agent_results.append((pref_ind, intern[1].name))
                    bank_agent_rank += 1/pref_ind
                if sector.firm_daa != None:
                    for intern in sector.firm_daa:
                        pref_ind = preferences.index(intern) + 1
                        firm_results.append((pref_ind, intern[1].name))
                        bank_firm_rank += 1/pref_ind
        row_to_add = [bank.name, placement_sum , bank_agent_rank, bank_firm_rank]
        firm_df.loc[len(firm_df)] = row_to_add
        daa_row = [bank.name, agent_results, firm_results]
        placement_results = [interns for s, interns in placement_s.items()]
        print(len(placement_results))
        place_row = [bank.name] + placement_results
        bank_daa_df.loc[len(bank_daa_df)] = daa_row
        bank_placement_df.loc[len(bank_placement_df)] = place_row




    with pd.ExcelWriter('InternMatchingResults.xlsx') as writer:
        df.to_excel(writer, sheet_name= 'Intern Results')
        firm_df.to_excel(writer, sheet_name= "Firm Results")
        pref_df.to_excel(writer, sheet_name = 'Intern Preferences')
        firm_pref_df.to_excel(writer, sheet_name = 'Firm Preferences')
        intern_placement_df.to_excel(writer, sheet_name= "Intern Placement Complete")
        bank_placement_df.to_excel(writer, sheet_name= "Bank Placement Complete")
        bank_daa_df.to_excel(writer, sheet_name= "Bank DAA Complete Results")

def findBlockingPairs():
    intern_file = 'intern_obj.pickle'
    bank_file = 'bank_obj.pickle'
    with open(intern_file, 'rb') as f: intern_list = pickle.load(f)
    with open(bank_file, 'rb') as f: bank_list = pickle.load(f)
    df = pd.DataFrame(columns = ['Round', 'Number', 'Pairs'])
    for i in range(1, 32):
        blocking_pairs = []
        print(i)
        current_interns = [intern for intern in intern_list if intern.placement[i-1] != (None, None)]
        print(len(current_interns))
        for intern in current_interns:
            current_firm = intern.placement[i-1]
            current_place = intern.preferences.index(current_firm[1])
            higher_firms = intern.preferences[:current_place]
            better_firms = [new_firm for new_firm in higher_firms if new_firm[0] != current_firm]
            while len(better_firms) > 0:
                firm_tup = better_firms.pop(0)
                firm = firm_tup[0]
                loc = firm_tup[1]
                sector = firm_tup[2]
                ranking = [intern_tup[1] for intern_tup in firm.ranking]
                intern_ind = ranking.index(intern)
                intern_val = firm.ranking[intern_ind]
                firm_interns = firm.loc_dict[loc].sectors[sector].interns[i]
                if any(intern_val[0] > tup[0] for tup in firm_interns):
                    blocking_pairs.append((intern.name, firm_tup))
                    better_firms = [new_firm for new_firm in better_firms if new_firm[0] != firm]

        row_to_add = [i, len(blocking_pairs), blocking_pairs]
        df.loc[len(df)] = row_to_add

    with pd.ExcelWriter('BlockingPairs.xlsx') as writer:
        df.to_excel(writer)
                        
                
