from lxml import etree
from tree import Tree


## will be used as global variables to generate recursively the KAF constituent nodes
NOTER='nonter'
TER='ter'
EDGE='edge'
noter_cnt=0
ter_cnt=0
edge_cnt=0


list_t = []
list_nt = []
list_edge = []

##This function generates a "tree" xml element as defined in KAF from a string containing
##the penntreebank format and a list of term ids to do the linking
'''           
s = '(S (NP (DET The) (NN dog)) (VP (V ate) (NP (DET the) (NN cat))) (. .))'
ids = ['t0 t1','t2','t3','t4','t5','t6']
tree_node = create_constituency_layer(s, ids)
e = etree.ElementTree(element=tree_node)
e.write(sys.stdout,pretty_print=True)
'''
def convert_penn_to_kaf(tree_str,term_ids,logging,lemma_for_termid):
    global list_t, list_nt,list_edge
    list_t = []
    list_nt = []
    list_edge = []
    
    this_tree = Tree(tree_str)
    logging.debug('\n'+str(this_tree))

   
    for num, token in enumerate(this_tree.leaves()):
        position = this_tree.leaf_treeposition(num)
        token_id = term_ids[num]
        this_tree[position] = token_id
        logging.debug('Matching '+token+' with term id='+token_id+' which according to KAF lemma='+str(lemma_for_termid.get(token_id).encode('utf-8')))

    
    ##Creat the ROOT
    num_nt = len(list_nt)
    nt_id = 'nter'+str(num_nt)
    list_nt.append((nt_id,'ROOT'))
    
    visit_node(this_tree, nt_id)
 
    root = etree.Element('tree')
    nonter_heads = set()
    #Nonter
    labels_for_nt = {}
    for nt_id, label in list_nt:
        ##Checking the head
        if len(label)>=2 and label[-1]=='H' and label[-2]=='=':
            nonter_heads.add(nt_id)
            label = label[:-2]
        ele = etree.Element('nt', attrib={'id':nt_id,'label':label})
        labels_for_nt[nt_id] = label
        root.append(ele)
    
    ## Terminals
    lemma_for_ter = {}
    for ter_id, span_ids in list_t:
        ele = etree.Element('t',attrib={'id':ter_id})
        span = etree.Element('span')
        ele.append(span)
        for termid in span_ids.split(' '):
            target = etree.Element('target',attrib={'id':termid})
            span.append(target)
        lemma_for_ter[ter_id] = lemma_for_termid.get(termid,'unknown')
        root.append(ele)
        
    ##Edges
    #for edge_id,node_to,node_from in list_edge:
    for edge_id, node_from, node_to in list_edge:
        ele = etree.Element('edge',attrib={'id':edge_id,'from':node_from,'to':node_to})
        
        ## For the comment
        ##Only non-ter
        label_to = labels_for_nt.get(node_to)
        
        ##Could be ter or nonter
        label_from = labels_for_nt.get(node_from)
        if label_from is None:
            label_from = lemma_for_ter.get(node_from,'kk')
                                        
        comment = '  '+(edge_id)+'  '+(label_to)+' <- '+(label_from)+' '
        
        if node_from in nonter_heads:
            ele.set('head','yes')
        root.append(etree.Comment(comment))
        root.append(ele)
          
    return root

    
def visit_node(node,id_parent=None):
    global list_t, list_nt,list_edge
    if isinstance(node,str): #is a terminal
        ##Create the terminal
        num_t = len(list_t)
        t_id = 'ter'+str(num_t)
        list_t.append((t_id,str(node)))
        
        ##Create the edge with the parent
        num_edges = len(list_edge)
        edge_id = 'tre'+str(num_edges)
        list_edge.append((edge_id,t_id,id_parent))
    else:  #Is a non terminal
        ##Create the nonterminal
        num_nt = len(list_nt)
        nt_id = 'nter'+str(num_nt)
        list_nt.append((nt_id,node.node))
        
        ##Create the linking with the parent
        if id_parent is not None:
            num_edges = len(list_edge)
            edge_id = 'tre'+str(num_edges)
            list_edge.append((edge_id,nt_id,id_parent))
        
        ##Call to the child
        for child in node:
            visit_node(child,nt_id)
