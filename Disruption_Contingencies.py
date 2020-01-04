
# Blockage contingencies from Norwich to Colchester

# Between two of the stations there are multiple cases.
# 3 Partial block cases for Diss to Ipswich
# 2 Full block cases for Stowmarket to Ipswich

from experta import *
import Chatbot

class BlockedRoute(Fact):
    pass

class Time_of_day(Fact):
    pass
###################################################################################
#               Norwich to Diss (Partial / Full) (Used Trowse contingencies)
###################################################################################
    @Rule(BlockedRoute(blockage="partial", origin="Norwich", destination="Diss", intent="schedule"))
    def partial_norwich_diss_schedule(self):
        return(
            "RUNNING AS BOOKED \n\
                    AM PEAK \n\
                        All: Greater Anglia services that are unaffected by this incident--<> \n\
                    PM PEAK \n\
                        All: Greater Anglia services that are unaffected by this incident--<> \n\
                    OFF-PEAK \n\
                        All: Greater Anglia services that are unaffected by this incident--<> \n\
            AMENDED SERVICES <calling pattern> \n\
                    AM PEAK \n\
                        1 per hour: Greater Anglia Colchester Shuttle--<Operate as Norwich - Colchester Shuttle> \n\
                    PM PEAK \n\
                        1 per hour: Greater Anglia Colchester Shuttle--<Operate as Norwich - Colchester Shuttle> \n\
                    OFF-PEAK \n\
                        1 per hour: Greater Anglia Colchester Shuttle--<Operate as Norwich - Colchester Shuttle> \n\
            CANCELLED \n\
                    AM PEAK \n\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
                    PM PEAK \n\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
                    OFF-PEAK \n\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations>")

    @Rule(BlockedRoute(blockage="partial", origin="Norwich", destination="Diss", intent="advise"))
    def partial_norwich_diss_advise(self):
        return("None")

    @Rule(BlockedRoute(blockage="full", origin="Norwich", destination="Diss", intent="schedule"))
    def full_norwich_diss_schedule(self):
        return(
            "RUNNING AS BOOKED \n\
                    AM PEAK \n\
                        All: Greater Anglia services that are unaffected by this incident--<> \n\
                    PM PEAK \n\
                        All: Greater Anglia services that are unaffected by this incident--<> \n\
                    OFF-PEAK \n\
                        All: Greater Anglia services that are unaffected by this incident--<> \n\
            AMENDED SERVICES <calling pattern> \n\
                    AM PEAK \n\
                        2 per hour: Greater Anglia G/E Services--<Operates Liverpool Street - Diss> \n\
                    PM PEAK \n\
                        2 per hour: Greater Anglia G/E Services--<Operates Liverpool Street - Diss> \n\
                    OFF-PEAK \n\
                        2 per hour: Greater Anglia G/E Services--<Operates Liverpool Street - Diss> \n\
            CANCELLED \n\
                    AM PEAK \n\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
                    PM PEAK \n\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
                    OFF-PEAK \n\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations>"
        )

    @Rule(BlockedRoute(blockage="full", origin="Norwich", destination="Diss", intent="advise"))
    def full_norwich_diss_advise(self):
        return("6P40 / 6P41 to divert via Ely & Thetford")


###################################################################################
#                   Diss to Ipswich (Partial blockages A,B,C)
###################################################################################
# A : Diss to Haughley Junction Line Working
# B : Haughley Junction to East Suffolk Junction Working
# C : East Suffolk Junction to Ipswich Working

# A : Diss to Haughley Junction Line Working
    @Rule(BlockedRoute(blockage="partial", origin="Diss", destination="Ipswich", intent="schedule"))
    def partial_diss_ipswich_scheduleA(self):
        return(
            "RUNNING AS BOOKED \n\
                    AM PEAK \n\
                        All: Greater Anglia services that are unaffected by this incident--<> \n\
                    PM PEAK \n\
                        All: Greater Anglia services that are unaffected by this incident--<> \n\
                    OFF-PEAK \n\
                        All: Greater Anglia services that are unaffected by this incident--<> \n\
            AMENDED SERVICES <calling pattern> \n\
                    AM PEAK \n\
                        1 per hour: Greater Anglia Colchester Shuttle--<Opertates Norwich - Colchester Shuttle> \n\
                    PM PEAK \n\
                        1 per hour: Greater Anglia Colchester Shuttle--<Opertates Norwich - Colchester Shuttle> \n\
                    OFF-PEAK \n\
                        1 per hour: Greater Anglia Colchester Shuttle--<Opertates Norwich - Colchester Shuttle> \n\
            CANCELLED \n\
                    AM PEAK \n\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
                    PM PEAK \n\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
                    OFF-PEAK \n\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations>")

    @Rule(BlockedRoute(blockage="partial", origin="Diss", destination="Ipswich", intent="advise"))
    def partial_diss_ipswich_adviseA(self):
        return("Consider cancelling 6A33 / 6P40")

# B : Haughley Junction to East Suffolk Junction Working
    @Rule(BlockedRoute(blockage="partial", origin="Diss", destination="Ipswich", intent="schedule"))
    def partial_diss_ipswich_scheduleB(self):
       return(
             "RUNNING AS BOOKED \n\
                    AM PEAK \n\
                        1 per hour: Greater Anglia G/E Services--<> \n\
                    PM PEAK \n\
                        1 per hour: Greater Anglia G/E Services--<> \n\
                    OFF-PEAK \n\
                        1 per hour: Freight-1 Freight Path each direction per hour-<Freight to be diverted via London where possible.,> \n\
                        1 per hour: Greater Anglia G/E Services--<> \n\
            AMENDED SERVICES <calling pattern> \n\
                    AM PEAK \n\
                        1 per hour: Greater Anglia Cambridge - Ipswich Service--<Operates as Cambridge - Stowmarket Shuttle where \n\
                                    possible, however if Stowmarket unavailable, Shuttle to Bury St Edmunds only.> \n\
                        1 per hour: Greater Anglia Ipswich Shuttle--<Operates as Liverpool Street - Ipswich> \n\
                    PM PEAK \n\
                        1 per hour: Greater Anglia Cambridge - Ipswich Service--<Operates as Cambridge - Stowmarket Shuttle where \n\
                                    possible, however if Stowmarket unavailable, Shuttle to Bury St Edmunds only.> \n\
                        1 per hour: Greater Anglia Ipswich Shuttle--<Operates as Liverpool Street - Ipswich> \n\
                    OFF-PEAK \n\
                        1 per hour: Greater Anglia Cambridge - Ipswich Service--<Operates as Cambridge - Stowmarket Shuttle where \n\
                                    possible, however if Stowmarket unavailable, Shuttle to Bury St Edmunds only.> \n\
                        1 per hour: Greater Anglia Ipswich Shuttle--<Operates as Liverpool Street - Ipswich> \n\
            CANCELLED \n\
                    AM PEAK \n\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
                    PM PEAK \n\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
                    OFF-PEAK \n\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations>")

    @Rule(BlockedRoute(blockage="partial", origin="Diss", destination="Ipswich", intent="advise"))
    def partial_diss_ipswich_adviseB(self):
        return(
            "Freight to be diverted via London \n\
            Monitor inbound freight, liaise with freight York & SSM Cambridge re-holding points")

# C : East Suffolk Junction to Ipswich Working
    @Rule(BlockedRoute(blockage="partial", origin="Diss", destination="Ipswich", intent="schedule"))
    def partial_diss_ipswich_scheduleC(self):
        return(
            "RUNNING AS BOOKED \n\
                    AM PEAK \n\
                        4 per hour: Greater Anglia G/E Services--<> \n\
                    PM PEAK \n\
                        4 per hour: Greater Anglia G/E Services--<> \n\ \n\
                    OFF-PEAK \n\
                        1 per hour: Freight-1 Freight Path each direction per hour-<> \n\
                        4 per hour: Greater Anglia G/E Services--<> \n\
            AMENDED SERVICES <calling pattern> \n\
                    AM PEAK \n\
                        None \n\
                    PM PEAK \n\
                        None \n\
                    OFF-PEAK \n\
                        None \n\
            CANCELLED \n\
                    AM PEAK \n\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
                    PM PEAK \n\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
                    OFF-PEAK \n\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations>")

    @Rule(BlockedRoute(blockage="partial", origin="Diss", destination="Ipswich", intent="advise"))
    def partial_diss_ipswich_adviseC(self):
        return(
            "All 1Pxx services stop addl Stowmarket. \n\
            If 2Wxx term stowmarket…bus service Ipswich-Needham Mkt-Stowmarket.")


###################################################################################
#               Diss to Stowmarket (Full)
###################################################################################
    @Rule(BlockedRoute(blockage="full", origin="Diss", destination="Stowmarket", intent="schedule"))
    def full_diss_stowmarket_schedule(self):
        return(
            "RUNNING AS BOOKED \n\
                    AM PEAK \n\
                        All: Greater Anglia services that are unaffected by this incident--<> \n\
                    PM PEAK \n\
                        All: Greater Anglia services that are unaffected by this incident--<> \n\
                    OFF-PEAK \n\
                        All: Greater Anglia services that are unaffected by this incident--<> \n\
            AMENDED SERVICES <calling pattern> \n\
                    AM PEAK \n\
                        1 per hour: Greater Anglia Cambridge - Ipswich Service--<Operates Cambridge - Bury St Edmunds> \n\
                        1 per hour: Greater Anglia G/E Service--<Operates Bury St Edmunds - Peterborough> \n\
                        2 per hour: Greater Anglia G/E Services--<Operates Liverpool Street - Ipswich> \n\
                    PM PEAK \n\
                        1 per hour: Greater Anglia Cambridge - Ipswich Service--<Operates Cambridge - Bury St Edmunds> \n\
                        1 per hour: Greater Anglia G/E Service--<Operates Bury St Edmunds - Peterborough> \n\
                        2 per hour: Greater Anglia G/E Services--<Operates Liverpool Street - Ipswich> \n\
                    OFF-PEAK \n\
                        1 per hour: Greater Anglia Cambridge - Ipswich Service--<Operates Cambridge - Bury St Edmunds> \n\
                        1 per hour: Greater Anglia G/E Service--<Operates Bury St Edmunds - Peterborough> \n\
                        2 per hour: Greater Anglia G/E Services--<Operates Liverpool Street - Ipswich> \n\
            CANCELLED \n\
                    AM PEAK \n\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
                    PM PEAK \n\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
                    OFF-PEAK \n\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations>"
        )

    @Rule(BlockedRoute(blockage="full", origin="Diss", destination="Stowmarket", intent="advise"))
    def full_diss_stowmarket_advise(self):
        return("Freight to be diverted via London Where possible")

###################################################################################
#               Stowmarket to Ipswich (Full Blockages A/B)
###################################################################################
# A : Haughley Junction Avaliable (GE24)
# B : London End Crossover Avaliable (GE24A)

# A : Haughley Junction Avaliable (GE24)
    @Rule(BlockedRoute(blockage="full", origin="Stowmarket", destination="Ipswich", intent="schedule"))
    def full_stowmarket_ipswich_scheduleA(self):
        return(
            "RUNNING AS BOOKED \n\
                    AM PEAK \n\
                        All: Greater Anglia services that are unaffected by this incident--<> \n\
                    PM PEAK \n\
                        All: Greater Anglia services that are unaffected by this incident--<> \n\
                    OFF-PEAK \n\
                        All: Greater Anglia services that are unaffected by this incident--<> \n\
            AMENDED SERVICES <calling pattern> \n\
                    AM PEAK \n\
                        1 per hour: Greater Anglia Cambridge - Ipswich Service--<Operates Cambridge - Stowmarket> \n\
                        1 per hour: Greater Anglia G/E Service--<Operates Stowmarket - Peterborough> \n\
                        2 per hour: Greater Anglia G/E Services--<Operates Liverpool Street - Ipswich> \n\
                    PM PEAK \n\
                        1 per hour: Greater Anglia Cambridge - Ipswich Service--<Operates Cambridge - Stowmarket> \n\
                        1 per hour: Greater Anglia G/E Service--<Operates Stowmarket - Peterborough> \n\
                        2 per hour: Greater Anglia G/E Services--<Operates Liverpool Street - Ipswich> \n\
                    OFF-PEAK \n\
                        1 per hour: Greater Anglia Cambridge - Ipswich Service--<Operates Cambridge - Stowmarket> \n\
                        1 per hour: Greater Anglia G/E Service--<Operates Stowmarket - Peterborough> \n\
                        2 per hour: Greater Anglia G/E Services--<Operates Liverpool Street - Ipswich> \n\
            CANCELLED \n\
                    AM PEAK \n\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
                    PM PEAK \n\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
                    OFF-PEAK \n\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations>"
        )

    @Rule(BlockedRoute(blockage="full", origin="Stowmarket", destination="Ipswich", intent="advise"))
    def full_stowmarket_ipswich_adviseA(self):
        return("Will require shunting in and out of the loop at Stowmarket")

# B : London End Crossover Avaliable (GE24A)
    @Rule(BlockedRoute(blockage="full", origin="Stowmarket", destination="Ipswich", intent="schedule"))
    def full_stowmarket_ipswich_scheduleB(self):
        return(
            "RUNNING AS BOOKED \n\
                    AM PEAK \n\
                        All: Greater Anglia services that are unaffected by this incident--<> \n\
                    PM PEAK \n\
                        All: Greater Anglia services that are unaffected by this incident--<> \n\
                    OFF-PEAK \n\
                        All: Greater Anglia services that are unaffected by this incident--<> \n\
            AMENDED SERVICES <calling pattern> \n\
                    AM PEAK \n\
                        1 per hour: Greater Anglia Cambridge - Ipswich Service--<Operates Cambridge - Bury St Edmunds> \n\
                        1 per hour: Greater Anglia G/E Service--<Operates Bury St Edmunds - Peterborough> \n\
                        2 per hour: Greater Anglia G/E Services--<Operates Liverpool Street - Ipswich> \n\
                    PM PEAK \n\
                        1 per hour: Greater Anglia Cambridge - Ipswich Service--<Operates Cambridge - Bury St Edmunds> \n\
                        1 per hour: Greater Anglia G/E Service--<Operates Bury St Edmunds - Peterborough> \n\
                        2 per hour: Greater Anglia G/E Services--<Operates Liverpool Street - Ipswich> \n\
                    OFF-PEAK \n\
                        1 per hour: Greater Anglia Cambridge - Ipswich Service--<Operates Cambridge - Bury St Edmunds> \n\
                        1 per hour: Greater Anglia G/E Service--<Operates Bury St Edmunds - Peterborough> \n\
                        2 per hour: Greater Anglia G/E Services--<Operates Liverpool Street - Ipswich> \n\
            CANCELLED \n\
                    AM PEAK \n\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
                    PM PEAK \n\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
                    OFF-PEAK \n\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations>")

    @Rule(BlockedRoute(blockage="full", origin="Stowmarket", destination="Ipswich", intent="advise"))
    def full_stowmarket_ipswich_adviseB(self):
        return("In the event that Stowmarket loop is not accessible and Stowmarket London End crossover can not be used.")


###################################################################################
#               Ipswich to ManningTree (Partial / Full blockage)
###################################################################################
    @Rule(BlockedRoute(blockage="partial", origin="Ipswich", destination="Manningtree", intent="schedule"))
    def partial_ipswich_manningtree_schedule(self):
        return(
            "RUNNING AS BOOKED \n\
                    AM PEAK \n\
                        2 per hour: Greater Anglia G/E Services--<> \n\
                    PM PEAK \n\
                        2 per hour: Greater Anglia G/E Services--<> \n\
                    OFF-PEAK \n\
                        1 per hour: Freight-1 Freight Path each direction per hour-<> \n\
                        2 per hour: Greater Anglia G/E Services--<> \n\
            AMENDED SERVICES <calling pattern> \n\
                    AM PEAK \n\
                        1 per hour: Greater Anglia Colchester Shuttle--<Operates Liverpool Street - Colchester> \n\
                    PM PEAK \n\
                        1 per hour: Greater Anglia Colchester Shuttle--<Operates Liverpool Street - Colchester> \n\
                    OFF-PEAK \n\
                        1 per hour: Greater Anglia Colchester Shuttle--<Operates Liverpool Street - Colchester> \n\
            CANCELLED \n\
                    AM PEAK \n\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
                    PM PEAK \n\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
                    OFF-PEAK \n\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations>")

    @Rule(BlockedRoute(blockage="partial", origin="Ipswich", destination="Manningtree", intent="advise"))
    def partial_ipswich_manningtree_advise(self):
        return("Consider extending services through to Manningtree / ECS to Mistley and return for PM peak & Off peak also where possible.")

    @Rule(BlockedRoute(blockage="full", origin="Ipswich", destination="Manningtree", intent="schedule"))
    def full_ipswich_manningtree_schedule(self):
        return(
            "RUNNING AS BOOKED \n\
                    AM PEAK \n\
                        All: Greater Anglia services that are unaffected by this incident--<> \n\
                    PM PEAK \n\
                        All: Greater Anglia services that are unaffected by this incident--<> \n\
                    OFF-PEAK \n\
                        1 per hour: Freight-1 Freight Path each direction per hour-<> \n\
                        All: Greater Anglia services that are unaffected by this incident--<> \n\
            AMENDED SERVICES <calling pattern> \n\
                    AM PEAK \n\
                        2 per hour: Greater Anglia G/E Services--<Operates Liverpool Street - Mannningtree> \n\
                        2 per hour: Greater Anglia Ipswich Shuttle--<Operates as Norwich - Ipswich Shuttle> \n\
                    PM PEAK \n\
                        2 per hour: Greater Anglia G/E Services--<Operates Liverpool Street - Mannningtree> \n\
                        2 per hour: Greater Anglia Ipswich Shuttle--<Operates as Norwich - Ipswich Shuttle> \n\
                    OFF-PEAK \n\
                        2 per hour: Greater Anglia G/E Services--<Operates Liverpool Street - Mannningtree> \n\
                        2 per hour: Greater Anglia Ipswich Shuttle--<Operates as Norwich - Ipswich Shuttle> \n\
            CANCELLED \n\
                    AM PEAK \n\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
                    PM PEAK \n\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
                    OFF-PEAK \n\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations>")

    @Rule(BlockedRoute(blockage="full", origin="Ipswich", destination="Manningtree", intent="advise"))
    def full_ipswich_manningtree_advise(self):
        return(
            "Shunting to take place at Manningtree North Jn if available. Shunting can also take place at Mistley. Permission should be obtained from Operations \n\
            on-call level 2 to start passenger services from the down main platform (platform 3) at Manningtree if this is necessary. \n\
            Divert freight via BurySt Edmunds & across country up to W9 traffic only")


###################################################################################
#               Manningtree to Colchester (partial / full blockage)
###################################################################################
    @Rule(BlockedRoute(blockage="partial", origin="Manningtree", destination="Colchester", intent="schedule"))
    def partial_manningtree_colchester_schedule(self):
        return(
            "RUNNING AS BOOKED \n\
                    AM PEAK \n\
                        2 per hour: Greater Anglia G/E Services--<> \n\
                    PM PEAK \n\
                        2 per hour: Greater Anglia G/E Services--<> \n\
                    OFF-PEAK \n\
                        1 per hour: Freight-1 Freight Path each direction per hour-<> \n\
                        2 per hour: Greater Anglia G/E Services--<> \n\
            AMENDED SERVICES <calling pattern> \n\
                    AM PEAK \n\
                        1 per hour: Greater Anglia Colchester Shuttle--<Operates Liverpool Street - Colchester> \n\
                    PM PEAK \n\
                        1 per hour: Greater Anglia Colchester Shuttle--<Operates Liverpool Street - Colchester> \n\
                    OFF-PEAK \n\
                        1 per hour: Greater Anglia Colchester Shuttle--<Operates Liverpool Street - Colchester> \n\
            CANCELLED \n\
                    AM PEAK \n\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
                    PM PEAK \n\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
                    OFF-PEAK \n\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations>")

    @Rule(BlockedRoute(blockage="partial", origin="Manningtree", destination="Colchester", intent="advise"))
    def partial_manningtree_colchester_advise(self):
        return(
            "- GriffinWharf may be blocked \n\
             -“Flighting” of trains is preferable to ensure as many trains through the sections as possible.")

    @Rule(BlockedRoute(blockage="full", origin="Manningtree", destination="Colchester", intent="schedule"))
    def full_manningtree_colchester_schedule(self):
        return(
            "RUNNING AS BOOKED \n\
                    AM PEAK \n\
                        All: Greater Anglia services that are unaffected by this incident--<> \n\
                    PM PEAK \n\
                        All: Greater Anglia services that are unaffected by this incident--<> \n\
                    OFF-PEAK \n\
                        All: Greater Anglia services that are unaffected by this incident--<> \n\
            AMENDED SERVICES <calling pattern> \n\
                    AM PEAK \n\
                        2 per hour: Greater Anglia G/E Service--<Operates Norwich - Manningtree> \n\
                        2 per hour: Greater Anglia G/E Services--<Operates Liverpool Street - Colchester> \n\
                    PM PEAK \n\
                        2 per hour: Greater Anglia G/E Service--<Operates Norwich - Manningtree> \n\
                        2 per hour: Greater Anglia G/E Services--<Operates Liverpool Street - Colchester> \n\
                    OFF-PEAK \n\
                        2 per hour: Greater Anglia G/E Service--<Operates Norwich - Manningtree> \n\
                        2 per hour: Greater Anglia G/E Services--<Operates Liverpool Street - Colchester> \n\
            CANCELLED \n\
                    AM PEAK \n\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
                    PM PEAK \n\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
                    OFF-PEAK \n\
                        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations>")

    @Rule(BlockedRoute(blockage="full", origin="Manningtree", destination="Colchester", intent="advise"))
    def full_manningtree_colchester_advise(self):
        return("Divert freight via BurySt Edmunds & across country up to W9 traffic only")

#####














