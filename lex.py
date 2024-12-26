import ply.lex as lex

# 定義tokens
tokens = [
    'NUMBER',
    'BOOL_VAL',
    'ID',
    'LPAREN',
    'RPAREN',

    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    'MODULUS',
    'GREATER',
    'SMALLER',
    'EQUAL',

    'DEFINE', 
    'PRINT_NUM', 
    'PRINT_BOOL', 
     
    'AND', 
    'OR', 
    'NOT',

    'IF',
    'FUN'
]  

# Type:NUMBER, Value:整數
def t_NUMBER(t):
    r'0|(-?[1-9]\d*)'
    t.value = int(t.value)
    return t

# Type:BOOL_VAL, Value:布林值
def t_BOOL_VAL(t):
    r'\#t|\#f'
    t.value = True if t.value == '#t' else False
    return t

# Type:ID
def t_ID(t):
    r'[a-zA-Z]([a-zA-Z0-9\-])*'

    # 檢查是不是關鍵字，如果是則將Type改成關鍵字
    t.type = {
        'print-num': 'PRINT_NUM',
        'print-bool': 'PRINT_BOOL',
        'define': 'DEFINE',
        'and': 'AND',
        'or': 'OR',
        'not': 'NOT',
        'if': 'IF',
        'mod': 'MODULUS',
        'fun': 'FUN'
    }.get(t.value, 'ID')
    return t

# 忽略分隔符
t_ignore = ' \t\n\r'

# 定義符號Type的規則
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_PLUS      = r'\+'
t_MINUS     = r'-'
t_MULTIPLY  = r'\*'
t_DIVIDE    = r'/'
t_GREATER   = r'>'
t_SMALLER   = r'<'
t_EQUAL     = r'='

# 錯誤處理(處理沒定義的符號)
def t_error(t):
    raise SyntaxError("syntax error (symbol undefined)")

# 建立詞法分析器
lexer = lex.lex()