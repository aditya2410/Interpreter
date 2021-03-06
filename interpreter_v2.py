import re
state={}
f_dict={}
class main_prog(object):
    """docstring for main_prog"""
    def __init__(self, arg):
        self.arg = arg

    def eval(self,stack=state):
        for x in self.arg:
            x.eval(stack)
        
    

class if_block(main_prog):
    """docstring for if_block"""
    def __init__(self,cond,then=[],els=[]):
        self.cond = cond
        self.then = then
        self.els = els
    def eval(self,stack=state):
        if self.cond.eval(stack)==True:
            for statement in self.then:
                statement.eval(stack)
        elif(self.els != None):
            for statement in self.els:
                statement.eval(stack)



class while_block(main_prog):
    """docstring for while_block"""
    def __init__(self,cond,body=[]):
        self.cond = cond
        self.body = body
    def eval(self,stack=state):
        while self.cond.eval(stack) is True:
            for statement in self.body:
                statement.eval(stack)
    

class print_stat(main_prog):
    """docstring for print_stat"""
    def __init__(self,stri=None):
        self.stri = stri

    def eval(self,stack=state):
        #print "stri",self.stri
        for x in self.stri:
            if x[0]=='"':
                print(x[1:-1],end=" ")
            else:
                print(state[x],end=" ")
        print("")
            

        

class expr(main_prog):
    """docstring for expr"""
    def __init__(self,left_op,right_op,op_type,function_call=False):
        self.left_op = left_op
        self.right_op = right_op
        self.op_type = op_type
        self.function_call=function_call

    def eval(self,stack=state):
        # print(stack,"expr_state")
        if self.op_type!=None:
            if self.op_type == '+':
                a=self.left_op.eval(stack) + self.right_op.eval(stack)
            # print("a11",a)
                return a
            elif self.op_type == '-':
                a=self.left_op.eval(stack) - self.right_op.eval(stack)
                return a
            elif self.op_type == '*':
                a=self.left_op.eval(stack) * self.right_op.eval(stack)
                return a
            elif self.op_type == '/':
                a=self.left_op.eval(stack) / self.right_op.eval(stack)
                return a
            elif self.op_type == '%':
                a=self.left_op.eval(stack) % self.right_op.eval(stack)
                return a
            elif self.op_type == '**':
                a=self.left_op.eval(stack) ** self.right_op.eval(stack)
                return a
            else:
                raise ValueError('invalid operator')
        elif self.right_op=='0':
            if self.function_call:
                return self.left_op.eval(stack)
            else:
                if self.left_op[0].isalpha():
                    a=float(stack[self.left_op])
                    # print("a11 123",a)
                    return a
                else:
                    a=float(self.left_op)
                    return a
        elif self.left_op=='0':
            if self.function_call:
                return self.right_op.eval(stack)
            else:
                if self.right_op[0].isalpha():
                    a=float(stack[self.right_op])
                    return a
                else:
                    a=float(self.right_op)
                    return a
        
            
        

class assi_statem(main_prog):
    """docstring for assi_statem"""
    def __init__(self,var,expri):
        self.var = var
        self.expri = expri

    def eval(self,stack=state):
        # print(stack,"assi_state",self.var,"variable")
        stack[self.var]=self.expri.eval(stack)

        
class condition(main_prog):
    """docstring for condition"""
    def __init__(self,left,cond_op,right):
       self.left = left
       self.right =right
       self.cond_op=cond_op

    def eval(self,stack=state):
        if self.cond_op == '>':
            a=self.left.eval(stack) > self.right.eval(stack)
            return a
        elif self.cond_op == '<':
            a=self.left.eval(stack) < self.right.eval(stack)
            return a
        elif self.cond_op == '<=':
            a=self.left.eval(stack) <= self.right.eval(stack)
            return a
        elif self.cond_op == '>=':
            a=self.left.eval(stack) >= self.right.eval(stack)
            return a
        elif self.cond_op == '==':
            a=self.left.eval(stack) == self.right.eval(stack)
            return a
                      
class function(main_prog):
    """docstring for function"""
    def __init__(self,name,arg):
        self.arg = arg
        self.name=name
        self.statement_list=f_dict[self.name][0]
        self.arg_name=f_dict[self.name][1]
        self.ret=f_dict[self.name][2]
        self.f_stack={}

    def eval(self,stack=state):
        f_stack={}
        i=0
        for x in self.arg_name:
            f_stack[x]=self.arg[i]
            i=i+1
            f_stack[self.ret]=None
        # print(f_stack,"function_stack")
        for y in self.statement_list:
            y.eval(stack=f_stack)
        # print("return",f_stack[self.ret])
        return f_stack[self.ret]




class Parser(object):
    def __init__(self, text):
        # client string input, e.g. "4 + 2 * 3 - 6 / 2"
        self.statement_list=[]
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0    
        self.current_char = self.text[0]
        self.operators=['-','+','/','*']
        self.cond_oper=['>','<','>=','<=','==']
        
        ####Don't touch this
        parts = re.split(r"""("[^"]*"|'[^']*')""", self.text)
        parts[::2] = map(lambda s: "".join(s.split()), parts[::2]) # outside quote
        self.text = "".join(parts)
        self.text = self.text.rstrip()
        # print(self.text)
        ###Don't touch this

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        """Advance the `pos` pointer and set the `current_char` variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def current_word(self):
        while self.current_char is not None:
            word_right=""
            word_left=""
            posi=self.pos
            while(self.current_char.isalpha() or self.current_char.isdigit()or self.current_char=='.' ):
                word_right+=self.current_char
                posi+=1
                self.current_char = self.text[posi]
            posi2=self.pos-1
            self.current_char = self.text[posi2]
            while(self.current_char.isalpha() or self.current_char.isdigit()):
                word_left+=self.current_char
                posi2-=1
                self.current_char = self.text[posi2]
            self.current_char = self.text[self.pos]
            return word_right

    def current_co_word(self):
        while self.current_char is not None:
            word_right=""
            word_left=""
            posi=self.pos
            a=['<','>','=']
            while(self.current_char in a):
                word_right+=self.current_char
                posi+=1
                self.current_char = self.text[posi]
            self.current_char = self.text[self.pos]
            return word_right


    def create_list(self):
        while self.current_char is not None:
            print("current_word",self.current_word(),self.pos,self.current_char)
            if(self.current_word()[:8]=="function"):
                self.parse_func()
                self.advance()
            elif(self.current_word()=="if"):
                self.statement_list.append(self.parse_if())
                self.advance()
                print("after if",self.current_char)
            elif(self.current_word()=="while"):
                self.statement_list.append(self.parse_wh())
                self.advance()
                
            elif(self.current_word()=="print"):
                self.statement_list.append(self.parse_pr())
                self.advance()
                print("after print ",self.current_char)
                
            else:
                self.statement_list.append(self.parse_assi())
                self.advance()
                
                print("after assignment",self.current_char)


    def parse_if(self):
        print("in if")
        self.pos+=2
        count=1
        a_if_then=[]    
        a_if_else=[]                               #create_exception
        self.current_char = self.text[self.pos]
        cond=self.parse_cond() 
        self.advance()

        flag=False
        # raise expression for then
        self.pos+=(4)
        self.current_char = self.text[self.pos]
        print(self.current_word(),self.current_char)
        while self.current_word()!="else":
            print("current word in if ",self.current_word(),self.current_char)
            if(self.current_word()=="if"):
                a_if_then.append(self.parse_if())
                self.advance()
            if(self.current_word()=="while"):
                a_if_then.append(self.parse_wh())
                self.advance()
            if(self.current_word()=="print"):
                a_if_then.append(self.parse_pr())
                self.advance()
            if(self.current_word()=="fi"):
                self.pos+=2
                self.current_char = self.text[self.pos]
                flag=True
                print(self.current_char)
                break
            else:
                a_if_then.append(self.parse_assi())
                self.advance()
                


        if(flag==False):
            self.pos+=(5)
            self.current_char = self.text[self.pos]
            while self.current_char is not None:
                if(self.current_word()=="if"):
                    a_if_else.append(self.parse_if())
                    self.advance()
                if(self.current_word()=="while"):
                    a_if_else.append(self.parse_wh())
                    self.advance()
                if(self.current_word()=="print"):
                    a_if_else.append(self.parse_pr())
                    self.advance()
                if(self.current_word()=="fi"):
                    self.pos+=2
                    self.current_char = self.text[self.pos]
                    flag=True  #raise_exception
                    break
                else:
                    a_if_else.append(self.parse_assi())
                    self.advance()

        return if_block(cond,a_if_then,a_if_else)

    def parse_wh(self):
        print("in while")
        self.pos+=5 
        a_wh=[]    
        self.current_char = self.text[self.pos]
        cond=self.parse_cond()
        self.advance()
        # raise expression for then
        while self.current_char is not None:
            if(self.current_word()=="if"):
                a_wh.append(self.parse_if())
                self.advance()
            if(self.current_word()=="while"):
                a_wh.append(self.parse_wh())
                self.advance()
            if(self.current_word()=="print"):
                a_wh.append(self.parse_pr())
                self.advance()
            if(self.current_word()=="done"):
                self.pos+=4
                self.current_char = self.text[self.pos]
                break
            else:
                a_wh.append(self.parse_assi())
                self.advance()   

        return while_block(cond,a_wh)
    
    def parse_pr(self):
        print("\"in print\"")
        self.pos+=5
        self.advance()
        #print(self.current_char," in print ")
        stri=""
        a=[]
        while self.current_char is not ')':
            if self.current_char is '"' :
                stri=""
                stri+=self.current_char
                print(stri," yo in print ")
                self.advance()
                while self.current_char is not '"':
                    print(stri,"yo 2 in print ")
                    stri+=self.current_char
                    self.advance()
                print(stri,"stri")
                stri+=self.current_char
                print(stri,"stri \"")
                self.advance()
                print(self.current_char,"bobob")
                
            elif self.current_char is ',' :
                print("stri")
                a.append(stri)
                self.advance()
                stri=""
            else:
                stri+=self.current_char
                self.advance()
        
        a.append(stri)
        print(self.current_char," in print ",a)
        self.advance()
        return print_stat(a)
        
    def parse_assi(self):
        print("in assi")
        var=self.current_word()
        self.pos+=len(var)
        print(var,"func")
        if(self.current_char=='('):
            self.advance()
            arg=self.parse_func_cal()
            self.advance()
            return function(var,arg)
        self.advance()
        expri=self.parse_expr([';'])
        return assi_statem(var,expri)


    def parse_expr(self,end):
        print("in expre")

        oper_flg=False
        right_oper=expr('0','0',None)
        left_oper=expr('0','0',None)
        while self.current_char not in end:
            # print("in expre",self.current_char,self.pos)
            if(self.current_char=='('):
                print(self.current_char)
                self.advance()
                if oper_flg==False:
                    left_oper=self.parse_expr([';'])
                else:
                    right_oper=self.parse_expr([';'])
                self.advance()

            elif(self.current_char in self.operators):
                print(self.current_char)
                oper=self.current_char
                oper_flg=True
                self.advance()
            elif(self.current_char==')'):
                print(self.current_char)
                
                return expr(left_oper,right_oper,oper)
            elif(self.current_char.isalpha() or self.current_char.isdigit()):
                print(self.current_char)
                x=self.current_word()
                a=self.pos+len(x)
                arg=None
                Flag=False
                print(x,"function")
                if(a<len(self.text)-1):
                    if(self.text[a]=='('):
                        print(x,"function")
                        self.pos=a
                        self.advance()
                        arg=self.parse_func_cal()
                        Flag=True
                        print(self.current_char,"aaaa")
                        x=function(x,arg)
                        if oper_flg==False:
                            left_oper=expr(x,'0',None,function_call=Flag)
                        else:
                            right_oper=expr('0',x,None,function_call=Flag)
                    else:
                        if oper_flg==False:
                            left_oper=expr(x,'0',None,function_call=Flag)
                            self.pos+=len(left_oper.left_op)-1
                            self.advance()
                        else:
                            right_oper=expr('0',x,None,function_call=Flag)
                            self.pos+=len(right_oper.right_op)-1
                            self.advance()

        print("in epr before return" ,self.current_char) 
        if oper_flg:
            return expr(left_oper,right_oper,oper)
        else:
            return left_oper

    def parse_cond(self):
        print("in cond")
        self.advance()
        a=['>','<','=']
        left=self.parse_expr(a)
        cond_op=self.current_co_word()
        self.pos+=len(cond_op)
        self.current_char = self.text[self.pos]
        right=self.parse_expr([')'])
        self.advance()
        return condition(left,cond_op,right)

    def parse_func_cal(self):
        stri=""
        a=[]
        while self.current_char is not ')':
            if self.current_char is '"' :
                stri=""
                stri+=self.current_char
                print(stri," yo in print ")
                self.advance()
                while self.current_char is not '"':
                    print(stri,"yo 2 in print ")
                    stri+=self.current_char
                    self.advance()
                print(stri,"stri")
                stri+=self.current_char
                print(stri,"stri \"")
                self.advance()
                print(self.current_char,"bobob")
                
            elif self.current_char is ',' :
                print("stri")
                a.append(stri)
                self.advance()
                stri=""
            else:
                stri+=self.current_char
                self.advance()

        a.append(stri)
        self.advance()
        return a

    def parse_func(self):
        self.pos+=7
        self.advance()
        name=self.current_word()
        self.pos+=len(name)-1
        self.advance()
        self.advance()
        arg=self.parse_func_cal()
        self.advance()
        self.pos+=4
        self.advance()
        a_fu=[]
        while self.current_char is not None:
            if(self.current_word()=="if"):
                a_fu.append(self.parse_if())
                self.advance()
            if(self.current_word()=="while"):
                a_fu.append(self.parse_wh())
                self.advance()
            if(self.current_word()=="print"):
                a_fu.append(self.parse_pr())
                self.advance()
            if(self.current_word()[:6]=="return"):
                self.pos+=5  #check
                self.advance()
                ret=self.current_word()
                self.advance()
                break
            else:
                a_fu.append(self.parse_assi())
                self.advance() 
        f_dict[name]=[a_fu,arg,ret]
        print("in par_fun before return" ,self.current_char)


        
        

#user_input = raw_input()
myfile=open("demmy.py",'r')
data=myfile.read()
#print data
a=Parser(data)
a.create_list()
b=a.statement_list[0].expri
# print(" asfas ",f_dict)
#print b.op_type,b.left_op.op_type,b.right_op.op_type,b.right_op.left_op.op_type
prog=main_prog(a.statement_list)
prog.eval(stack=state)
print("state",state)

            




        




















 








     