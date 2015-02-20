import itertools

# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.
class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        pass

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return a String representing its
    # answer to the question: "1", "2", "3", "4", "5", or "6". These Strings
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName().
    #
    # In addition to returning your answer at the end of the method, your Agent
    # may also call problem.checkAnswer(String givenAnswer). The parameter
    # passed to checkAnswer should be your Agent's current guess for the
    # problem; checkAnswer will return the correct answer to the problem. This
    # allows your Agent to check its answer. Note, however, that after your
    # agent has called checkAnswer, it will#not* be able to change its answer.
    # checkAnswer is used to allow your Agent to learn from its incorrect
    # answers; however, your Agent cannot change the answer to a question it
    # has already answered.
    #
    # If your Agent calls checkAnswer during execution of Solve, the answer it
    # returns will be ignored; otherwise, the answer returned at the end of
    # Solve will be taken as your Agent's answer to this problem.
    #
    # @param problem the RavensProblem your agent should solve
    # @return your Agent's answer to this problem
    def Solve(self,problem):
        figures, attributesA, attributesB, attributesC = getAttributes(problem)
        attributesInBDifferentFromA = findAttributeDifferences(attributesA, attributesB)
        transformC(attributesC, attributesInBDifferentFromA)        
        answer = findAnswer(problem, attributesC, figures)
        
        """

        print '***************************************************************'
        print 'Problem Name:   ' + problem.getName()
        print 'Problem Type:   ' + problem.getProblemType()
        print "Answer: " + answer
        print '***************************************************************' + '\n'
        """
        #d = getProblemDictionary(problem)
        
        #print d
        
        print getProblemList(problem)
        
        #for k1 in d:
        #    for k2 in d[k1]:
        #        print k1 + k2
        #        
        #        print type(k1), type(k2)
        
        return answer
    
    
    
    
    


def getAttributes(problem):
        figures = problem.getFigures()
        figureA = figures.get("A")
        figureB = figures.get("B")
        figureC = figures.get("C")
        
        objectsA = figureA.objects
        objectsB = figureB.objects
        objectsC = figureC.objects
        
        d = getProblemDictionary(problem)
        
        #create dictionaries with Object as key and Attributes as value 
        attributesA = d[figureA.getName()]
        attributesB = d[figureB.getName()]
        attributesC = d[figureC.getName()]
        
        #Start -  Make sure Figures have an equal amount of objects to make the comparison easier.
        objectCountA = len(attributesA.keys())
        objectCountB = len(attributesB.keys())
        
        # in this case, A has an object that disappears in B.
        # to facilitate a comparison, remove object from A and the corresponding object from C.
        
        if(objectCountA > objectCountB):
            objectsInANotInB = objectDiff(attributesA, attributesB)
            attributesA = removeObjectFromFigure(objectsInANotInB, attributesA)
            attributesC = removeObjectFromFigure(objectsInANotInB, attributesC)
            
        # in this case, B has an extra object        
        elif(objectCountB > objectCountA):
            """
            This special case was written to solve Classmates Problem 2.
            My code assumes object names match between figures, however my classmate's problem does not fit this assumption
            Will have to rework my code to handle cases where the figure names don't match
            """
            objectsInBNotInA = objectDiff(attributesB, attributesA)
            attributesA = addObjectToFigure(objectsInBNotInA, attributesA, attributesB)
            attributesC = addObjectToFigure(objectsInBNotInA, attributesC, attributesB)
            
        #End -  Make sure Figures have an equal amount of objects to make the comparison easier.
        
        return figures, attributesA, attributesB, attributesC
    
def objectDiff(attributes1, attributes2):
    """
    attributes1 is a dictionary of the type: {ObjectName1: {AttributeName1: AttributeValue1, ...}, ....} similar for attributes 2
    checks two figures (Figures A and B for example) to see if there is an unequal amount of objects in them.
    returns a list of objects that exist and are associated w/attributes1 but not found to exist and be associated with attributes2
    For example, if Figure A has Objects X, Y, and Z and Figure B has Objects X and Y, 
    then objectsInANotInB = objectDiff(attributesA, attributesB) ---->  objectsInANotInB = [Z]
    """
    diff =[]

    for i in attributes1.keys():
        if i not in attributes2.keys():
            diff.append(i)
    return diff

def removeObjectFromFigure(diff, attributes):
    for i in diff:
        value_to_remove = i
        attributes = {key: value for key, value in attributes.items() if key != value_to_remove}
    return attributes
        
def addObjectToFigure(diff, attributesListToBeAddedTo, attributesListToBeAddedFrom):
    for i in diff:
        attributesListToBeAddedTo.update({i:attributesListToBeAddedFrom.get(i)})
    return attributesListToBeAddedTo

def getProblemDictionary(problem):
    """
    Organize problem into a dictionary with the following structure:
    d = {FigureName1: {ObjectName1: {AttributeName1: AttributeValue1, ...}}, ... , FigureNameN: {ObjectNameN: {AttributeNameN: AttributeValueN}}}
    """
    d = {}

    figures = problem.getFigures()
    for f in figures:
        objects = figures.get(str(f)).objects
        d[f] = {}

        for o in objects:
            attributes = o.attributes
            d[f][o.getName()] = {}

            for a in attributes:
                d[f][o.getName()][a.getName()] = a.getValue()

    return d


def findAttributeDifferences(attributes1, attributes2):
    differences = {}
    for a in attributes2:
        differences.update({a:{}})
        if a in attributes1:
            for k,v in attributes2[a].iteritems():
                # if attributes2 (B) has an attribute value that changed from the corresponding attributes1 (A) value, then add to the differences list
                if attributes1[a].get(k):
                    if attributes1[a].get(k) != attributes2[a].get(k):
                        if k == "angle":
                            deltaAngle = int(attributes2[a].get(k)) - int(attributes1[a].get(k)) % 360
                            differences[a].update({k:str(deltaAngle)})
                        else:
                            differences[a].update({k:v})
                # if attributes2 (B) has an attribute key/value that attributes1 (A) doesn't have, then add to the differences list
                else:
                    differences[a].update({k:v})
            
    return differences

def transformC(attributesC, attributesInBDifferentFromA):
    for object, attributes in attributesInBDifferentFromA.iteritems():
        if attributesC.get(object):
            object = attributesC.get(object)
            
            # transforming the objects at this point
            for k, v in attributes.iteritems():
                # problem 19 exception.
                # rotating a circle doesn't do anything ... just ignore this case and keep looping
                if((object.get('shape')=="circle") and (k=="angle")):
                    continue
                object[k]=v 

def findAnswer(problem, attributes, figures):
    answers = ["1","2","3","4","5","6"]
    for a in answers:
        objects = figures.get(a)
        d = getProblemDictionary(problem)
        objectAttributes = d[objects.getName()]
        
        # was pleased to find you can compare dictionaries like this below! so easy compared to java
        if objectAttributes == attributes:
            return a
    return "10" # guess en lieu of random number generator


# some code that I need to integrate to the above so i can run algorithm across all possible correspondence combinations
def correspondences(list1, list2):
    """
    list1 is a list of the objects in Figure A
    list2 is a list of the objects in Figure B
    returns a list of list of tuples which represent all possible correspondences between the **indices** of list1 and list2
    """
    len1 = len(list1)
    len2 = len(list2)
    indices1 = [i for i in range(len1)]
    indices2 = [i for i in range(len2)]
    
    if len1 >= len2:
        correspondences = [zip(x,indices2) for x in itertools.permutations(indices1,len(indices2))]
    else:
        correspondences = [zip(indices1, y) for y in itertools.permutations(indices2,len(indices1))]

    return indices1, indices2, correspondences


def objects_to_remove_or_add(indices1, indices2, correspondence_list_of_tuples):
    """
    indices1 is a list of the indices of the objects in Figure A
    for example, if objects_in_A = [X, Y, Z] then indices1 = [0, 1, 2]
    similar for indices2
    correspondence_list_of_tuples is a correspondence between the indices of the objects in Figures A and B
    In order to make a comparison and transformation, it is useful to make sure Figures A, B, C, and the candidate answer have an equal amount of objects
    This function will return what objects can be removed or added to the Figures
    """
    len1 = len(indices1)
    len2 = len(indices2)
    status = {'add to A and C': None, 'remove from B and answer': None}
    
    if len1 == len2:
        return status
    elif len1 > len2:
        x_vals = zip(*correspondence_list_of_tuples)[0]
        remove_list = [l for l in indices1 if l not in x_vals]        
        status['remove from B and answer'] = remove_list
        return status
    else:
        y_vals = zip(*correspondence_list_of_tuples)[1]
        add_list = [l for l in indices2 if l not in y_vals]
        status['add to A and C'] = add_list
        return status
"""
# Examples
# Lists represent the objects in A and B
list1, list2 = ['A', 'B', 'C'], ['D', 'E', 'F']
indices1, indices2, correspondence_list = correspondences(list1, list2)
print correspondence_list
for c in correspondence_list:
    remove_or_add = objects_to_remove_or_add(indices1, indices2, c)
    print c , remove_or_add

print "*******************************************************************"

list3, list4 = ['A', 'B'], ['C', 'D', 'E']
indices3, indices4, correspondence_list =  correspondences(list3, list4)
print correspondence_list
for c in correspondence_list:
    remove_or_add = objects_to_remove_or_add(indices3, indices4, c)
    print c, remove_or_add
    

print "*******************************************************************"

list5, list6 = ['A', 'B', 'C'], ['D', 'E']
indices5, indices6, correspondence_list =  correspondences(list5, list6)
print correspondence_list
for c in correspondence_list:
    remove_or_add = objects_to_remove_or_add(indices5, indices6, c)
    print c, remove_or_add

    
print "*******************************************************************"


TODO: repurpose Project 1 algorithm


get list_of_objects_from_A and list_of_objects_from_B and compare length of lists

if lengths are the same:
    find all correspondences between objects in A and B:
    for each correspondence, run Project 1 algorithm
        stop when answer is found
    
if list_of_objects_from_A > list_of_objects_from_B:
    find all correspondences between objects in A and B:
        for each correspondence, pop the extra object(s) in B and answer:
            for each correspondence, run Project 1 algorithm
                stop when answer is found
                    
if list_of_objects_from_A < list_of_objects_from_B:
    find all correspondences between objects in A and B:
        for each correspondence, add the extra object(s) to A and C:
            for each correspondence, run Project 1 algorithm
                stop when answer is found
"""