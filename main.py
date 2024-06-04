#AM: 4054 ONOMA: KONSTANTINOS EVANGELOU
#AM: 4193 ONOMA: GEORGIOS TSOUMANIS
import sys

bound_list = ['main','def','#def','#int','global','if','elif','else','while','print','return','input','int','and','or','not']

lineCounter = 1

class Token:
    def __init__(self, family, recognised_string, line_number):
        self.family = family
        self.recognised_string = recognised_string
        self.line_number = line_number


### symbol table classes and functions ###

class Entity:
    def __init__(self, name, type, offset):
        self.name = name
        self.type = type
        self.offset = offset

    def __str__(self):
        return self.name + " " + self.type + " " + self.offset
    



class Variable(Entity):
    pass

class Function(Entity):
    def __init__(self, name, datatype, start_quad, offset, formalParameters):
        super().__init__(name, datatype, offset)
        self.start_quad = start_quad
        self.formalParameters = formalParameters
        self.arguments = list()

    def __str__(self):
        return self.name + " " + self.datatype + " " + self.start_quad + " " + self.offset + " " + self.formalParameters
    


class Parameter(Entity):
    def __init__(self, name, datatype, mode, offset):
        super().__init__(name, datatype, offset)
        self.mode = mode

    def __str__(self):
        return self.name + " " + self.datatype + " " + self.mode + " " + self.offset
    

class FormalParameter(Entity):
    def __init__(self, name, datatype, mode, offset):
        super().__init__(name, datatype, offset)
        self.mode = mode

    def __str__(self):
        return self.name + " " + self.datatype + " " + self.mode + " " + self.offset
    

class TemporaryVariable(Entity): 
    def __init__(self, name, datatype, offset):
        super().__init__(name, datatype, offset)

    def __str__(self):
        return self.name + " " + self.datatype + " " + self.offset
    







class Scope:
    def __init__(self,identifier,nestingLevel):
        self.identifier = identifier
        self.nestingLevel = nestingLevel
        self.entities = list()

    
    def __str__(self):

        return self.identifier + " " + str(self.nestingLevel) + " " + str(self.entities)
    


class SymbolTable:

    scopes=list()

    def addScope(self,scope):
        scopeToAdd=Scope(scope,len(self.scopes))
        self.scopes.append(scopeToAdd)

    
    def addEntity(self,entity):
        
        if self.scopes:  # Check if there are any scopes
            self.scopes[-1].entities.append(entity)

    
    



    

    
    def removeScope(self):
        
        self.scopes.pop()


    
    def addArgument(self,argument):
        if self.scopes:
            self.scopes[-1].entities[-1].arguments.append(argument)

    def search(self,identifier):
        
        for scope in reversed(self.scopes):
            for entity in scope.entities:
                if entity.name == identifier:
                    return entity
        return None



    


    
## Lectical Analysis ##

def lex():

    global lineCounter 
    
    tokenString = "" 
    char=myFile.read(1)
    
    while True:
        
        if(char==" " or char == "\t"):
            char=myFile.read(1)
        
        elif(char=="\n"):
            
            lineCounter +=1    
            
            char=myFile.read(1)
            
        
        else:
            break   
                            
    
    if (char.isdigit()):
        tokenString= tokenString + char
        char =myFile.read(1)

        while (char.isdigit()):
            tokenString= tokenString + char
            char =myFile.read(1)
            
            if(int(tokenString)<  -32767 or int(tokenString)>32767):
                raise Exception("Int overflow")
        myFile.seek(myFile.tell()-1)
        return Token("alnum",tokenString,lineCounter)
        
    ### we are guarding the first occurance in the above if statement
    if(char.isalpha()): 

        while(char.isalnum()):
            tokenString=tokenString+char
            char=myFile.read(1)
            
            
            if(tokenString in bound_list):
                
                myFile.seek(myFile.tell()-1)
                
                return Token("keyword",tokenString,lineCounter)
            if(len(tokenString)>30):
                raise Exception("character overflow " , tokenString, len(tokenString), lineCounter)
           
        
        myFile.seek(myFile.tell()-1)
        # if(lineCounter>121):
        #     myFile.seek(myFile.tell()-1)
            
        
       
        return Token("alnum",tokenString,lineCounter)
    

    if(char=="+"):                                                  
        return Token("addOperator",char,lineCounter)
    
    if(char=="-"):
        return Token("minusOperator",char,lineCounter)
    
    if(char=="*"):
        return Token("mulOperator",char,lineCounter)
    if (char == "="):
        char=myFile.read(1)
        if(char=="="):
            return Token("comparatorOperator","==",lineCounter)
        else:
            
            return Token("equalOperator","=",lineCounter)
        

    if(char=="/"):
        char=myFile.read(1)
        if(char=="/"):
            return Token("modOperator","//",lineCounter)
        else:
            raise Exception("Invalid character")  
        
    if(char=="%"):
        return Token("divOperator",char,lineCounter)
    
    if(char=="<"):
        char=myFile.read(1)
        if(char=="="):
            return Token("smallerOrEqualOperator","<=",lineCounter)
        else:
            myFile.seek(myFile.tell()-1)
            return Token("smallerOperator","<",lineCounter)
        
    if(char==">"):
        char=myFile.read(1)
        if(char=="="):
            return Token("biggerOrEqualOperator",">=",lineCounter)
        else:
            myFile.seek(myFile.tell()-1)
            return Token("biggerOperator",">",lineCounter)
        
    if(char=="!"):
        char=myFile.read(1)
        if(char=="="):
            return Token("smallerOrEqualOperator","!=",lineCounter)
        else:
            raise Exception("Invalid character")  

        
    

    if(char=="#"):
        char = myFile.read(1)
        if char == "#":
            # Ignore characters until "##" is encountered
            while True:
                char = myFile.read(1)
                if char == "#":
                    char = myFile.read(1)
                    if char == "#":
                        break
            
            return lex()

            
        elif(char=="{"):
            return Token("lBracketOperator","#{",lineCounter)
        
        elif(char=="}"):
            return Token("rBracketOperator","#}",lineCounter)    
        elif(char=="i"): 
            next_chars = char + myFile.read(2)  # Read the next two characters
            if next_chars == "int":
                return Token("keyword", "#int", lineCounter)
            else:
                raise Exception("Invalid character")
        elif(char=="d"):
            next_chars = char + myFile.read(2)
            if next_chars == "def":
                return Token("keyword", "#def", lineCounter)
            else:
                raise Exception("Invalid character")
        
        else:
            raise Exception("Invalid character ddin %i %s" , lineCounter, char)  
    
    
    if(char==":"):
        return Token("colonOperator",char,lineCounter)
    
    if(char==","):
        return Token("comaOperator",char,lineCounter)



    if(char=="("):
        return Token("lParenthesisOperator",char,lineCounter)
    if(char==")"):
        return Token("rParenthesisOperator",char,lineCounter)
    
    
    

    if(char ==""):
        return Token("EOF","",lineCounter)
    else:
        raise Exception("Unknown charachter")




## Syntax Analysis ##
    






def program():
    global token
    token = lex()
    declarations()
    while token.recognised_string == "def":
        functionDefinition()
    mainfunction()
    print("Syntax analysis completed successfully")
    
    
    

    
    
    

def functionDefinition(): 
    global token
    if token.recognised_string == "def":
        token = lex()
        
        if token.family == "alnum":

            function=Function(token.recognised_string, "int", next_quad(), 0, list())
            symbol_table.addEntity(function)
            token = lex()
            if token.recognised_string == "(":
                formalparlist()
                #token = lex()
                if token.recognised_string == ")":
                    token = lex()
                    if token.recognised_string == ":":
                        token=  lex()
                        
                        block()
                    else:

                        raise Exception("Syntax error: expected colon", token.recognised_string, token.line_number)
                else:
                    
                    raise Exception("Syntax error: expected closing parenthesis " , token.recognised_string, token.line_number)
            else:
                
                raise Exception("Syntax error: expected opening parenthesis ", token.recognised_string)
        else:
            
            raise Exception("Syntax error: expected identifier")
    else:
        
        pass



symbol_table = SymbolTable()


def block():
    global token
    global symbol_table
    if token.recognised_string == "#{":
        token = lex()
         
        symbol_table.addScope("block")
        declarations()
        functionDefinition()
        globalDeclaration()
        
        gen_quad("begin_block", "_", "_", "_")
        
        while (token.recognised_string != "#}"):
            statements()
        if token.recognised_string == "#}":
            token = lex()
            symbol_table.removeScope()
            gen_quad("end_block", "_", "_", "_")
        else:
            
            raise Exception("Syntax error: expected closing brace }#",token.recognised_string, token.line_number)
    else:
        
        raise Exception("Syntax error: expected opening brace #{ %s %i" , token.recognised_string, token.line_number)
    


def declarations():     
    global token
    if token.recognised_string == "#int":
        token = lex()
        if token.family == "alnum":
            token = lex()
            variable=Variable(token.recognised_string, "int", 0)
            symbol_table.addEntity(variable)
            
        else:
            
            raise Exception("Syntax error: expected identifier")
    else:
        pass  # No declarations to parse

def statements():
    global token
    if(token.family=="alnum"):
        
        identifier=token.recognised_string

        value=assignstatement()

        gen_quad("=", value, "_", identifier)

    if(token.recognised_string=="if"):
        token=lex()
        ifstatement()
    
    
    elif(token.recognised_string=="while"):
        token=lex()
        whilestatement()
    elif(token.recognised_string=="return"):
        token=lex()
        returnstatement()
    elif(token.recognised_string=="print"):
        token=lex()
        printstatement()
    elif(token.recognised_string=="int"):
        token=lex()
        inputstatement()
    else:
        pass    



def printstatement():
    global token
    if token.recognised_string == "(":
        token = lex()  
        value= expression()  
        
        if token.recognised_string == ")":
            token = lex()  
            gen_quad("out", value, "_", "_")
        else:
            
            raise Exception("Syntax error: expected closing parenthesis", token.recognised_string, token.line_number)
    else:
        
        raise Exception("Syntax error: expected opening parenthesis", token.recognised_string, token.line_number)

    

def assignstatement():
    global token
    if token.family == "alnum":
        
        token = lex()
        if token.recognised_string == "=":
            token = lex()
            return expression()  
            
        else:
            
            raise Exception("Syntax error: expected assignment operator" , token.recognised_string, token.line_number)
    else:
        raise Exception("Syntax error: expected identifier", token.recognised_string, token.line_number, token.family)    

def ifstatement():
    global token
    (conditionTrue,conditionFalse)=condition()  
    
    
    if token.recognised_string == ":":
        token = lex()
        back_patch(conditionTrue, next_quad())
        statements()  
        while(token.recognised_string=="elif"):
            token=lex()
            ifstatement()

        if(token.recognised_string=="else"):
        
            token=lex()
            skip_list = make_list(next_quad())
            gen_quad("jump", "_", "_", "_")
            back_patch(conditionFalse, next_quad())
            
        
            else_statement()
            back_patch(skip_list, next_quad())
        
        
        

    else:
        
        raise Exception("Syntax error: expected colon" , token.recognised_string, token.line_number)
        
   

def else_statement():
    global token
    
    if token.recognised_string == ":":
        token = lex()  
        statements()  
       
    else:
       
        raise Exception("Syntax error: expected colon", token.recognised_string, token.line_number)
    

def whilestatement():
    global token
    while_start = next_quad()
    (conditionTrue,conditionFalse)=condition()
    
    if token.recognised_string == ":":    
        token=lex()
        back_patch(conditionTrue, next_quad())
        block()
        gen_quad("jump", "_", "_", while_start)
        back_patch(conditionFalse, next_quad())
    else:
       
        raise Exception("Syntax error: expected colon")


def returnstatement():
    global token
    toReturn=expression()
    gen_quad("ret", toReturn, "_", "_")  
    

def inputstatement():
    global token
    if token.recognised_string == "(":
        token = lex()
        if token.recognised_string == "input":
            token = lex()
            if token.recognised_string == "(":
                token = lex()
                if token.recognised_string== ")":
                        token = lex()

                        gen_quad("in", "_", "_", "_") 
                else: 
                    raise Exception("Syntax error: expected closing parenthesis", token.recognised_string, token.line_number)
                
                if token.recognised_string == ")":
                    token = lex()
                    
                else:
               
                    raise Exception("Syntax error: expected closing parenthesis", token.recognised_string, token.line_number)
            else:
                    raise Exception("Syntax error: expected opening parenthesis", token.recognised_string, token.line_number)
        else:
           
            raise Exception("Syntax error: expected identifier",    token.recognised_string, token.line_number)
    else:
       
        raise Exception("Syntax error: expected opening parenthesis", token.recognised_string, token.line_number)        






def multiply():
    global token
    op =""
    if (token.recognised_string == '*' or token.recognised_string =="//" or token.recognised_string == "%"):
        op = token.recognised_string
        token=lex()
    else:
        raise Exception("Syntax error: expected multiplication or division operator")
    return op


def add():
    global token
    op=""
    if (token.recognised_string == '+' or token.recognised_string =="-"):
        op = token.recognised_string
        token=lex()
    else:
        raise Exception("Syntax error: expected addition or subtraction operator")
    return op


def condition():
    global token
    
    
    (conditionTrue,conditionFalse)=boolterm()  
    while token.recognised_string == "or":
        back_patch(conditionFalse, next_quad())
        token = lex()
        (condition1True,condition1False)=boolterm()
        condition1True=merge(conditionTrue,condition1True)
        conditionFalse=condition1False
    return conditionTrue,conditionFalse
    

def boolterm():
    global token
    (conditionTrue,conditionFalse)=boolfactor()  
    while token.recognised_string == "and":
        back_patch(conditionTrue, next_quad())
        token = lex()
        (condition1True,condition1False)=boolfactor()
        condition1False=merge(conditionFalse,condition1False)
        conditionTrue=condition1True
    return conditionTrue,conditionFalse

def boolfactor():
    global token
    if token.recognised_string == "not":
        token = lex()
        boolfactor()
    else:
        
        firstExpression=expression() 
        
        op=relop()  
        secondExpression=expression() 

        conditionTrue=make_list(next_quad())
        gen_quad(op, firstExpression, secondExpression, "_")
        conditionFalse=make_list(next_quad())
        gen_quad("jump", "_", "_", "_")
        return conditionTrue, conditionFalse





def expression(): 
    global token 
    
    firststTerm=term()  
    signtmp = new_temp()
    gen_quad("+", firststTerm, 0, signtmp)
    
    while token.recognised_string == "+" or token.recognised_string == "-":
        
        op=add()  
        anotherTerm=term()  
        temp=new_temp()
        gen_quad(op, signtmp, anotherTerm, temp)
        firststTerm=temp
    return firststTerm
    

    

def relop(): 
    global token 
    
    if token.recognised_string == "<" or token.recognised_string == ">" or token.recognised_string == "==" or token.recognised_string == "!=" or token.recognised_string == "<=" or token.recognised_string == ">=":
        toReturn = token.recognised_string
        token = lex() 
        return toReturn
        
    else:
        
        raise   Exception("Syntax error: expected relational operator", token.recognised_string, token.line_number, token.family)





def term(): 
    global token
    
    firstFactor=factor()  
   
    while token.recognised_string == "*" or token.recognised_string == "//" or token.recognised_string == "%":
        op=multiply() 
        secondFactor=factor()
        temp=new_temp()
        gen_quad(op, firstFactor, secondFactor, temp)
        firstFactor=temp
    return firstFactor 

def factor(): 
    global token
    
    toReturn=call_func()

    if token.family == "number":
        toReturn = token.recognised_string
        token = lex()  
        
    elif token.recognised_string =="(":
        
        token = lex()
        toReturn=expression()
        
        
        if token.recognised_string == ")":
            token = lex()
        else:
            
            raise Exception("Syntax error: expected closing parenthesis")

    
    
    return toReturn
        
    

def call_func():
    global token
    if token.family == "alnum":
        funcName = token.recognised_string
        gen_quad("call", funcName, "_", "_")
        token = lex() 
        if token.recognised_string == "(":
            token = lex()  
            actualparse()
           
            if token.recognised_string == ")":
                token = lex()  
            else:
                
                raise Exception("Syntax error: expected closing parenthesis")
        else:
            pass
        return funcName
    else:
        pass

def actualparse():
    global token
    if token.recognised_string != ")":
        actualparlist()
    else:
        
        pass
       

def actualparlist():
    global token
    actualparitem()
    
    while token.recognised_string == ",":
        token = lex()  
        actualparitem()


def actualparitem():
    global token


    
    toReturn=expression() 
    gen_quad("par", toReturn, "CV", "_")

    

def formalparlist():
    
    global token
    token=lex()
    formalparitem()
    
    while token.recognised_string == ",":
        token = lex() 
        formalparitem()


def formalparitem():
    global token
    
    parameter=Parameter(token.recognised_string, "int", "CV", 0)
    symbol_table.addArgument(parameter)
    
    token=lex()


    # expression()
    



def globalDeclaration(): 
    global token
    
    if token.recognised_string == "global":
        
        token = lex()  
        if token.family == "alnum":
            token = lex()
            
        else:
            
            raise Exception("Syntax error: expected identifier")
    else:
        
        pass


def mainfunction():
    global token
    if token.recognised_string == "#def":
        token = lex()  
        if token.recognised_string == "main":
            token = lex()  
            declarations()
            
            while token.family != "EOF":
                statements()
             
        else:
            
            raise Exception("Syntax error: expected 'main' keyword")
    else:
        
        raise Exception("Syntax error: expected '#def' keyword")




    ### intermediate code generation ###
quad_list=list()
temp_counter = 0
class Quad():
        
    def __init__(self, operator, arg1, arg2, target):
        self.operator = operator
        self.arg1 = arg1
        self.arg2 = arg2
        self.target = target

    def __str__(self):
        return (str(self.operator)) + "," + (str(self.arg1)) + "," + (str(self.arg2)) + "," + (str(self.target))


def gen_quad(operator, arg1, arg2, target):
    global quad_list
    # global nextlabel
    # label = nextlabel
    # nextlabel += 1
    quad = Quad(operator, arg1, arg2, target)
    quad_list.append(quad)
    return quad


def next_quad():
        return len(quad_list)

def back_patch(list, target): ##maybe needs repair
    for i in list:
        quad_list[i].target = target

def new_temp():
    global temp_counter
    temp = "T_" + str(temp_counter)
    temp_counter += 1

    tempVar = TemporaryVariable(temp, "int", 0)
    symbol_table.addEntity(tempVar)
    return temp
    

def empty_list():
    return list()

def merge(list1, list2):
    return list1 + list2

def make_list(label):
    newlist = list()
    newlist.append(label)
    return newlist


def outputFile(filename):
    f1 = open(filename +".sym", "a")
    for scope in symbol_table.scopes:
        f1.write(str(scope) + "\n")
    f1.close()
    


def main(args):
    if len(args) < 2:
        print("Usage: python main.py <file>")
        return

    file = args[1]  
    global myFile
    try:
        myFile = open(file, "r")
        print("File found") 
        
    except FileNotFoundError:
        print("File not found")
        pass
    program()

    filename = "intermideateCode.int"  # Choose your desired filename

    with open(filename, "w") as file:  # Open in write mode ('w')
        for quad in quad_list:
            file.write(str(quad) + "\n")  # Write each quad as a string with a newline

        file.write(f"Total number of quads: {len(quad_list)}\n")

if __name__ == "__main__":
    main(sys.argv)