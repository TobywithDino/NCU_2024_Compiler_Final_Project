import ply.yacc as yacc
from lex import lexer, tokens

# 紀錄變數的全域表
variables = {}


def evaluate(node, local_scope={}):
    scope = local_scope
    if type(node) == tuple:
        op = node[0] # 要做的事情
        if op == "define":
            variables[node[1]] = evaluate(node[2], scope)
        elif op == "print-num":
            result = evaluate(node[1], scope)
            if type(result) != int:
                raise TypeError(f'Type Error: Expect \'number\' but got {type(result)}')
            print(result)
        elif op == "print-bool":
            result = evaluate(node[1], scope)
            if type(result) != bool:
                raise TypeError(f'Type Error: Expect \'bool\' but got {type(result)}')
            print("#t") if result else print("#f")
        elif op == "+":
            result = 0
            for nd in node[1]:
                tmp = evaluate(nd, scope)
                if type(tmp) != int:
                    raise TypeError(f'Type Error: Expect \'number\' but got {type(tmp)}')
                result += tmp
            return result
        elif op == "-":
            a = evaluate(node[1], scope)
            b = evaluate(node[2], scope)
            if type(a) != int or type(b) != int:
                raise TypeError(f'Type Error: Expect \'number\' but got {type(a)} and {type(b)}')
            result = a - b
            return result
        elif op == "*":
            result = 1
            for nd in node[1]:
                tmp = evaluate(nd, scope)
                if type(tmp) != int:
                    raise TypeError(f'Type Error: Expect \'number\' but got {type(tmp)}')
                result *= tmp
            return result
        elif op == "/":
            a = evaluate(node[1], scope)
            b = evaluate(node[2], scope)
            if type(a) != int or type(b) != int:
                raise TypeError(f'Type Error: Expect \'number\' but got {type(a)} and {type(b)}')
            result = a // b
            return result
        elif op == "mod":
            a = evaluate(node[1], scope)
            b = evaluate(node[2], scope)
            if type(a) != int or type(b) != int:
                raise TypeError(f'Type Error: Expect \'number\' but got {type(a)} and {type(b)}')
            result = a % b
            return result
        elif op == ">":
            a = evaluate(node[1], scope)
            b = evaluate(node[2], scope)
            if type(a) != int or type(b) != int:
                raise TypeError(f'Type Error: Expect \'number\' but got {type(a)} and {type(b)}')
            return a > b
        elif op == "<":
            a = evaluate(node[1], scope)
            b = evaluate(node[2], scope)
            if type(a) != int or type(b) != int:
                raise TypeError(f'Type Error: Expect \'number\' but got {type(a)} and {type(b)}')
            return a < b
        elif op == "=":
            first = evaluate(node[1][0], scope)
            if type(first) != int:
                raise TypeError(f'Type Error: Expect \'number\' but got {type(first)}')
            for nd in node[1]:
                a = evaluate(nd, scope)
                if type(a) != int:
                    raise TypeError(f'Type Error: Expect \'number\' but got {type(first)}')
                result = (first == a)
            return result
        elif op == "and":
            result = True
            for nd in node[1]:
                a = evaluate(nd, scope)
                if type(a) != bool:
                    raise TypeError(f'Type Error: Expect \'bool\' but got {type(a)}')
                result = result and a
            return result
        elif op == "or":
            result = False
            for nd in node[1]:
                a = evaluate(nd, scope)
                if type(a) != bool:
                    raise TypeError(f'Type Error: Expect \'bool\' but got {type(a)}')
                result = result or a
            return result
        elif op == "not":
            a = evaluate(node[1], scope)
            if type(a) != bool:
                raise TypeError(f'Type Error: Expect \'bool\' but got {type(a)}')
            return not a
        elif op == "if":
            if evaluate(node[1], scope):
                return evaluate(node[2], scope)
            else:
                return evaluate(node[3], scope)
        elif op == "fun":
            # node 是 fun_exp 規則的，p[0] = (fun, ids, body)
            _, params, body = node
            if type(body) == tuple and body[0] == 'nest':   # 如果是nested function，body = ('nest', define stmt, exp)
                scope[body[1][1]] = evaluate(body[1][2])    # body[1][1]是內部函數變數名(fun_id)，body[1][2]是func_body(exp)，這行是外部函數拿來紀錄內部函數的變數
                body = body[2]                              # 紀錄完內部函數變數後，body變為原本(外部函數)的exp 
            return (params, body, scope)
        elif op == "call":
            # node 是 fun_call 規則的，p[0] = (call, fun_exp | id, args)
            func = evaluate(node[1], scope) # node[1] = fun_exp 或是 ID(定義過的函數，evaluate後一樣fun_exp),回傳一個函式func = (params, body, scope)
            args = [evaluate(arg, scope) for arg in node[2]] # 得到params_list 參數值，將其變成list型別
            if type(func) == tuple: # fun_exp
                params, body, closure_scope = func
                local_scope = {**closure_scope, **dict(zip(params, args))} # 紀錄函數變數的真實值，代到evaluate
                result = evaluate(body, local_scope)
                return result
            else:
                raise Exception('Invalid Function Call')
    elif type(node) == str:
        if node in scope: # 若node這個id是在scope中(函數定義的變數)，回傳scope中紀錄的argument值
            return scope[node]
        else:
            if node not in variables:
                raise Exception('Variable not defined')
            return variables[node]
    else:
        return node
        


# 定義規則
def p_program(p):
    '''program : stmt_list
    '''
    # $$ = $1
    p[0] = p[1]

def p_stmt_list(p):
    '''stmt_list : stmt stmt_list 
                 | stmt
    '''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]  # 若由stmt_list stmt變成stmt_list，則將兩個型別list相加
    else:
        p[0] = [p[1]] # 若由stmt變成stmt_list，則將stmt變成list型別

def p_stmt(p):
    '''stmt : exp
            | def_stmt
            | print_stmt
    '''
    p[0] = p[1]

def p_def_stmt(p):
    '''def_stmt : LPAREN DEFINE ID exp RPAREN
    '''
    p[0] = (p[2], p[3], p[4])

def p_print_stmt(p):
    '''print_stmt : LPAREN PRINT_NUM exp RPAREN
                  | LPAREN PRINT_BOOL exp RPAREN
    '''
    p[0] = (p[2], p[3])

def p_exp(p):
    '''exp : BOOL_VAL
           | NUMBER
           | ID
           | num_op
           | logical_op
           | fun_exp
           | fun_call
           | if_exp
    '''
    p[0] = p[1]

def p_num_op(p):
    '''num_op : LPAREN PLUS exp exps RPAREN
              | LPAREN MINUS exp exp RPAREN
              | LPAREN MULTIPLY exp exps RPAREN
              | LPAREN DIVIDE exp exp RPAREN
              | LPAREN MODULUS exp exp RPAREN
              | LPAREN GREATER exp exp RPAREN
              | LPAREN SMALLER exp exp RPAREN
              | LPAREN EQUAL exp exps RPAREN
    '''
    if p[2] in ['+', '*', '=']:
        p[0] = (p[2], [p[3]] + p[4])
    else:
        p[0] = (p[2], p[3], p[4])

def p_exp_list(p):
    '''exps : exp exps
            | exp
    '''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [p[1]]

def p_logical_op(p):
    '''logical_op : LPAREN AND exp exps RPAREN
                  | LPAREN OR exp exps RPAREN
                  | LPAREN NOT exp RPAREN
    '''
    if p[2] in ['and', 'or']:
        p[0] = (p[2], [p[3]] + p[4])
    elif p[2] == 'not':
        p[0] = (p[2], p[3])

def p_if_exp(p):
    '''if_exp : LPAREN IF test_exp then_exp else_exp RPAREN
    '''
    p[0] = (p[2], p[3], p[4], p[5])

def p_test_exp(p):
    '''test_exp : exp
    '''
    p[0] = p[1]

def p_then_exp(p):
    '''then_exp : exp
    '''
    p[0] = p[1]

def p_else_exp(p):
    '''else_exp : exp
    '''
    p[0] = p[1]

def p_fun_exp(p):
    '''fun_exp : LPAREN FUN LPAREN fun_ids RPAREN fun_body RPAREN
    '''
    p[0] = (p[2], p[4], p[6])  # 定義函數，包含參數列表和函數本體
    # p[6]有可能是(exp)或是('nest', define, exp)

def p_fun_ids(p):
    '''fun_ids : ID fun_ids
               |
    '''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = [p[1]] + p[2]

def p_fun_body(p):
    '''fun_body : exp
                | def_stmt exp
    '''
    if len(p) == 2: # 一般的函數(不包含nested函數)
        p[0] = p[1]
    else: # Nested函數
        p[0] = ('nest', p[1], p[2])

def p_fun_call(p):
    '''fun_call : LPAREN fun_exp param_list RPAREN
                | LPAREN ID param_list RPAREN
    '''
    p[0] = ('call', p[2], p[3])

def p_param_list(p):
    '''param_list : param param_list
                  |
    '''
    # 參數列表可能為空或是有一個以上
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = [p[1]] + p[2]

def p_param(p):
    '''param : exp
    '''
    p[0] = p[1]


# 錯誤處理(規則問題)
def p_error(p):
    raise SyntaxError("syntax error (no match rule)")

# 建立語法分析器
parser = yacc.yacc()

if __name__ == "__main__":
    data = """
(define foo (fun (x) (+ x 1)))
(print-num (abb 1) )
    """
    try:
        results = parser.parse(data)
        for r in results:
            evaluate(r)
    except Exception as e:
        print(f'error {e}')