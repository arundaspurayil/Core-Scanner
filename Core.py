from enum import Enum

Core = Enum('Core',
	'PROGRAM,\
	BEGIN,\
	END,\
	INT,\
	ENDFUNC,\
	IF,\
	THEN,\
	ELSE,\
	WHILE,\
	ENDWHILE,\
	ENDIF,\
	SEMICOLON,\
	LPAREN,\
	RPAREN,\
	COMMA,\
	ASSIGN,\
	NEGATION,\
	OR,\
	EQUAL,\
	LESS\
	LESSEQUAL,\
	ADD,\
	SUB,\
	MULT,\
	INPUT,\
	OUTPUT,\
	CONST,\
	ID,\
	EOS'
)
