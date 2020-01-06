
# Blockage contingencies from Norwich to Colchester

# Between two of the stations there are multiple cases.
# 3 Partial block cases for Diss to Ipswich
# 2 Full block cases for Stowmarket to Ipswich

from experta import *
from experta import abstract
import Chatbot

class BlockedRoute(Fact):
    pass

###################################################################################
#               Norwich to Diss (Partial / Full) (Used Trowse contingencies)
###################################################################################
class Disruption_Contingencies(KnowledgeEngine):
    @Rule(BlockedRoute(blockage="partial", origin="Norwich", destination="Diss", intent="schedule"))
    def partial_norwich_diss_schedule(self): 
        self.response = (
            "RUNNING AS BOOKED <br/>\
                    AM PEAK <br/>\
                        All: Greater Anglia services that are unaffected by this incident--<> <br/>\
                    PM PEAK <br/>\
                        All: Greater Anglia services that are unaffected by this incident--<> <br/>\
                    OFF-PEAK <br/>\
                        All: Greater Anglia services that are unaffected by this incident--<> <br/>\
            AMENDED SERVICES <calling pattern> <br/>\
                    AM PEAK <br/>\
                        1 per hour: Greater Anglia Colchester Shuttle--<Operate as Norwich - Colchester Shuttle> <br/>\
                    PM PEAK <br/>\
                        1 per hour: Greater Anglia Colchester Shuttle--<Operate as Norwich - Colchester Shuttle> <br/>\
                    OFF-PEAK <br/>\
                        1 per hour: Greater Anglia Colchester Shuttle--<Operate as Norwich - Colchester Shuttle> <br/>\
            CANCELLED <br/>\
                    AM PEAK <br/>\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> <br/>\
                    PM PEAK <br/>\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> <br/>\
                    OFF-PEAK <br/>\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations>")

    @Rule(BlockedRoute(blockage="partial", origin="Norwich", destination="Diss", intent="advice"))
    def partial_norwich_diss_advice(self):
        self.response = ("None")

    @Rule(BlockedRoute(blockage="full", origin="Norwich", destination="Diss", intent="schedule"))
    def full_norwich_diss_schedule(self):
        self.response = (
            "RUNNING AS BOOKED <br/>\
                    AM PEAK <br/>\
                        All: Greater Anglia services that are unaffected by this incident--<> <br/>\
                    PM PEAK <br/>\
                        All: Greater Anglia services that are unaffected by this incident--<> <br/>\
                    OFF-PEAK <br/>\
                        All: Greater Anglia services that are unaffected by this incident--<> <br/>\
            AMENDED SERVICES <calling pattern> <br/>\
                    AM PEAK <br/>\
                        2 per hour: Greater Anglia G/E Services--<Operates Liverpool Street - Diss> <br/>\
                    PM PEAK <br/>\
                        2 per hour: Greater Anglia G/E Services--<Operates Liverpool Street - Diss> <br/>\
                    OFF-PEAK <br/>\
                        2 per hour: Greater Anglia G/E Services--<Operates Liverpool Street - Diss> <br/>\
            CANCELLED <br/>\
                    AM PEAK <br/>\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> <br/>\
                    PM PEAK <br/>\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> <br/>\
                    OFF-PEAK <br/>\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations>"
        )

    @Rule(BlockedRoute(blockage="full", origin="Norwich", destination="Diss", intent="advice"))
    def full_norwich_diss_advice(self):
        self.response = ("6P40 / 6P41 to divert via Ely & Thetford")


###################################################################################
#                   Diss to Ipswich (Partial blockages A,B,C)
###################################################################################
# A : Diss to Haughley Junction Line Working
# B : Haughley Junction to East Suffolk Junction Working
# C : East Suffolk Junction to Ipswich Working

# A : Diss to Haughley Junction Line Working
    @Rule(BlockedRoute(blockage="partial", origin="Diss", destination="Ipswich", intent="schedule"))
    def partial_diss_ipswich_scheduleA(self):
        self.response = (
            "RUNNING AS BOOKED <br/>\
                    AM PEAK <br/>\
                        All: Greater Anglia services that are unaffected by this incident--<> <br/>\
                    PM PEAK <br/>\
                        All: Greater Anglia services that are unaffected by this incident--<> <br/>\
                    OFF-PEAK <br/>\
                        All: Greater Anglia services that are unaffected by this incident--<> <br/>\
            AMENDED SERVICES <calling pattern> <br/>\
                    AM PEAK <br/>\
                        1 per hour: Greater Anglia Colchester Shuttle--<Opertates Norwich - Colchester Shuttle> <br/>\
                    PM PEAK <br/>\
                        1 per hour: Greater Anglia Colchester Shuttle--<Opertates Norwich - Colchester Shuttle> <br/>\
                    OFF-PEAK <br/>\
                        1 per hour: Greater Anglia Colchester Shuttle--<Opertates Norwich - Colchester Shuttle> <br/>\
            CANCELLED <br/>\
                    AM PEAK <br/>\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> <br/>\
                    PM PEAK <br/>\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> <br/>\
                    OFF-PEAK <br/>\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations>")

    @Rule(BlockedRoute(blockage="partial", origin="Diss", destination="Ipswich", intent="advice"))
    def partial_diss_ipswich_adviceA(self):
        self.response = ("Consider cancelling 6A33 / 6P40")

# B : Haughley Junction to East Suffolk Junction Working
    @Rule(BlockedRoute(blockage="partial", origin="Diss", destination="Ipswich", intent="schedule"))
    def partial_diss_ipswich_scheduleB(self):
       self.response = (
             "RUNNING AS BOOKED <br/>\
                    AM PEAK <br/>\
                        1 per hour: Greater Anglia G/E Services--<> <br/>\
                    PM PEAK <br/>\
                        1 per hour: Greater Anglia G/E Services--<> <br/>\
                    OFF-PEAK <br/>\
                        1 per hour: Freight-1 Freight Path each direction per hour-<Freight to be diverted via London where possible.,> <br/>\
                        1 per hour: Greater Anglia G/E Services--<> <br/>\
            AMENDED SERVICES <calling pattern> <br/>\
                    AM PEAK <br/>\
                        1 per hour: Greater Anglia Cambridge - Ipswich Service--<Operates as Cambridge - Stowmarket Shuttle where <br/>\
                                    possible, however if Stowmarket unavailable, Shuttle to Bury St Edmunds only.> <br/>\
                        1 per hour: Greater Anglia Ipswich Shuttle--<Operates as Liverpool Street - Ipswich> <br/>\
                    PM PEAK <br/>\
                        1 per hour: Greater Anglia Cambridge - Ipswich Service--<Operates as Cambridge - Stowmarket Shuttle where <br/>\
                                    possible, however if Stowmarket unavailable, Shuttle to Bury St Edmunds only.> <br/>\
                        1 per hour: Greater Anglia Ipswich Shuttle--<Operates as Liverpool Street - Ipswich> <br/>\
                    OFF-PEAK <br/>\
                        1 per hour: Greater Anglia Cambridge - Ipswich Service--<Operates as Cambridge - Stowmarket Shuttle where <br/>\
                                    possible, however if Stowmarket unavailable, Shuttle to Bury St Edmunds only.> <br/>\
                        1 per hour: Greater Anglia Ipswich Shuttle--<Operates as Liverpool Street - Ipswich> <br/>\
            CANCELLED <br/>\
                    AM PEAK <br/>\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> <br/>\
                    PM PEAK <br/>\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> <br/>\
                    OFF-PEAK <br/>\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations>")

    @Rule(BlockedRoute(blockage="partial", origin="Diss", destination="Ipswich", intent="advice"))
    def partial_diss_ipswich_adviceB(self):
        self.response = (
            "Freight to be diverted via London <br/>\
            Monitor inbound freight, liaise with freight York & SSM Cambridge re-holding points")

# C : East Suffolk Junction to Ipswich Working
    @Rule(BlockedRoute(blockage="partial", origin="Diss", destination="Ipswich", intent="schedule"))
    def partial_diss_ipswich_scheduleC(self):
        self.response = (
            "RUNNING AS BOOKED <br/>\
                    AM PEAK <br/>\
                        4 per hour: Greater Anglia G/E Services--<> <br/>\
                    PM PEAK <br/>\
                        4 per hour: Greater Anglia G/E Services--<> <br/>\ <br/>\
                    OFF-PEAK <br/>\
                        1 per hour: Freight-1 Freight Path each direction per hour-<> <br/>\
                        4 per hour: Greater Anglia G/E Services--<> <br/>\
            AMENDED SERVICES <calling pattern> <br/>\
                    AM PEAK <br/>\
                        None <br/>\
                    PM PEAK <br/>\
                        None <br/>\
                    OFF-PEAK <br/>\
                        None <br/>\
            CANCELLED <br/>\
                    AM PEAK <br/>\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> <br/>\
                    PM PEAK <br/>\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> <br/>\
                    OFF-PEAK <br/>\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations>")

    @Rule(BlockedRoute(blockage="partial", origin="Diss", destination="Ipswich", intent="advice"))
    def partial_diss_ipswich_adviceC(self):
        self.response = (
            "All 1Pxx services stop addl Stowmarket. <br/>\
            If 2Wxx term stowmarket…bus service Ipswich-Needham Mkt-Stowmarket.")


###################################################################################
#               Diss to Stowmarket (Full)
###################################################################################
    @Rule(BlockedRoute(blockage="full", origin="Diss", destination="Stowmarket", intent="schedule"))
    def full_diss_stowmarket_schedule(self):
        self.response = (
            "RUNNING AS BOOKED <br/>\
                    AM PEAK <br/>\
                        All: Greater Anglia services that are unaffected by this incident--<> <br/>\
                    PM PEAK <br/>\
                        All: Greater Anglia services that are unaffected by this incident--<> <br/>\
                    OFF-PEAK <br/>\
                        All: Greater Anglia services that are unaffected by this incident--<> <br/>\
            AMENDED SERVICES <calling pattern> <br/>\
                    AM PEAK <br/>\
                        1 per hour: Greater Anglia Cambridge - Ipswich Service--<Operates Cambridge - Bury St Edmunds> <br/>\
                        1 per hour: Greater Anglia G/E Service--<Operates Bury St Edmunds - Peterborough> <br/>\
                        2 per hour: Greater Anglia G/E Services--<Operates Liverpool Street - Ipswich> <br/>\
                    PM PEAK <br/>\
                        1 per hour: Greater Anglia Cambridge - Ipswich Service--<Operates Cambridge - Bury St Edmunds> <br/>\
                        1 per hour: Greater Anglia G/E Service--<Operates Bury St Edmunds - Peterborough> <br/>\
                        2 per hour: Greater Anglia G/E Services--<Operates Liverpool Street - Ipswich> <br/>\
                    OFF-PEAK <br/>\
                        1 per hour: Greater Anglia Cambridge - Ipswich Service--<Operates Cambridge - Bury St Edmunds> <br/>\
                        1 per hour: Greater Anglia G/E Service--<Operates Bury St Edmunds - Peterborough> <br/>\
                        2 per hour: Greater Anglia G/E Services--<Operates Liverpool Street - Ipswich> <br/>\
            CANCELLED <br/>\
                    AM PEAK <br/>\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> <br/>\
                    PM PEAK <br/>\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> <br/>\
                    OFF-PEAK <br/>\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations>"
        )

    @Rule(BlockedRoute(blockage="full", origin="Diss", destination="Stowmarket", intent="advice"))
    def full_diss_stowmarket_advice(self):
        self.response = ("Freight to be diverted via London Where possible")

###################################################################################
#               Stowmarket to Ipswich (Full Blockages A/B)
###################################################################################
# A : Haughley Junction Avaliable (GE24)
# B : London End Crossover Avaliable (GE24A)

# A : Haughley Junction Avaliable (GE24)
    @Rule(BlockedRoute(blockage="full", origin="Stowmarket", destination="Ipswich", intent="schedule"))
    def full_stowmarket_ipswich_scheduleA(self):
        self.response = (
            "RUNNING AS BOOKED <br/>\
                    AM PEAK <br/>\
                        All: Greater Anglia services that are unaffected by this incident--<> <br/>\
                    PM PEAK <br/>\
                        All: Greater Anglia services that are unaffected by this incident--<> <br/>\
                    OFF-PEAK <br/>\
                        All: Greater Anglia services that are unaffected by this incident--<> <br/>\
            AMENDED SERVICES <calling pattern> <br/>\
                    AM PEAK <br/>\
                        1 per hour: Greater Anglia Cambridge - Ipswich Service--<Operates Cambridge - Stowmarket> <br/>\
                        1 per hour: Greater Anglia G/E Service--<Operates Stowmarket - Peterborough> <br/>\
                        2 per hour: Greater Anglia G/E Services--<Operates Liverpool Street - Ipswich> <br/>\
                    PM PEAK <br/>\
                        1 per hour: Greater Anglia Cambridge - Ipswich Service--<Operates Cambridge - Stowmarket> <br/>\
                        1 per hour: Greater Anglia G/E Service--<Operates Stowmarket - Peterborough> <br/>\
                        2 per hour: Greater Anglia G/E Services--<Operates Liverpool Street - Ipswich> <br/>\
                    OFF-PEAK <br/>\
                        1 per hour: Greater Anglia Cambridge - Ipswich Service--<Operates Cambridge - Stowmarket> <br/>\
                        1 per hour: Greater Anglia G/E Service--<Operates Stowmarket - Peterborough> <br/>\
                        2 per hour: Greater Anglia G/E Services--<Operates Liverpool Street - Ipswich> <br/>\
            CANCELLED <br/>\
                    AM PEAK <br/>\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> <br/>\
                    PM PEAK <br/>\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> <br/>\
                    OFF-PEAK <br/>\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations>"
        )

    @Rule(BlockedRoute(blockage="full", origin="Stowmarket", destination="Ipswich", intent="advice"))
    def full_stowmarket_ipswich_adviceA(self):
        self.response = ("Will require shunting in and out of the loop at Stowmarket")

# B : London End Crossover Avaliable (GE24A)
    @Rule(BlockedRoute(blockage="full", origin="Stowmarket", destination="Ipswich", intent="schedule"))
    def full_stowmarket_ipswich_scheduleB(self):
        self.response = (
            "RUNNING AS BOOKED <br/>\
                    AM PEAK <br/>\
                        All: Greater Anglia services that are unaffected by this incident--<> <br/>\
                    PM PEAK <br/>\
                        All: Greater Anglia services that are unaffected by this incident--<> <br/>\
                    OFF-PEAK <br/>\
                        All: Greater Anglia services that are unaffected by this incident--<> <br/>\
            AMENDED SERVICES <calling pattern> <br/>\
                    AM PEAK <br/>\
                        1 per hour: Greater Anglia Cambridge - Ipswich Service--<Operates Cambridge - Bury St Edmunds> <br/>\
                        1 per hour: Greater Anglia G/E Service--<Operates Bury St Edmunds - Peterborough> <br/>\
                        2 per hour: Greater Anglia G/E Services--<Operates Liverpool Street - Ipswich> <br/>\
                    PM PEAK <br/>\
                        1 per hour: Greater Anglia Cambridge - Ipswich Service--<Operates Cambridge - Bury St Edmunds> <br/>\
                        1 per hour: Greater Anglia G/E Service--<Operates Bury St Edmunds - Peterborough> <br/>\
                        2 per hour: Greater Anglia G/E Services--<Operates Liverpool Street - Ipswich> <br/>\
                    OFF-PEAK <br/>\
                        1 per hour: Greater Anglia Cambridge - Ipswich Service--<Operates Cambridge - Bury St Edmunds> <br/>\
                        1 per hour: Greater Anglia G/E Service--<Operates Bury St Edmunds - Peterborough> <br/>\
                        2 per hour: Greater Anglia G/E Services--<Operates Liverpool Street - Ipswich> <br/>\
            CANCELLED <br/>\
                    AM PEAK <br/>\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> <br/>\
                    PM PEAK <br/>\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> <br/>\
                    OFF-PEAK <br/>\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations>")

    @Rule(BlockedRoute(blockage="full", origin="Stowmarket", destination="Ipswich", intent="advice"))
    def full_stowmarket_ipswich_adviceB(self):
        self.response = ("In the event that Stowmarket loop is not accessible and Stowmarket London End crossover can not be used.")


###################################################################################
#               Ipswich to ManningTree (Partial / Full blockage)
###################################################################################
    @Rule(BlockedRoute(blockage="partial", origin="Ipswich", destination="Manningtree", intent="schedule"))
    def partial_ipswich_manningtree_schedule(self):
        self.response = (
            "RUNNING AS BOOKED <br/>\
                    AM PEAK <br/>\
                        2 per hour: Greater Anglia G/E Services--<> <br/>\
                    PM PEAK <br/>\
                        2 per hour: Greater Anglia G/E Services--<> <br/>\
                    OFF-PEAK <br/>\
                        1 per hour: Freight-1 Freight Path each direction per hour-<> <br/>\
                        2 per hour: Greater Anglia G/E Services--<> <br/>\
            AMENDED SERVICES <calling pattern> <br/>\
                    AM PEAK <br/>\
                        1 per hour: Greater Anglia Colchester Shuttle--<Operates Liverpool Street - Colchester> <br/>\
                    PM PEAK <br/>\
                        1 per hour: Greater Anglia Colchester Shuttle--<Operates Liverpool Street - Colchester> <br/>\
                    OFF-PEAK <br/>\
                        1 per hour: Greater Anglia Colchester Shuttle--<Operates Liverpool Street - Colchester> <br/>\
            CANCELLED <br/>\
                    AM PEAK <br/>\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> <br/>\
                    PM PEAK <br/>\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> <br/>\
                    OFF-PEAK <br/>\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations>")

    @Rule(BlockedRoute(blockage="partial", origin="Ipswich", destination="Manningtree", intent="advice"))
    def partial_ipswich_manningtree_advice(self):
        self.response = ("Consider extending services through to Manningtree / ECS to Mistley and return for PM peak & Off peak also where possible.")

    @Rule(BlockedRoute(blockage="full", origin="Ipswich", destination="Manningtree", intent="schedule"))
    def full_ipswich_manningtree_schedule(self):
        self.response = (
            "RUNNING AS BOOKED <br/>\
                    AM PEAK <br/>\
                        All: Greater Anglia services that are unaffected by this incident--<> <br/>\
                    PM PEAK <br/>\
                        All: Greater Anglia services that are unaffected by this incident--<> <br/>\
                    OFF-PEAK <br/>\
                        1 per hour: Freight-1 Freight Path each direction per hour-<> <br/>\
                        All: Greater Anglia services that are unaffected by this incident--<> <br/>\
            AMENDED SERVICES <calling pattern> <br/>\
                    AM PEAK <br/>\
                        2 per hour: Greater Anglia G/E Services--<Operates Liverpool Street - Mannningtree> <br/>\
                        2 per hour: Greater Anglia Ipswich Shuttle--<Operates as Norwich - Ipswich Shuttle> <br/>\
                    PM PEAK <br/>\
                        2 per hour: Greater Anglia G/E Services--<Operates Liverpool Street - Mannningtree> <br/>\
                        2 per hour: Greater Anglia Ipswich Shuttle--<Operates as Norwich - Ipswich Shuttle> <br/>\
                    OFF-PEAK <br/>\
                        2 per hour: Greater Anglia G/E Services--<Operates Liverpool Street - Mannningtree> <br/>\
                        2 per hour: Greater Anglia Ipswich Shuttle--<Operates as Norwich - Ipswich Shuttle> <br/>\
            CANCELLED <br/>\
                    AM PEAK <br/>\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> <br/>\
                    PM PEAK <br/>\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> <br/>\
                    OFF-PEAK <br/>\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations>")

    @Rule(BlockedRoute(blockage="full", origin="Ipswich", destination="Manningtree", intent="advice"))
    def full_ipswich_manningtree_advice(self):
        self.response = (
            "Shunting to take place at Manningtree North Jn if available. Shunting can also take place at Mistley. Permission should be obtained from Operations <br/>\
            on-call level 2 to start passenger services from the down main platform (platform 3) at Manningtree if this is necessary. <br/>\
            Divert freight via BurySt Edmunds & across country up to W9 traffic only")


###################################################################################
#               Manningtree to Colchester (partial / full blockage)
###################################################################################
    @Rule(BlockedRoute(blockage="partial", origin="Manningtree", destination="Colchester", intent="schedule"))
    def partial_manningtree_colchester_schedule(self):
        self.response = (
            "RUNNING AS BOOKED <br/>\
                    AM PEAK <br/>\
                        2 per hour: Greater Anglia G/E Services--<> <br/>\
                    PM PEAK <br/>\
                        2 per hour: Greater Anglia G/E Services--<> <br/>\
                    OFF-PEAK <br/>\
                        1 per hour: Freight-1 Freight Path each direction per hour-<> <br/>\
                        2 per hour: Greater Anglia G/E Services--<> <br/>\
            AMENDED SERVICES <calling pattern> <br/>\
                    AM PEAK <br/>\
                        1 per hour: Greater Anglia Colchester Shuttle--<Operates Liverpool Street - Colchester> <br/>\
                    PM PEAK <br/>\
                        1 per hour: Greater Anglia Colchester Shuttle--<Operates Liverpool Street - Colchester> <br/>\
                    OFF-PEAK <br/>\
                        1 per hour: Greater Anglia Colchester Shuttle--<Operates Liverpool Street - Colchester> <br/>\
            CANCELLED <br/>\
                    AM PEAK <br/>\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> <br/>\
                    PM PEAK <br/>\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> <br/>\
                    OFF-PEAK <br/>\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations>")

    @Rule(BlockedRoute(blockage="partial", origin="Manningtree", destination="Colchester", intent="advice"))
    def partial_manningtree_colchester_advice(self):
        self.response = (
            "- GriffinWharf may be blocked <br/>\
             -“Flighting” of trains is preferable to ensure as many trains through the sections as possible.")

    @Rule(BlockedRoute(blockage="full", origin="Manningtree", destination="Colchester", intent="schedule"))
    def full_manningtree_colchester_schedule(self):
        self.response = (
            "RUNNING AS BOOKED <br/>\
                    AM PEAK <br/>\
                        All: Greater Anglia services that are unaffected by this incident--<> <br/>\
                    PM PEAK <br/>\
                        All: Greater Anglia services that are unaffected by this incident--<> <br/>\
                    OFF-PEAK <br/>\
                        All: Greater Anglia services that are unaffected by this incident--<> <br/>\
            AMENDED SERVICES <calling pattern> <br/>\
                    AM PEAK <br/>\
                        2 per hour: Greater Anglia G/E Service--<Operates Norwich - Manningtree> <br/>\
                        2 per hour: Greater Anglia G/E Services--<Operates Liverpool Street - Colchester> <br/>\
                    PM PEAK <br/>\
                        2 per hour: Greater Anglia G/E Service--<Operates Norwich - Manningtree> <br/>\
                        2 per hour: Greater Anglia G/E Services--<Operates Liverpool Street - Colchester> <br/>\
                    OFF-PEAK <br/>\
                        2 per hour: Greater Anglia G/E Service--<Operates Norwich - Manningtree> <br/>\
                        2 per hour: Greater Anglia G/E Services--<Operates Liverpool Street - Colchester> <br/>\
            CANCELLED <br/>\
                    AM PEAK <br/>\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> <br/>\
                    PM PEAK <br/>\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> <br/>\
                    OFF-PEAK <br/>\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations>")

    @Rule(BlockedRoute(blockage="full", origin="Manningtree", destination="Colchester", intent="advice"))
    def full_manningtree_colchester_advice(self):
        self.response = ("Divert freight via BurySt Edmunds & across country up to W9 traffic only")

def respond(values):
    engine = Disruption_Contingencies()
    engine.reset()
    engine.declare(BlockedRoute(blockage=values[0], origin=values[1], destination=values[2], intent=values[3]))
    engine.run()
    if hasattr(engine, 'response'):
        value = engine.response
        return value
    else:
        return None
    


def main():
    values = ['partial', 'Norwich', 'Diss', 'schedule']
    print(respond(values))
    
if __name__ == '__main__':
    main()










