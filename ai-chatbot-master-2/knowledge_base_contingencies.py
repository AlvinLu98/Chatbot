"""
knowledge_base_contingencies.py

Master's knowledge base for blockage contingencies
"""

from pyknow import *
import chatbot

class BlockedRoute(Fact):
    pass

class Contingencies(KnowledgeEngine):
    @Rule(BlockedRoute(blockage="partial", start="Liverpool Street", to="Stratford", intent="schedule"))
    def partial_block_liverpool_street_stratford_schedule(self):
        chatbot.message(
"RUNNING AS BOOKED \n\
        6 per hour: Greater Anglia G/E Services--<> \n\
        6 per hour: MTR Crossrail Services--<> \n\
    PM PEAK \n\
        6 per hour: Greater Anglia G/E Services--<> \n\
        6 per hour: MTR Crossrail Services--<> \n\
    OFF-PEAK \n\
        6 per hour: Greater Anglia G/E Services--<> \n\
        6 per hour: MTR Crossrail Services--<> \n\
AMENDED SERVICES <calling pattern> \n\
    AM PEAK \n\
        1 per hour: Greater Anglia Braintree Shuttle--<Operates as Braintree - Witham shuttle> \n\
        1 per hour: Greater Anglia Harwich Shuttle--<Operates as Manningtree-Harwich shuttle> \n\
        1 per hour: Greater Anglia Southminster Shuttle--<Operates as Southminster-Wickford shuttle> \n\
        2 per hour: MTR Crossrail Services--<Gidea Park - Stratford Shuttle, then ECS to Gidea Park for next working> \n\
    PM PEAK \n\
        1 per hour: Greater Anglia Braintree Shuttle--<Operates as Braintree - Witham shuttle> \n\
        1 per hour: Greater Anglia Harwich Shuttle--<Operates as Manningtree-Harwich shuttle> \n\
        1 per hour: Greater Anglia Southminster Shuttle--<Operates as Southminster-Wickford shuttle> \n\
        2 per hour: MTR Crossrail Services--<ECS Gidea Park - Stratford to form Stratford - Gidea Park Shuttle> \n\
    OFF-PEAK \n\
        1 per hour: Greater Anglia Braintree Shuttle--<Operates as Braintree - Witham shuttle> \n\
        1 per hour: Greater Anglia Harwich Shuttle--<Operates as Manningtree-Harwich shuttle> \n\
        1 per hour: Greater Anglia Southminster Shuttle--<Operates as Southminster-Wickford shuttle> \n\
CANCELLED \n\
    AM PEAK \n\
        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
        All: MTR Crossrail--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
    PM PEAK \n\
        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
        All: MTR Crossrail--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
    OFF-PEAK \n\
        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
        All: MTR Crossrail--<All other services affected by this problem will be subject to cancellation and short notice alterations>")

    @Rule(BlockedRoute(blockage="partial", start="Liverpool Street", to="Stratford", intent="advise"))
    def partial_block_liverpool_street_stratford_advise(self):
        chatbot.message(
"When diverting mains to electrics etc, priority should always be given to the TOC on the unaffected lines...eg GA for Issues on the electric \
lines & MTR for issues on the main lines \n\n\
Where possible avoid crossing up and down line services over the same Jn’s i.e. if there is a main line blockage between Bethnal Green and \
Bow, up main services to cross back the mains at Wheler Street and down line service to cross to electrics at Bethnal Green West Jn. \
Sub lines not to be used for GE services")

    @Rule(BlockedRoute(blockage="full", start="Liverpool Street", to="Stratford", intent="schedule"))
    def full_block_liverpool_street_stratford_schedule(self):
        chatbot.message(
"RUNNING AS BOOKED \n\
    AM PEAK \n\
        None \n\
    PM PEAK \n\
        None \n\
    OFF-PEAK \n\
        None \n\
AMENDED SERVICES <calling pattern> \n\
    AM PEAK \n\
        1 per hour: Greater Anglia Braintree Shuttle--<Operates as Braintree - Witham shuttle> \n\
        7 per hour: Greater Anglia G/E Services--<To Start & Terminate at Stratford> \n\
        1 per hour: Greater Anglia Harwich Shuttle--<Operates as Manningtree-Harwich shuttle> \n\
        1 per hour: Greater Anglia Southminster Shuttle--<Operates as Southminster-Wickford shuttle> \n\
        8 per hour: MTR Crossrail Services--<To Start & Terminate at Stratford> \n\
    PM PEAK \n\
        1 per hour: Greater Anglia Braintree Shuttle--<Operates as Braintree - Witham shuttle> \n\
        7 per hour: Greater Anglia G/E Services--<To Start & Terminate at Stratford> \n\
        1 per hour: Greater Anglia Harwich Shuttle--<Operates as Manningtree-Harwich shuttle> \n\
        1 per hour: Greater Anglia Southminster Shuttle--<Operates as Southminster-Wickford shuttle> \n\
        8 per hour: MTR Crossrail Services--<To Start & Terminate at Stratford> \n\
    OFF-PEAK \n\
        1 per hour: Greater Anglia Braintree Shuttle--<Operates as Braintree - Witham shuttle> \n\
        7 per hour: Greater Anglia G/E Services--<To Start & Terminate at Stratford> \n\
        1 per hour: Greater Anglia Harwich Shuttle--<Operates as Manningtree-Harwich shuttle> \n\
        1 per hour: Greater Anglia Southminster Shuttle--<Operates as Southminster-Wickford shuttle> \n\
        6 per hour: MTR Crossrail Services--<To Start & Terminate at Stratford> \n\
CANCELLED \n\
    AM PEAK \n\
        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
        All: MTR Crossrail--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
    PM PEAK \n\
        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
        All: MTR Crossrail--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
    OFF-PEAK \n\
        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
        All: MTR Crossrail--<All other services affected by this problem will be subject to cancellation and short notice alterations>")
        
    @Rule(BlockedRoute(blockage="full", start="Liverpool Street", to="Stratford", intent="advise"))
    def full_block_liverpool_street_stratford_advise(self):
        chatbot.message(
"This plan will require a revised traincrew diagrams and constant stepping up of stock at Stratford to avoid Platform 10A to be kept clear \
for freight. \n\
Must have a train crew manager on site at Stratford to do this. Should also consider having a traincrew manager at Gidea Park. \n\n\
GA services to start & terminate in Stratford platforms 9 & 10 off peak and also 10A in AM peak \n\n\
MTR Cross Rail Services to start & terminate in Stratford platforms 5 & 8")

    @Rule(BlockedRoute(blockage="partial", start="Stratford", to="Ilford", intent="schedule"))
    def partial_block_stratford_ilford_schedule(self):
        chatbot.message(
"RUNNING AS BOOKED \n\
    AM PEAK \n\
        6 per hour: Greater Anglia G/E Services--<> \n\
        6 per hour: MTR Crossrail Services--<> \n\
    PM PEAK \n\
        6 per hour: Greater Anglia G/E Services--<> \n\
        6 per hour: MTR Crossrail Services--<> \n\
    OFF-PEAK \n\
        1 per hour: Freight-1 Freight Path each direction per hour- <> \n\
        6 per hour: Greater Anglia G/E Services--<> \n\
        6 per hour: MTR Crossrail Services--<> \n\
AMENDED SERVICES <calling pattern> \n\
    AM PEAK \n\
        1 per hour: Greater Anglia Braintree Shuttle--<Operates as Braintree - Witham shuttle> \n\
        1 per hour: Greater Anglia Harwich Shuttle--<Operates as Manningtree-Harwich shuttle> \n\
        1 per hour: Greater Anglia Southminster Shuttle--<Operates as Southminster-Wickford shuttle> \n\
    PM PEAK \n\
        1 per hour: Greater Anglia Braintree Shuttle--<Operates as Braintree - Witham shuttle> \n\
        1 per hour: Greater Anglia Harwich Shuttle--<Operates as Manningtree-Harwich shuttle> \n\
        1 per hour: Greater Anglia Southminster Shuttle--<Operates as Southminster-Wickford shuttle> \n\
    OFF-PEAK \n\
        1 per hour: Greater Anglia Braintree Shuttle--<Operates as Braintree - Witham shuttle> \n\
        1 per hour: Greater Anglia Harwich Shuttle--<Operates as Manningtree-Harwich shuttle> \n\
        1 per hour: Greater Anglia Southminster Shuttle--<Operates as Southminster-Wickford shuttle> \n\
CANCELLED \n\
    AM PEAK \n\
        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
        All: MTR Crossrail--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
    PM PEAK \n\
        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
        All: MTR Crossrail--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
    OFF-PEAK \n\
        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
        All: MTR Crossrail--<All other services affected by this problem will be subject to cancellation and short notice alterations>")
    
    @Rule(BlockedRoute(blockage="partial", start="Stratford", to="Ilford", intent="advise"))
    def partial_block_stratford_ilford_advise(self):
        chatbot.message(
"When diverting mains to electrics etc, priority should always be given to the TOC on the unaffected lines...eg GA for Issues on the electric \
lines & MTR for issues on the main lines \n\n\
For those 2Wxx services running with reduced stops the principles are: Keep booked 2Wxx headcodes. This best for workload on \
signaller, controllers and customer service. \n\
Down road - Trains running with reduced stops as per the plan - xx10, xx30, xx50 ex Liverpool St, Trains running all stations as booked \
xx00, xx20, xx40 ex Liverpool St. \n\
Up road – Trains running with reduced stops as per the plan - xx04, xx24, xx44 ex Shenfield, Trains running all stations as booked xx14, \
xx34, xx54 ex Shenfield.")

    @Rule(BlockedRoute(blockage="full", start="Stratford", to="Ilford", intent="schedule"))
    def full_block_stratford_ilford_schedule(self):
        chatbot.message(
"RUNNING AS BOOKED \n\
    AM PEAK \n\
        None \n\
    PM PEAK \n\
        None \n\
    OFF-PEAK \n\
        None \n\
AMENDED SERVICES <calling pattern> \n\
    AM PEAK \n\
        1 per hour: Greater Anglia Braintree Shuttle--<Operates as Braintree - Witham shuttle> \n\
        3 per hour: Greater Anglia G/E Service--<To Start & Terminate at Shenfield> \n\
        3 per hour: Greater Anglia G/E Services--<To Start & Terminate at Ilford> \n\
        1 per hour: Greater Anglia Harwich Shuttle--<Operates as Manningtree-Harwich shuttle> \n\
        1 per hour: Greater Anglia Southminster Shuttle--<Operates as Southminster-Wickford shuttle> \n\
        4 per hour: MTR Crossrail Services--<To Start & Terminate at Ilford> \n\
    PM PEAK \n\
        1 per hour: Greater Anglia Braintree Shuttle--<Operates as Braintree - Witham shuttle> \n\
        3 per hour: Greater Anglia G/E Service--<To Start & Terminate at Shenfield> \n\
        3 per hour: Greater Anglia G/E Services--<To Start & Terminate at Ilford> \n\
        1 per hour: Greater Anglia Harwich Shuttle--<Operates as Manningtree-Harwich shuttle> \n\
        1 per hour: Greater Anglia Southminster Shuttle--<Operates as Southminster-Wickford shuttle> \n\
        4 per hour: MTR Crossrail Services--<To Start & Terminate at Ilford> \n\
    OFF-PEAK \n\
        1 per hour: Greater Anglia Braintree Shuttle--<Operates as Braintree - Witham shuttle> \n\
        3 per hour: Greater Anglia G/E Service--<To Start & Terminate at Shenfield> \n\
        3 per hour: Greater Anglia G/E Services--<To Start & Terminate at Ilford> \n\
        1 per hour: Greater Anglia Harwich Shuttle--<Operates as Manningtree-Harwich shuttle> \n\
        1 per hour: Greater Anglia Southminster Shuttle--<Operates as Southminster-Wickford shuttle> \n\
        4 per hour: MTR Crossrail Services--<To Start & Terminate at Ilford> \n\
CANCELLED \n\
    AM PEAK \n\
        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
        All: MTR Crossrail--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
    PM PEAK \n\
        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
        All: MTR Crossrail--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
    OFF-PEAK \n\
        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
        All: MTR Crossrail--<All other services affected by this problem will be subject to cancellation and short notice alterations>")

    @Rule(BlockedRoute(blockage="full", start="Stratford", to="Ilford", intent="advise"))
    def full_block_stratford_ilford_advise(self):
        chatbot.message(
"This plan will require a revised traincrew diagrams and constant stepping up of stock at Ilford / Shenfield to avoid platform congestion \
This will also involve stepping up of stocks and crew. Must have a train crew manager on site at Ilford to do this. Should also consider \
having a traincrew manager at GideaPark). \n\n\
Divert freight via T&H where possible… divert GE freight via Bury St Edmunds & across country \n\
Block on freight to adjoining routes \n\n\
1Kxx Services Southend Victoria - Ilford MUST be 8 car units.")

    @Rule(BlockedRoute(blockage="partial", start="Ilford", to="Gidea Park", intent="schedule"))
    def partial_block_ilford_gidea_park_schedule(self):
        chatbot.message(
"RUNNING AS BOOKED \n\
    AM PEAK \n\
        6 per hour: Greater Anglia G/E Services--<> \n\
        6 per hour: MTR Crossrail Services--<> \n\
    PM PEAK \n\
        6 per hour: Greater Anglia G/E Services--<> \n\
        6 per hour: MTR Crossrail Services--<> \n\
    OFF-PEAK \n\
        1 per hour: Freight-1 Freight Path each direction per hour- <> \n\
        6 per hour: Greater Anglia G/E Services--<> \n\
        6 per hour: MTR Crossrail Services--<> \n\
AMENDED SERVICES <calling pattern> \n\
    AM PEAK \n\
        1 per hour: Greater Anglia Braintree Shuttle--<Operates as Braintree - Witham shuttle> \n\
        1 per hour: Greater Anglia Harwich Shuttle--<Operates as Manningtree-Harwich shuttle> \n\
        1 per hour: Greater Anglia Southminster Shuttle--<Operates as Southminster-Wickford shuttle> \n\
    PM PEAK \n\
        1 per hour: Greater Anglia Braintree Shuttle--<Operates as Braintree - Witham shuttle> \n\
        1 per hour: Greater Anglia Harwich Shuttle--<Operates as Manningtree-Harwich shuttle> \n\
        1 per hour: Greater Anglia Southminster Shuttle--<Operates as Southminster-Wickford shuttle> \n\
    OFF-PEAK \n\
        1 per hour: Greater Anglia Braintree Shuttle--<Operates as Braintree - Witham shuttle> \n\
        1 per hour: Greater Anglia Harwich Shuttle--<Operates as Manningtree-Harwich shuttle> \n\
        1 per hour: Greater Anglia Southminster Shuttle--<Operates as Southminster-Wickford shuttle> \n\
CANCELLED \n\
    AM PEAK \n\
        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
        All: MTR Crossrail--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
    PM PEAK \n\
        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
        All: MTR Crossrail--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
    OFF-PEAK \n\
        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
        All: MTR Crossrail--<All other services affected by this problem will be subject to cancellation and short notice alterations>")

    @Rule(BlockedRoute(blockage="partial", start="Ilford", to="Gidea Park", intent="advise"))
    def partial_block_ilford_gidea_park_advise(self):
        chatbot.message(
"When diverting mains to electrics etc, priority should always be given to the TOC on the unaffected lines...eg GA for Issues on the electric \
lines & MTR for issues on the main lines \n\n\
For those 2Wxx services running with reduced stops the principles are: Keep booked 2Wxx headcodes. This best for workload on \
signaller, controllers and customer service. \n\n\
Signaller and Controller Instructions: \n\
If EL’s are blocked east of Chadwell Heath and services are diverted DML, Crossrail would like to run additional services to Chadwell Heath where \
resources and capacity are available.")

    @Rule(BlockedRoute(blockage="full", start="Ilford", to="Gidea Park", intent="schedule"))
    def full_block_ilford_gidea_park_schedule(self):
        chatbot.message(
"RUNNING AS BOOKED \n\
    AM PEAK\n\
        None \n\
    PM PEAK \n\
        None \n\
    OFF-PEAK \n\
        None \n\
AMENDED SERVICES <calling pattern> \n\
    AM PEAK \n\
        1 per hour: Greater Anglia Braintree Shuttle--<Operates as Braintree - Witham shuttle> \n\
        1 per hour: Greater Anglia Colchester Shuttle--<Operates as Norwich - Colchester Shuttle> \n\
        8 per hour: Greater Anglia G/E Services--<To Start & Terminate at Shenfield.> \n\
        1 per hour: Greater Anglia Harwich Shuttle--< Operates as Manningtree-Harwich shuttle> \n\
        1 per hour: Greater Anglia Southminster Shuttle--<Operates as Southminster-Wickford shuttle> \n\
        2 per hour: MTR Crossrail Service--<Operates Shenfield - Gidea Park> \n\
        4 per hour: MTR Crossrail Services--<Operates Liverpool Street - Ilford> \n\
    PM PEAK \n\
        1 per hour: Greater Anglia Braintree Shuttle--<Operates as Braintree - Witham shuttle> \n\
        1 per hour: Greater Anglia Colchester Shuttle--<Operates as Norwich - Colchester Shuttle> \n\
        8 per hour: Greater Anglia G/E Services--<To Start & Terminate at Shenfield.> \n\
        1 per hour: Greater Anglia Harwich Shuttle--< Operates as Manningtree-Harwich shuttle> \n\
        1 per hour: Greater Anglia Southminster Shuttle--<Operates as Southminster-Wickford shuttle> \n\
        2 per hour: MTR Crossrail Service--<Operates Shenfield - Gidea Park> \n\
        4 per hour: MTR Crossrail Services--<Operates Liverpool Street - Ilford> \n\
    OFF-PEAK \n\
        1 per hour: Greater Anglia Braintree Shuttle--<Operates as Braintree - Witham shuttle> \n\
        1 per hour: Greater Anglia Colchester Shuttle--<Operates as Norwich - Colchester Shuttle> \n\
        8 per hour: Greater Anglia G/E Services--<To Start & Terminate at Shenfield.> \n\
        1 per hour: Greater Anglia Harwich Shuttle--< Operates as Manningtree-Harwich shuttle> \n\
        1 per hour: Greater Anglia Southminster Shuttle--<Operates as Southminster-Wickford shuttle> \n\
        2 per hour: MTR Crossrail Service--<Operates Shenfield - Gidea Park> \n\
        4 per hour: MTR Crossrail Services--<Operates Liverpool Street - Ilford> \n\
CANCELLED \n\
    AM PEAK \n\
        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
        All: MTR Crossrail--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
    PM PEAK \n\
        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
        All: MTR Crossrail--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
    OFF-PEAK \n\
        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
        All: MTR Crossrail--<All other services affected by this problem will be subject to cancellation and short notice alterations>")

    @Rule(BlockedRoute(blockage="full", start="Ilford", to="Gidea Park", intent="advise"))
    def full_block_ilford_gidea_park_advise(self):
        chatbot.message(
"This plan will require a revised traincrew diagrams and constant stepping up of stock at Ilford / Shenfield to avoid platform congestion \
This will also involve stepping up of stocks and crew. Must have a train crew manager on site at Ilford to do this. Should also consider \
having a traincrew managers at GideaPark Shenfield and Chadwell Heath) \n\n\
Freight Services to be diverted cross country where possible")

    @Rule(BlockedRoute(blockage="partial", start="Gidea Park", to="Shenfield", intent="schedule"))
    def partial_block_gidea_park_shenfield_schedule(self):
        chatbot.message(
"RUNNING AS BOOKED \n\
    AM PEAK \n\
        6 per hour: Greater Anglia G/E Services--<> \n\
        3 per hour: MTR Crossrail Services--<> \n\
    PM PEAK \n\
        6 per hour: Greater Anglia G/E Services--<> \n\
        3 per hour: MTR Crossrail Services--<> \n\
    OFF-PEAK \n\
        1 per hour: Freight-1 Freight Path each direction per hour- <> \n\
        6 per hour: Greater Anglia G/E Services--<> \n\
        3 per hour: MTR Crossrail Services--<> \n\
AMENDED SERVICES <calling pattern> \n\
    AM PEAK \n\
        1 per hour: Greater Anglia Braintree Shuttle--<Operates as Braintree - Witham shuttle> \n\
        1 per hour: Greater Anglia Harwich Shuttle--<Operates as Manningtree-Harwich shuttle> \n\
        1 per hour: Greater Anglia Southminster Shuttle--<Operates as Southminster-Wickford shuttle> \n\
        3 per hour: MTR Crossrail Service--<Operates as Liverpool St - Gidea Park Shuttle.> \n\
    PM PEAK \n\
        1 per hour: Greater Anglia Braintree Shuttle--<Operates as Braintree - Witham shuttle> \n\
        1 per hour: Greater Anglia Harwich Shuttle--<Operates as Manningtree-Harwich shuttle> \n\
        1 per hour: Greater Anglia Southminster Shuttle--<Operates as Southminster-Wickford shuttle> \n\
        3 per hour: MTR Crossrail Service--<Operates as Liverpool St - Gidea Park Shuttle.> \n\
    OFF-PEAK \n\
        1 per hour: Greater Anglia Braintree Shuttle--<Operates as Braintree - Witham shuttle> \n\
        1 per hour: Greater Anglia Harwich Shuttle--<Operates as Manningtree-Harwich shuttle> \n\
        1 per hour: Greater Anglia Southminster Shuttle--<Operates as Southminster-Wickford shuttle> \n\
        3 per hour: MTR Crossrail Service--<Operates as Liverpool St - Gidea Park Shuttle.> \n\
CANCELLED \n\
    AM PEAK \n\
        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
        All: MTR Crossrail--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
    PM PEAK \n\
        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
        All: MTR Crossrail--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
    OFF-PEAK \n\
        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
        All: MTR Crossrail--<All other services affected by this problem will be subject to cancellation and short notice alterations>")

    @Rule(BlockedRoute(blockage="partial", start="Gidea Park", to="Shenfield", intent="advise"))
    def partial_block_gidea_park_shenfield_advise(self):
        chatbot.message(
"When diverting mains to electrics etc, priority should always be given to the TOC on the unaffected lines...eg GA for Issues on the electric \
lines & MTR for issues on the main lines")


    @Rule(BlockedRoute(blockage="full", start="Gidea Park", to="Shenfield", intent="schedule"))
    def full_block_gidea_park_shenfield_schedule(self):
        chatbot.message(
"RUNNING AS BOOKED \n\
    AM PEAK \n\
        None \n\
    PM PEAK \n\
        None \n\
    OFF-PEAK \n\
        None \n\
AMENDED SERVICES <calling pattern> \n\
    AM PEAK \n\
        1 per hour: Greater Anglia Braintree Shuttle--<Operates as Braintree - Witham shuttle> \n\
        1 per hour: Greater Anglia Colchester Shuttle--<Operates as Norwich - Colchester Shuttle> \n\
        8 per hour: Greater Anglia G/E Services--<To Start & Terminate at Shenfield> \n\
        1 per hour: Greater Anglia Harwich Shuttle--<Operates as Manningtree-Harwich shuttle> \n\
        1 per hour: Greater Anglia Southminster Shuttle--<Operates as Southminster-Wickford shuttle> \n\
        6 per hour: MTR Crossrail Services--<Operates Liverpool Street - Gidea Park> \n\
    PM PEAK \n\
        1 per hour: Greater Anglia Braintree Shuttle--<Operates as Braintree - Witham shuttle> \n\
        1 per hour: Greater Anglia Colchester Shuttle--<Operates as Norwich - Colchester Shuttle> \n\
        8 per hour: Greater Anglia G/E Services--<To Start & Terminate at Shenfield> \n\
        1 per hour: Greater Anglia Harwich Shuttle--<Operates as Manningtree-Harwich shuttle> \n\
        1 per hour: Greater Anglia Southminster Shuttle--<Operates as Southminster-Wickford shuttle> \n\
        6 per hour: MTR Crossrail Services--<Operates Liverpool Street - Gidea Park> \n\
    OFF-PEAK \n\
        1 per hour: Greater Anglia Braintree Shuttle--<Operates as Braintree - Witham shuttle> \n\
        1 per hour: Greater Anglia Colchester Shuttle--<Operates as Norwich - Colchester Shuttle> \n\
        8 per hour: Greater Anglia G/E Services--<To Start & Terminate at Shenfield> \n\
        1 per hour: Greater Anglia Harwich Shuttle--<Operates as Manningtree-Harwich shuttle> \n\
        1 per hour: Greater Anglia Southminster Shuttle--<Operates as Southminster-Wickford shuttle> \n\
        6 per hour: MTR Crossrail Services--<Operates Liverpool Street - Gidea Park> \n\
CANCELLED \n\
    AM PEAK \n\
        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
        All: MTR Crossrail--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
    PM PEAK \n\
        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
        All: MTR Crossrail--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
    OFF-PEAK \n\
        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
        All: MTR Crossrail--<All other services affected by this problem will be subject to cancellation and short notice alterations>")

    @Rule(BlockedRoute(blockage="full", start="Gidea Park", to="Shenfield", intent="advise"))
    def full_block_gidea_park_shenfield_advise(self):
        chatbot.message(
"This plan will require a revised traincrew diagrams and constant stepping up of stock at Ilford / Shenfield to avoid platform congestion \
This will involve stepping up of stocks and crew. Must have a train crew manager on site at Ilford to do this. Should also consider having \
a traincrew managers at GideaPark and Shenfield)")

    @Rule(BlockedRoute(blockage="partial", start="Shenfield", to="Church Lane", intent="schedule"))
    def partial_block_shenfield_Church_Lane_schedule(self):
        chatbot.message(
"RUNNING AS BOOKED \n\
    AM PEAK \n\
    2 per hour: Greater Anglia G/E Services--<> \n\
    PM PEAK \n\
    2 per hour: Greater Anglia G/E Services--<> \n\
    OFF-PEAK \n\
    1 per hour: Freight-1 Freight Path each direction per hour- <> \n\
    2 per hour: Greater Anglia G/E Services--< \n\
AMENDED SERVICES <calling pattern> \n\
    AM PEAK \n\
        1 per hour: Greater Anglia Braintree Shuttle--<Operates as Braintree - Witham shuttle> \n\
        1 per hour: Greater Anglia Harwich Shuttle--<Operates as Manningtree-Harwich shuttle> \n\
        1 per hour: Greater Anglia Norwich Shuttle--<Operates as Norwich - Colchester shuttle> \n\
    PM PEAK \n\
        1 per hour: Greater Anglia Braintree Shuttle--<Operates as Braintree - Witham shuttle> \n\
        1 per hour: Greater Anglia Harwich Shuttle--<Operates as Manningtree-Harwich shuttle> \n\
        1 per hour: Greater Anglia Norwich Shuttle--<Operates as Norwich - Colchester shuttle> \n\
    OFF-PEAK \n\
        1 per hour: Greater Anglia Braintree Shuttle--<Operates as Braintree - Witham shuttle> \n\
        1 per hour: Greater Anglia Harwich Shuttle--<Operates as Manningtree-Harwich shuttle> \n\
        1 per hour: Greater Anglia Norwich Shuttle--<Operates as Norwich - Colchester shuttle> \n\
CANCELLED \n\
    AM PEAK \n\
        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
    PM PEAK \n\
        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
    OFF-PEAK \n\
        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations>")

    @Rule(BlockedRoute(blockage="partial", start="Shenfield", to="Church Lane", intent="advise"))
    def partial_block_shenfield_Church_Lane_advise(self):
        chatbot.message(
"Witham - Braintree shuttle to be used where resources allow...consider splitting an 8 car unit from elsewhere to provide a 4 car for the shuttle.")
            
    @Rule(BlockedRoute(blockage="full", start="Chelmsford", to="Witham", intent="schedule"))
    def full_block_chelmsford_witham_schedule(self):
        chatbot.message(
"RUNNING AS BOOKED \n\
    AM PEAK \n\
        All: Greater Anglia services that are unaffected by this incident--<> \n\
    PM PEAK \n\
        All: Greater Anglia services that are unaffected by this incident--<> \n\
    OFF-PEAK \n\
        All: Greater Anglia services that are unaffected by this incident--<> \n\
AMENDED SERVICES <calling pattern> \n\
    AM PEAK \n\
        1 per hour: Greater Anglia Braintree Shuttle--<Operates as Braintree - Witham shuttle> \n\
        1 per hour: Greater Anglia Colchester Shuttle--<Operates as Norwich - Colchester Shuttle> \n\
        2 per hour: Greater Anglia G/E Service--<To Start & Terminate at Witham> \n\
        2 per hour: Greater Anglia G/E Services--<Operates Liverpool Street - Chelmsford> \n\
    PM PEAK \n\
        1 per hour: Greater Anglia Braintree Shuttle--<Operates as Braintree - Witham shuttle> \n\
        1 per hour: Greater Anglia Colchester Shuttle--<Operates as Norwich - Colchester Shuttle> \n\
        2 per hour: Greater Anglia G/E Service--<To Start & Terminate at Witham> \n\
        2 per hour: Greater Anglia G/E Services--<Operates Liverpool Street - Chelmsford> \n\
    OFF-PEAK \n\
        1 per hour: Greater Anglia Braintree Shuttle--<Operates as Braintree - Witham shuttle> \n\
        1 per hour: Greater Anglia Colchester Shuttle--<Operates as Norwich - Colchester Shuttle> \n\
        2 per hour: Greater Anglia G/E Service--<To Start & Terminate at Witham> \n\
        2 per hour: Greater Anglia G/E Services--<Operates Liverpool Street - Chelmsford> \n\
CANCELLED \n\
    AM PEAK \n\
        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
    PM PEAK \n\
        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations> \n\
    OFF-PEAK \n\
        All: Greater Anglia--<All other services affected by this problem will be subject to cancellation and short notice alterations>")

    @Rule(BlockedRoute(blockage="full", start="Chelmsford", to="Witham", intent="advise"))
    def full_block_chelmsford_witham_advise(self):
        chatbot.message(
"INSTRUCTIONS TO CONTROLLERS: \n\
Must have train crew managers on site at Witham & Chelmsford to do this. \n\n\
Divert freight via BurySt Edmunds & across country up to W9 traffic only")

def respond(information_tokens):
    engine = Contingencies()
    engine.reset()
    engine.declare(BlockedRoute(blockage=information_tokens[0], start=information_tokens[1], to=information_tokens[2], intent=information_tokens[3]))
    engine.run()