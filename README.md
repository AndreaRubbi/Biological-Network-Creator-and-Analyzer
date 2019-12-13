# Biological Network Creator and Analyzer by: Andrea Rubbi


Biological Network Creator and Analyzer: python program able to identify the unique interactions between human proteins from Uniprot database, plot them and, if requested, analyze a subgraph with respect to some target proteins 

## How to use it:

You can both run the program with the mitab file or without:

run the program: $ ./network_gen.py  | or | $ ./network_gen.py mitab

If you run it without the file it will first ask you to choose it with an
automatically opened window.

It asks several questions that are too trivial to be explained.

However, two of them are worthy of an explanation:

  -the program will ask you which proteins you want to select as target
  -then it will ask a distance threshold from the targets for the creation of the subgraph.

### About Input File:

You can find this kind of file on databases such as Intact.
During the development and testing of the program the file with all the interactions
on Intact database has been used.
link of that file --> ftp://ftp.ebi.ac.uk/pub/databases/intact/current/all.zip

## Requirements

 -- easygui --> python3 -m pip install easygui  
 -- colored --> python3 -m pip install colored
 -- pandas --> python3 -m pip install pandas
 -- matplotlib.pyplot --> python3 -m pip install matplotlib
 -- networkx --> python3 -m pip install networkx
 -- concurrent.futures --> python3 -m pip install futures






