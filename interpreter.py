state={}
class main_prog(object):
    """docstring for main_prog"""
    def __init__(self, arg):
        self.arg = arg

    def eval(self):
        for x in self.arg:
            x.eval()
        
    

class if_block(main_prog):
    """docstring for if_block"""
    def __init__(self,cond,then=[],els=[]):
        self.cond = cond
        self.then = then
        self.els = els
    def eval(self):
        if self.cond.eval()==True:
            for statement in self.then:
                statement.eval()
        elif(self.els != None):
            for statement in self.els:
                statement.eval()



class while_block(main_prog):
    """docstring for while_block"""
    def __init__(self,cond,body=[]):
        self.cond = cond
        self.body = body
    def eval(self):
        while self.cond.eval() is True:
            for statement in self.body:
                statement.eval()
    

class print_stat(main_prog):
    """docstring for print_stat"""
    def __init__(self,stri=None):
        self.stri = stri

    def eval(self):
        #print "stri",self.stri
        for x in self.stri:
            if x[0]=='"':
                print(x[1:-1],end=" ")
            else:
                print(state[x],end=" ")
        print("")
            

        

class expr(main_prog):
    """docstring for expr"""
    def __init__(self,left_op,right_op,op_type):
        self.left_op = left_op
        self.right_op = right_op
        self.op_type = op_type

    def eval(self):
        if self.op_type!=None:
            if self.op_type == '+':
                a=self.left_op.eval() + self.right_op.eval()
                return a
            elif self.op_type == '-':
                a=self.left_op.eval() - self.right_op.eval()
                return a
            elif self.op_type == '*':
                a=self.left_op.eval() * self.right_op.eval()
                return a
            elif self.op_type == '/':
                a=self.left_op.eval() / self.right_op.eval()
                return a
            elif self.op_type == '%':
                a=self.left_op.eval() % self.right_op.eval()
                return a
            elif self.op_type == '**':
                a=self.left_op.eval() ** self.right_op.eval()
                return a
            else:
                raise ValueError('invalid operator')
        elif self.right_op==0:
            if self.left_op[0].isalpha():
                a=state[self.left_op]
                return a
            else:
                a=int(self.left_op)
                return a
        elif self.left_op==0:
            if self.right_op[0].isalpha():
                a=state[self.right_op]
                return a
            else:
                a=int(self.right_op)
                return a
            
        

class assi_statem(main_prog):
    """docstring for assi_statem"""
    def __init__(self,var,expri):
        self.var = var
        self.expri = expri

    def eval(self):
        state[self.var]=self.expri.eval()

        
class condition(main_prog):
    """docstring for condition"""
    def __init__(self,left,cond_op,right):
       self.left = left
       self.right =right
       self.cond_op=cond_op

    def eval(self):
        if self.cond_op == '>':
            a=self.left.eval() > self.right.eval()
            return a
        elif self.cond_op == '<':
            a=self.left.eval() < self.right.eval()
            return a
        elif self.cond_op == '<=':
            a=self.left.eval() <= self.right.eval()
            return a
        elif self.cond_op == '>=':
            a=self.left.eval() >= self.right.eval()
            return a
        elif self.cond_op == '==':
            a=self.left.eval() == self.right.eval()
            return a
                      




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
            while(self.current_char.isalpha() or self.current_char.isdigit()):
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
            return word_left+word_right

    def create_list(self):
        while self.current_char is not None:
            #print "current_word",self.current_word(),self.pos,self.current_char
            if(self.current_word()=="if"):
                self.statement_list.append(self.parse_if())
                self.advance()
                self.advance()
                #print "after if",self.current_char
            elif(self.current_word()=="while"):
                self.statement_list.append(self.parse_wh())
                self.advance()
                self.advance()
            elif(self.current_word()=="print"):
                self.statement_list.append(self.parse_pr())
                self.advance()
                self.advance()
            else:
                self.statement_list.append(self.parse_assi())
                self.advance()
                self.advance()
                #print "after assignment",self.current_char


    def parse_if(self):
        #print("in if")
        self.pos+=3 
        count=1
        a_if_then=[]    
        a_if_else=[]                               #create_exception
        self.current_char = self.text[self.pos]
        cond=self.parse_cond() 
        self.advance()
        self.advance()
        # raise expression for then
        self.pos+=(4+len("\n"))
        self.current_char = self.text[self.pos]
        while self.current_word()!="else":
            #print "current word in if ",self.current_word()
            if(self.current_word()=="if"):
                a_if_then.append(self.parse_if())
                self.advance()
                self.advance()
            if(self.current_word()=="while"):
                a_if_then.append(self.parse_wh())
                self.advance()
                self.advance()
            if(self.current_word()=="print"):
                a_if_then.append(self.parse_pr())
                self.advance()
                self.advance()
            if(self.current_word()=="fi"):
                self.pos+=2
                self.current_char = self.text[self.pos]
                flag=True
                #print self.current_char
                break
            else:
                a_if_then.append(self.parse_assi())
                self.advance()
                self.advance()


        if(flag==0):
            self.pos+=(4+len("\n"))
            while self.current_char is not None:
                if(self.current_word()=="if"):
                    a_if_else.append(self.parse_if())
                    self.advance()
                    self.advance()
                if(self.current_word()=="while"):
                    a_if_else.append(self.parse_wh())
                    self.advance()
                    self.advance()
                if(self.current_word()=="print"):
                    a_if_else.append(self.parse_pr())
                    self.advance()
                    self.advance()
                if(self.current_word()=="fi"):
                    self.pos+=2
                    self.current_char = self.text[self.pos]
                    flag=True  #raise exception
                    break
                else:
                    a_if_else.append(self.parse_assi())
                    self.advance()
                    self.advance()

        return if_block(cond,a_if_then,a_if_else)

    def parse_wh(self):
        #print("in while")
        self.pos+=6 
        a_wh=[]    
        self.current_char = self.text[self.pos]
        cond=self.parse_cond()
        self.advance()
        self.advance()
        # raise expression for then
        while self.current_char is not None:
            if(self.current_word()=="if"):
                a_wh.append(self.parse_if())
                self.advance()
                self.advance()
            if(self.current_word()=="while"):
                a_wh.append(self.parse_wh())
                self.advance()
                self.advance()
            if(self.current_word()=="print"):
                a_wh.append(self.parse_pr())
                self.advance()
                self.advance()
            if(self.current_word()=="done"):
                self.pos+=4
                self.current_char = self.text[self.pos]
                flag=True
                break
            else:
                a_wh.append(self.parse_assi())
                self.advance()
                self.advance()   

        return while_block(cond,a_wh)
    
    def parse_pr(self):
        #print("in print")
        self.pos+=5
        self.advance()
        stri=""
        a=[]
        while self.current_char is not ';':
            if self.current_char is ',' :
                self.advance()
                a.append(stri)
                stri=""
            stri+=self.current_char
            self.advance()
        a.append(stri)
        return print_stat(a)
        
    def parse_assi(self):
        #print "in assi"
        var=""
        while self.current_char is not '=':
            #print(self.current_char)
            var+=self.current_char
            self.advance()
        self.advance()
        expri=self.parse_expr([';'])
        return assi_statem(var,expri)


    def parse_expr(self,end):
        #print "in expre",

        oper_flg=False
        right_oper=0
        left_oper=0
        while self.current_char not in end:
            if(self.current_char=='('):
                #print(self.current_char)
                self.advance()
                if oper_flg==False:
                    left_oper=self.parse_expr([';'])
                else:
                    right_oper=self.parse_expr([';'])
                self.advance()

            elif(self.current_char in self.operators):
                #print(self.current_char)
                oper=self.current_char
                oper_flg=True
                self.advance()
            elif(self.current_char==')'):
                #print(self.current_char)
                
                return expr(left_oper,right_oper,oper)
            elif(self.current_char.isalpha() or self.current_char.isdigit()):
                #print(self.current_char)
                if oper_flg==False:
                    left_oper=expr(self.current_word(),0,None)
                    self.pos+=len(left_oper.left_op)
                    self.current_char=self.text[self.pos]
                else:
                    right_oper=expr(0,self.current_word(),None)
                    self.pos+=len(right_oper.right_op)
                    self.current_char=self.text[self.pos]
                
            #print "in epr before return" ,self.current_char 
        if oper_flg:
            return expr(left_oper,right_oper,oper)
        else:
            return left_oper

    def parse_cond(self):
        #print("in cond")
        left=self.parse_expr(self.cond_oper)
        cond_op=self.current_char
        self.advance()
        right=self.parse_expr([':'])
        return condition(left,cond_op,right)

#user_input = raw_input()
myfile=open("demmy.txt",'r')
data=myfile.read()
#print data
a=Parser(data)
a.create_list()
b=a.statement_list[0].expri
#print b.op_type,b.left_op.op_type,b.right_op.op_type,b.right_op.left_op.op_type
prog=main_prog(a.statement_list)
prog.eval()
#print state

            




        




















 








     