import numpy as np
import matplotlib.cm as cmx
import matplotlib.pyplot as plt
import matplotlib.colors as clrs
import numbers
import math
import re

#SCROLL DOWN TO MAIN PART


#FUNCTIONS
#The main method
def dissimilarityBasedColoring(str):
    #builds tree structured list from string representation of dendrogram
    tree = make_tree(str)

    
    #step 1 - initial shade values are found
    l=traverse_tree(tree)
    #step 2 - initial values are normalized
     
    #find the maximum value of initial shades
    max=get_max(l)
    #normalized list is returned
    n=normalize(l,max)

    #step 3- match objects with shades
    i=0
    
    #match objects and shades
    for each_item in tree:
        match_object_and_shade(each_item,n[i])
        i=i+1
        
    shades=[]
    #produce list matching the positions of original objects in list 'object'
    for object in objects:
        shades.append(dict[object])
    return shades

#traverse the tree using post-order
def traverse_tree(the_list):
    #if is node with children
    if isinstance(the_list, list):
        #list used to store information for current node
        r=[]
        nr=[]
        #call borth children
        for each_item in the_list:
            #get sublist [[v_1, v_2],[ v_3, v_4]] 
            r.append(traverse_tree(each_item))
            #find two objects, one from each sublist
            nr.append(get_item(each_item))
        #find dissimilarity from dissimilarity matrix using two object found from sublists
        #due to hierarchical clustering, the dissimilarity of current node equals 
        #the distance between two elements from different subtrees
        dis=DIS[int(nr[0])][int(nr[1])]
        #if both children were leaves
        if(r[0]==0 and r[1]==0):
            return [0,dis]
        #if at least one child was sublist
        else:
            #find minimum and maximum values from sublists
            min1=get_min(r[0])
            min2=get_min(r[1])
            max1=get_max(r[0])
            max2=get_max(r[1])
            #find midpoints for both subtrees
            m1=(min1+max1)/2
            m2=(min2+max2)/2
            #add difference of dissimilarity between midpoints of both subtree
            diff=m1+dis-m2
            #prepare results            
            r2=[]
            r2.append(r[0])
            #recalculate second subtree
            r2.append(reCalculate(r[1],diff))
            #return repositioned list reflecting dissimilarity between two clusters at current node
            return r2
    #is leaf
    else:
        return 0  
    
#find minimum value of tree structured list    
def get_min(the_list):
    #set large positive value for initial value
    min=9999999
    #recursively call children
    if isinstance(the_list, list):
        for each_item in the_list:
            m=get_min(each_item)
            #if m is smaller than current min, update it
            if(m<min):
                min=m
        #return smallest value in current tree
        return min 
    #is leaf
    else:
        return the_list 
    
#find maximum value of tree structured list
def get_max(the_list):
    #set large negative value for initial value
    max=-9999999
     #has children
    if isinstance(the_list, list):
        #recursively call children
        for each_item in the_list:
            m=get_max(each_item)
            #if m is larger than current max, update it
            if(m>max):
                max=m
        #return largest value in current tree
        return max 
    #is leaf
    else:
        return the_list 
    
#returns first found leaf of a subtree for finding dissimilarity 
def get_item(the_list):
    if isinstance(the_list, list):
        return get_item(the_list[0])
    else:
        #returns index of object
        return objects.index(the_list)
    
#normalizes the feature space [0,max] to [0,1]    
def normalize(the_list,max):
    #has children
    if isinstance(the_list, list):
        r=[]
        #recursively call children
        for each_item in the_list:
            r.append(normalize(each_item,max))
        return r 
    #is leaf
    else:
        #actual normalization on single object shade
        return the_list/max 
    
#recursively traverse the sub.tree and add diff to every element
def reCalculate(the_list,diff):
    l=[]
    #has children
    if isinstance(the_list, list):
        for each_item in the_list:
            #recursively call children
            l.append(reCalculate(each_item,diff))
        return l
    #is leaf
    else:
        return the_list+diff 

# turns string representation of dendogram stucture to tree structured list
def make_tree(data):
    items = re.findall(r"\(|\)|\w+", data)

    def req(index):
        result = []
        item = items[index]
        while item != ")":
            if item == "(":
                subtree, index = req(index + 1)
                result.append(subtree)
            else:
                result.append(item)
            index += 1
            item = items[index]
        return result, index

    return req(1)[0]

#assumes that all objects' names/indicators  are stored in list 'objects'
#matches the one dimensional list of objects with tree structured list with names/indicators and calculated shades
def match_object_and_shade(the_list,shades):
    i=0
    if isinstance(the_list, list):
        for each_item in the_list:
            match_object_and_shade(each_item,shades[i])
            i=i+1
    else:
        #save name/indicator with corresponding shade value
        dict[the_list]=shades
        


#MAIN PART        
objects=['Linsead','Perilla','Cotton','Sesame','Camellia','Olive','Beef','Hog']
#load dissimilarity matrix for objects
DIS = np.loadtxt("dis.txt", dtype='d', delimiter=',')
#clustering results for objects
cluster_str='((((Olive-Camellia)-(Sesame-Cotton))-(Perilla-Linsead))-(Hog-Beef))'

#call main function, find shade values
dict= {}
shades=dissimilarityBasedColoring(cluster_str)
print(shades)


#map shades to colormap
#Currently colormap named "Greys" is used (from white to black)
jet = cm = plt.get_cmap('Greys') 
cNorm  = clrs.Normalize(vmin=0, vmax=1)
scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)
for e in range(len(objects)):
    color = scalarMap.to_rgba(shades[e])
    print(objects[e]+" "+str(color))
    
    
#Author:KADRI UMBLEJA, kadriumbleja@gmail.com