# Bhowmick agreement measure
Implementation of inter-annotator agreement measure described in (Bhowmick et al., 2008)
- https://dl.acm.org/citation.cfm?doid=1611628.1611637
- http://www.aclweb.org/anthology/W08-1209

###### Example of use:
`python2 compute_bhowmick_agreement.py example_categories.csv example_annotations.csv`

- `example_categories.csv` contains the possible labels, one per line.
- `exemple_annotations.csv` contains the annotations with the comma-separated columns, the 1st column being ids of elements, and the following representing the different annotators (one column per annotator).