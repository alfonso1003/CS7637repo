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
        print ''
        print '***************************************************************'
        print 'Problem Name:   ' + problem.getName()

        problemType = problem.getProblemType()
        print 'Problem Type:   ' + problemType
        print 'Correct Answer: ' + problem.correctAnswer

        attributesA, attributesB, attributesC = getAttributes(problem)
        
        attributesInBDifferentFromA = findAttributeDifferences(attributesA, attributesB)
        
        print attributesA
        print attributesB
        print attributesC
        
        print attributesInBDifferentFromA

        if problemType == '2x1':
            pass

        elif problemType == '2x2':    
            pass

        elif problemType == '3x1':
            pass

        print '***************************************************************'
        print ''

        return "6"


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
        
        return attributesA, attributesB, attributesC
    
def objectDiff(attributes1, attributes2):
    """
    attributes1 is a dictionary of the type: {ObjectName1: {AttributeName1: AttributeValue1, ...}, ....}
    similar for attributes 2
    checks two figures (Figures A and B for example) to see if there is an unequal amount of objects in them.
    returns a list of objects that exist and are associated w/attributes1 but not found to exist and be associated with attributes2
    For example, if Figure A has Objects X, Y, and Z and Figure B has Objects X and Y, then
    objectsInANotInB = objectDiff(attributesA, attributesB) ---->  objectsInANotInB = [Z]
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
                            deltaAngle = int(attributes2[a].get(k)) - int(attributes1[a].get(k))
                            differences[a].update({k:str(deltaAngle)})
                        else:
                            differences[a].update({k:v})
                # if attributes2 (B) has an attribute key/value that attributes1 (A) doesn't have, then add to the differences list
                else:
                    differences[a].update({k:v})
            
    return differences