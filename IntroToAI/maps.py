from functions import UndirectedGraph

# Romania map (from AIMA) as an undirected graph
romania_map = UndirectedGraph(dict(
    Arad=dict(Zerind=75, Sibiu=140, Timisoara=118),
    Bucharest=dict(Urziceni=85, Pitesti=101, Giurgiu=90, Fagaras=211),
    Craiova=dict(Drobeta=120, Rimnicu=146, Pitesti=138),
    Drobeta=dict(Mehadia=75),
    Eforie=dict(Hirsova=86),
    Fagaras=dict(Sibiu=99),
    Hirsova=dict(Urziceni=98),
    Iasi=dict(Vaslui=92, Neamt=87),
    Lugoj=dict(Timisoara=111, Mehadia=70),
    Oradea=dict(Zerind=71, Sibiu=151),
    Pitesti=dict(Rimnicu=97),
    Rimnicu=dict(Sibiu=80),
    Urziceni=dict(Vaslui=142)
))

# Set locations for straight-line distance (Euclidean) heuristic.
romania_map.locations = dict(
    Arad=(91, 492), Bucharest=(400, 327), Craiova=(253, 288),
    Drobeta=(165, 299), Eforie=(562, 293), Fagaras=(305, 449),
    Giurgiu=(375, 270), Hirsova=(534, 350), Iasi=(473, 506),
    Lugoj=(165, 379), Mehadia=(168, 339), Neamt=(406, 537),
    Oradea=(131, 571), Pitesti=(320, 368), Rimnicu=(233, 410),
    Sibiu=(207, 457), Timisoara=(94, 410), Urziceni=(456, 350),
    Vaslui=(509, 444), Zerind=(108, 531)
)

# Fantasy World Map with 15 nodes

fantasy_map = UndirectedGraph(dict(
    Aldor=dict(Brimstone=70, Celestia=60, Ironwood=30),
    Brimstone=dict(Draconis=80, Frosthelm=50),
    Celestia=dict(Eldoria=70, Griffinhold=40),
    Draconis=dict(Frosthelm=60, Kingsport=90),
    Eldoria=dict(Lunaris=50, Mystvale=40),
    Frosthelm=dict(Griffinhold=55, Oakhaven=80),
    Griffinhold=dict(Helios=65),
    Helios=dict(Ironwood=45, Kingsport=70, Novaria=60),
    Ironwood=dict(Mystvale=50, Ravenmoor=80),
    Kingsport=dict(Lunaris=60, Oakhaven=75),
    Lunaris=dict(Mystvale=45, Novaria=85),
    Mystvale=dict(Oakhaven=65),
    Novaria=dict(Ravenmoor=70),
    Oakhaven=dict(Ravenmoor=60)
))
# The UndirectedGraph class will ensure that reverse edges are added automatically.

# Set locations (x, y coordinates) for each node.
fantasy_map.locations = dict(
    Aldor=(50, 400),
    Brimstone=(120, 420),
    Celestia=(80, 360),
    Draconis=(150, 460),
    Eldoria=(100, 320),
    Frosthelm=(180, 480),
    Griffinhold=(60, 340),
    Helios=(200, 300),
    Ironwood=(40, 380),
    Kingsport=(220, 310),
    Lunaris=(130, 280),
    Mystvale=(90, 260),
    Novaria=(210, 260),
    Oakhaven=(170, 240),
    Ravenmoor=(50, 200)
)
