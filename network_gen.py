#! /usr/bin/python3

# ─── IMPORTING THE LIBRARIES ────────────────────────────────────────────────────
from easygui import fileopenbox 
import sys, time, colored, threading
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from concurrent.futures import ThreadPoolExecutor as TPE
from colored import stylize
# ────────────────────────────────────────────────────────────────────────────────
# ──────────────────────────────── CODE ──────────────────────────────────────────
# ─── JUST A BUFFERING ANIMATION ─────────────────────────────────────────────────
def animate():
    global go
    chars = "/—\|" 
    while go:
        for char in chars:
            sys.stdout.write('\r'+'loading...'+char)
            time.sleep(.1)
            sys.stdout.flush()
    sys.stdout.flush()
    print('\n') 

# ─── SELECTING ONLY UNIPROTKB DATABASE AND HUMAN PROTEINS DATA ──────────────────
def search_mitab(mitabfile):
    global go
    global list_int
    with open(mitabfile) as f:
        for line in f:
            v = line.split('\t')
            if v[0].find('uniprotkb:') > -1 and v[1].find('uniprotkb:') > -1:
                tax1 = v[9].replace('taxid:','')
                tax2 = v[10].replace('taxid:','')
                if tax1.lower().find('human') > -1 and tax2.lower().find('human') > -1: # ! 9606 == Homo Sapiens & Human
                    int1 = v[0].replace('uniprotkb:','')
                    int2 = v[1].replace('uniprotkb:','')
                    texp = v[6].replace('psi-mi:','')
                    cexp = v[11].replace('psi-mi:','')
                    pint = (int1, int2, texp, tax1, tax2, cexp)
                    list_int.append(pint)
    go = False

# ─── BETTER VISUALIZATION USING PANDAS ──────────────────────────────────────────
def better_vis(list_int):
    int1, int2, tax1, tax2, texp, cexp = (list() for y in range(6))
    for x in list_int:
        int1.append(x[0])
        int2.append(x[1])
        texp.append(x[2])
        tax1.append(x[3])
        tax2.append(x[4])
        cexp.append(x[5])
        
    df = {'int1' : int1, 'int2' : int2, 'tax1' : tax1, 'tax2' : tax2, 'texp' : texp, 'cexp' : cexp}
    index = pd.MultiIndex.from_arrays(list(df.values()), names=(df.keys()))
    dff = pd.DataFrame(df)
    dff.to_csv('Hu_Int.csv')
    print(dff)
    print('\nComplete table in \'Hu_Int.csv\' file')

# ─── GETTING THE INTERACTIONS ───────────────────────────────────────────────────
def get_inter(list_int):
    dint = dict()
    for pint in list_int: 
        # ─── HERE THE INTERACTORS ARE SELECTED ───────────────────────────
        g1 = pint[0]
        g2 = pint[1]
        # ─────────────────────────────────────────────────────────────────
        gi = [g1, g2]
        gi.sort()
        dint[(gi[0],gi[1])] = dint.get((gi[0],gi[1]),0) + 1
         
    return dint

# ─── PLOTTING THE GRAPH ─────────────────────────────────────────────────────────
def plot_graph(ints):
    g = nx.Graph()
    g.add_edges_from(ints)
    nx.draw(g)
    plt.show()
    print('Number of nodes: ', g.number_of_nodes())
    print('Number of edges: ', g.number_of_edges())

# ─── CALCULATING THE LENGTH OF THE SHORTEST PATH AND SELECT ONLY THOSE UNDER CUTOFF
def distance_reg(ints, target, thresh):
    g = nx.Graph()
    g.add_edges_from(ints)
    G = nx.Graph()
    G.add_node(target)
    for y in g.nodes():
        if y == target: continue
        try:
            p = nx.shortest_path_length(g, target = target, source = y)
            if p > thresh: continue
            G.add_node(y)
        except: continue
        
    for y in g.edges():
        if y[0] in G.nodes() and y[1] in G.nodes():
            G.add_edge(y[0], y[1])
    return G

# ─── PRINT BETWEENESS CENTRALITY ────────────────────────────────────────────────
def print_between(targets):
    global go
    BT = nx.betweenness_centrality(g)
    go = False
    time.sleep(0.5)
    for target in targets: print(stylize('Betweeness Centrality of {a}: '.format(a = target), colored.fg(1)), str(BT[target])[:])
    print('\n─────────────────────────────────────────\n')
    
# ─── PRINT CLUSTERING COEFFICIENT ───────────────────────────────────────────────
# ─── PRINT DEGREE ───────────────────────────────────────────────────────────────
def print_rest(target):
    print(stylize('Clustering of {a}: '.format(a = target), colored.fg(1)), str(nx.clustering(g, nodes = target))[:])
    print(stylize('Degree of {a}: '.format(a = target), colored.fg(1)), nx.degree(g, nbunch = target))
    print('\n─────────────────────────────────────────\n')    

# ────────────────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print('',\
stylize('███╗   ██╗███████╗████████╗██╗    ██╗ ██████╗ ██████╗ ██╗  ██╗ '                               ,colored.fg(2)), 
stylize('████╗  ██║██╔════╝╚══██╔══╝██║    ██║██╔═══██╗██╔══██╗██║ ██╔╝                                ',colored.fg(2)),
stylize('██╔██╗ ██║█████╗     ██║   ██║ █╗ ██║██║   ██║██████╔╝█████╔╝                                 ',colored.fg(2)),
stylize('██║╚██╗██║██╔══╝     ██║   ██║███╗██║██║   ██║██╔══██╗██╔═██╗                                 ',colored.fg(2)),
stylize('██║ ╚████║███████╗   ██║   ╚███╔███╔╝╚██████╔╝██║  ██║██║  ██╗                                ',colored.fg(2)),
stylize('╚═╝  ╚═══╝╚══════╝   ╚═╝    ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝                                ',colored.fg(2)),
stylize(''                                                                                              ,colored.fg(2)),
stylize(' ██████╗ ███████╗███╗   ██╗███████╗██████╗  █████╗ ████████╗ ██████╗ ██████╗                  ',colored.fg(2)),
stylize('██╔════╝ ██╔════╝████╗  ██║██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗                 ',colored.fg(2)),
stylize('██║  ███╗█████╗  ██╔██╗ ██║█████╗  ██████╔╝███████║   ██║   ██║   ██║██████╔╝                 ',colored.fg(2)),
stylize('██║   ██║██╔══╝  ██║╚██╗██║██╔══╝  ██╔══██╗██╔══██║   ██║   ██║   ██║██╔══██╗                 ',colored.fg(2)),
stylize('╚██████╔╝███████╗██║ ╚████║███████╗██║  ██║██║  ██║   ██║   ╚██████╔╝██║  ██║                 ',colored.fg(2)),
stylize(' ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝                 ',colored.fg(2)),
stylize(''                                                                                              ,colored.fg(2)),
stylize(' █████╗ ███╗   ██╗██████╗      █████╗ ███╗   ██╗ █████╗ ██╗  ██╗   ██╗███████╗███████╗██████╗ ',colored.fg(2)),
stylize('██╔══██╗████╗  ██║██╔══██╗    ██╔══██╗████╗  ██║██╔══██╗██║  ╚██╗ ██╔╝╚══███╔╝██╔════╝██╔══██╗',colored.fg(2)),
stylize('███████║██╔██╗ ██║██║  ██║    ███████║██╔██╗ ██║███████║██║   ╚████╔╝   ███╔╝ █████╗  ██████╔╝',colored.fg(2)),
stylize('██╔══██║██║╚██╗██║██║  ██║    ██╔══██║██║╚██╗██║██╔══██║██║    ╚██╔╝   ███╔╝  ██╔══╝  ██╔══██╗',colored.fg(2)),
stylize('██║  ██║██║ ╚████║██████╔╝    ██║  ██║██║ ╚████║██║  ██║███████╗██║   ███████║███████╗██║  ██║',colored.fg(2)),
stylize('╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝     ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═╝   ╚══════╝╚══════╝╚═╝  ╚═╝',colored.fg(2)), 


'\n\tBy: Andrea Rubbi\n', sep = '\n\t')
    # ─── READING MITAB FILE FILTERING HUMAN AND UNIPROT DATA ────────────────────────
    go = True
    list_int = list()
    if len(sys.argv) < 2:
        print('\n─────────────────────────────────────────\n')
        print('Select the file with interactions:')
        mitabfile = fileopenbox(title = 'Mitabfile')
        print('You have selected: {a}'.format(a = mitabfile))
    else: mitabfile = sys.argv[1]
    e = TPE(max_workers = 2)
    e.submit(search_mitab, mitabfile)
    e.submit(animate())
    # ────────────────────────────────────────────────────────────────────────────────
    if input(stylize('Would you like to see the interactions?\n(y/n): ', colored.fg(2))) == 'y': better_vis(list_int)
    print('\n─────────────────────────────────────────\n')
    ints = get_inter(list_int)
    if input(stylize('Would you like to see the graph?(only small files)\n(y/n): ', colored.fg(2))) == 'y': plot_graph(ints)
    print('\n─────────────────────────────────────────\n')
    targets, nodes, edges = (list(), set(), set())
    # ────────────────────────────────────────────────────────────────────────────────
    # ─── ASKING FOR TARGETS TO ANALYSE AND SELECTING A DISTANCE THRESHOLD FROM THEM ─
    while True:
        target = input(stylize('Insert a target ID(blank to stop): ', colored.fg(2)))
        if target == '': break
        targets.append(target)
    thres = int(input(stylize('Select a threshold\nthreshold = ', colored.fg(2))))
    # ────────────────────────────────────────────────────────────────────────────────
    p = threading.Thread(target = animate)
    go = True
    p.daemon = True
    p.start()
    # ─── FOR EVERY TARGET GET THE INTERACTORS UNDER CERTAIN DISTANCE ────────────────
    for target in targets:
        G = distance_reg(ints, target, thres)
        nodes.update(set(G.nodes()))
        edges.update(set(G.edges()))
    go = False
    time.sleep(0.5)
    # ────────────────────────────────────────────────────────────────────────────────
    # ─── CREATING GENERAL GRAPH WITH ALL TARGETS ────────────────────────────────────
    g = nx.Graph()
    edges = list(edges)
    nodes = list(nodes)
    g.add_nodes_from(nodes)
    g.add_edges_from(edges)
    
    print('\n─────────────────────────────────────────\n')
    
    # ─── PLOTTING TH GRAPH ──────────────────────────────────────────────────────────
    if input(stylize('Would you like to see the Graph?\n(y/n): ', colored.fg(2))) == 'y':
        pos = nx.spring_layout(g)
        nx.draw_networkx_nodes(g, pos, nodelist = [x for x in g.nodes() if x not in targets], node_color = 'b')
        nx.draw_networkx_nodes(g, pos, nodelist = targets, node_color = 'r')
        nx.draw_networkx_edges(g, pos)
        nx.draw_networkx_labels(g, pos)
        plt.title('Network of target: {t}'.format(t = targets[:]))
        plt.show()
        
    # ─── PRINTING INFO ABOUT THE NETWORK ────────────────────────────────────────────
    print('\n─────────────────────────────────────────\n')
    print(stylize('Number of Edges: ', colored.fg(1)), len(edges))
    print(stylize('Number of Nodes: ', colored.fg(1)), len(nodes))
    print('\n─────────────────────────────────────────\n')
    
    e = TPE(max_workers = 5)
    go = True
    for target in targets:
        e.submit(print_rest, target)
    # ────────────────────────────────────────────────────────────────────────────────
    e.submit(print_between, targets)
    e.submit(animate)