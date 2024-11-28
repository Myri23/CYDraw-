from ply.lex import *
from ply.yacc import *

# Table des mots-clés
reserved = {
    'MOVE': 'MOVE',
    'DRAW': 'DRAW',
    'SET': 'SET',
    'COLOR': 'COLOR',
    'IF': 'IF',
    'THEN': 'THEN',
    'END': 'END',
    'FOR': 'FOR',
    'DO': 'DO',
    'IN': 'IN',
    # Directions
    'UP': 'DIRECTION',
    'DOWN': 'DIRECTION',
    'LEFT': 'DIRECTION',
    'RIGHT': 'DIRECTION',
    # Formes
    'CIRCLE': 'FORM',
    'SQUARE': 'FORM',
    'LINE': 'FORM',
}
# Liste des tokens (mots-clés + autres tokens)
tokens = (
    'NUMBER', 'COMMA', 'EQUAL', 'ID',
    'DIRECTION', 'FORM', 'LEFT_PARENTHESE', 'RIGHT_PARENTHESE'
) + tuple(reserved.values())

# Expressions régulières pour les tokens simples
t_EQUAL = r'='
t_COMMA = r','
t_LEFT_PARENTHESE = r'\('
t_RIGHT_PARENTHESE = r'\)'

# Ignorer les espaces et les tabulations
t_ignore = ' \t\n'

# Nombre
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Identifiants et mots-clés
def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')  # Vérifie si c'est un mot-clé, sinon c'est un ID
    return t

# Gestion des erreurs lexicales
def t_error(t):
    print(f"Erreur lexicale : caractère non reconnu '{t.value[0]}'")
    t.lexer.skip(1)

# Construction du lexer
lexer = lex()

# ----------------------------------------
# Définition de la grammaire PLY (parser)
# ----------------------------------------

# Règles de parsing
def p_program(p):
    '''program : statement
               | statement program'''
    if len(p) == 2:  # Cas de base : un seul statement
        p[0] = [p[1]]
    else:  # Cas récursif : un statement suivi d'un program
        p[0] = [p[1]] + p[2]

def p_statement_movement(p):
    'statement : MOVE DIRECTION NUMBER'
    p[0] = f"Mouvement : {p[1]} {p[2]} {p[3]}"
    print(f"Mouvement : {p[1]} {p[2]} {p[3]}")

def p_statement_drawing(p):
    'statement : DRAW FORM NUMBER COMMA NUMBER'
    p[0] = f"Dessiner : {p[1]} {p[2]} avec les paramètres {p[3]}, {p[5]}"
    print(f"Dessiner : {p[1]} {p[2]} avec les paramètres {p[3]}, {p[5]}")

def p_statement_condition(p):
    'statement : IF condition THEN program END'
    p[0] = f"Condition : Si {p[2]}, alors {p[4]}"
    print(f"Condition : Si {p[2]}, alors {p[4]}")

def p_statement_loop(p):
    'statement : FOR ID IN LEFT_PARENTHESE NUMBER COMMA NUMBER RIGHT_PARENTHESE DO program END'
    p[0] = f"Boucle : {p[2]} de {p[5]} à {p[7]} avec instructions {p[10]}"
    print(f"Boucle : {p[2]} de {p[5]} à {p[7]}")

def p_statement_assign(p):
    'statement : ID EQUAL NUMBER'
    print(f"Assignation : {p[1]} = {p[3]}")

def p_condition(p):
    'condition : ID'
    p[0] = p[1]

# Gestion des erreurs de syntaxe
def p_error(p):
    if p:
        print(f"Erreur de syntaxe à '{p.value}'")
    else:
        print("Erreur de syntaxe : fin inattendue du fichier")

# Construction du parser
parser = yacc()

# ----------------------------------------
# Exemple d'exécution
# ----------------------------------------

data =    '''
MOVE UP 10
DRAW CIRCLE 50, 50
IF x THEN MOVE DOWN 5 END
FOR i IN (1,10) DO MOVE LEFT 5 END
'''

# Analyse lexicale
lexer.input(data)

print("Tokens :")
for token in lexer:
    print(token)

# Analyse syntaxique
print("\nParsing :")
parser.parse(data)

