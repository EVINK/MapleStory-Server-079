"""
Eval - Converted from Java source
Original: tools/Eval.java
Package: tools
"""

from enum import Enum, IntEnum
from typing import Dict
from typing import Optional, Any
import math


class Eval:
    """
    Class Eval
    """

    def __init__(self, expression: str):
        self.rootOperation = None
        self.string = None
        self.position = 0
        self.pushedBackOperator = None
        self.tokeniser = None
        self.rootOperation = Compiler(expression).compile()

    # Static initializer
    # Tokeniser.START_NEW_EXPRESSION = '('


    def eval(self, expression: str, variables: dict) -> Any:
        return Eval(expression).eval(variables)

    def eval_expression(self, expression: str) -> Any:
        return Eval(expression).eval()

    def eval_variables(self, variables: dict) -> Any:
        return self.rootOperation.eval(variables)

    def toString(self) -> str:
        return self.rootOperation

    def getBigDecimal(self) -> Any:
        len = self.string
        start = self.position
        ch = None
        while self.position < len and (Character.isDigit(ch = self.string[self.position]) or ch == '.'):
            self.position += 1
        if self.position < len and ((ch = self.string[self.position]) == 'E' or ch == 'e'):
            self.position += 1
            if self.position < len and ((ch = self.string[self.position]) == '+' or ch == '-'):
                self.position += 1
            while self.position < len and Character.isDigit(ch = self.string[self.position]):
                self.position += 1
        return BigDecimal(self.string[start:self.position])

    def validateOperandType(self, operand: Any, type: Any) -> None:
        operandType = None
        if isinstance(operand, Operation) and (operandType = (operand).type) != type:
            raise RuntimeError("cannot use " + operandType.name + " operands with " + type.name + " operators")

    def evaluateOperand(self, operand: Any, variables: dict) -> Any:
        if isinstance(operand, Operation):
            return (operand).eval(variables)
        if not (isinstance(operand, String)):
            return operand
        value = None
        if variables is None or (value = variables.get(operand)) is None:
            raise RuntimeError("no value for variable \"" + operand + "\"")
        return value

    def compile(self, preReadOperand: Any, preReadOperator: Any, nestingLevel: int, endOfExpressionChar: str, terminatePrecedence: int) -> Any:
        operand = (preReadOperand is not None) ? preReadOperand : self.getOperand(nestingLevel)
        operator = (preReadOperator is not None) ? preReadOperator : self.tokeniser.getOperator(endOfExpressionChar)
        while operator != Operator.END:
            if operator == Operator.TERNARY:
                operand2 = self.compile(None, None, nestingLevel, ':', -1)
                operand3 = self.compile(None, None, nestingLevel, endOfExpressionChar, -1)
                operand = Operation.tenaryOperationFactory(operator, operand, operand2, operand3)
                operator = Operator.END
            else:
                nextOperand = self.getOperand(nestingLevel)
                nextOperator = self.tokeniser.getOperator(endOfExpressionChar)
                if nextOperator == Operator.END:
                    operand = Operation.binaryOperationfactory(operator, operand, nextOperand)
                    operator = Operator.END
                    if preReadOperator is None or endOfExpressionChar == '\0':
                        continue
                    self.tokeniser.pushBack(Operator.END)
                elif nextOperator.precedence <= terminatePrecedence:
                    operand = Operation.binaryOperationfactory(operator, operand, nextOperand)
                    self.tokeniser.pushBack(nextOperator)
                    operator = Operator.END
                elif operator.precedence >= nextOperator.precedence:
                    operand = Operation.binaryOperationfactory(operator, operand, nextOperand)
                    operator = nextOperator
                else:
                    operand = Operation.binaryOperationfactory(operator, operand, self.compile(nextOperand, nextOperator, nestingLevel, endOfExpressionChar, operator.precedence))
                    operator = self.tokeniser.getOperator(endOfExpressionChar)
                    if operator != Operator.END or preReadOperator is None or endOfExpressionChar == '\0':
                        continue
                    self.tokeniser.pushBack(Operator.END)
        return operand

    def getOperand(self, nestingLevel: int) -> Any:
        operand = self.tokeniser.getOperand()
        if operand == Tokeniser.START_NEW_EXPRESSION:
            operand = self.compile(None, None, nestingLevel + 1, ')', -1)
        elif isinstance(operand, Operator):
            return Operation.unaryOperationfactory(operand, self.getOperand(nestingLevel))
        return operand


# Inner class from Java (originally nested)
class Type(Enum):
    """Enum Type"""

    ARITHMETIC = ("arithmetic")
    BOOLEAN = ("boolean")

    def __init__(self, name):
        self._name = name


# Inner class from Java (originally nested)
class Tokeniser:
    """
    Class Tokeniser
    """

    def __init__(self):
        self.string = None
        self.position = 0
        self.pushedBackOperator = None

    # Static initializer
    # Tokeniser.START_NEW_EXPRESSION = '('


    def getBigDecimal(self) -> Any:
        len = self.string
        start = self.position
        ch = None
        while self.position < len and (Character.isDigit(ch = self.string[self.position]) or ch == '.'):
            self.position += 1
        if self.position < len and ((ch = self.string[self.position]) == 'E' or ch == 'e'):
            self.position += 1
            if self.position < len and ((ch = self.string[self.position]) == '+' or ch == '-'):
                self.position += 1
            while self.position < len and Character.isDigit(ch = self.string[self.position]):
                self.position += 1
        return BigDecimal(self.string[start:self.position])

    def toString(self) -> str:
        return self.string[0:self.position] + ">>>" + self.string[self.position:]


# Inner class from Java (originally nested)
class Operator(Enum):
    """Enum Operator"""

    END = (-1, 0, (String)null, (Type)null, (Type)null) {
            @Override
            BigDecimal perform(final BigDecimal value1, final BigDecimal value2, final BigDecimal value3) {
                throw new RuntimeException("END is a dummy operation")

    def __init__(self, precedence, numberOfOperands, string, resultType, operandType):
        self._precedence = precedence
        self._numberOfOperands = numberOfOperands
        self._string = string
        self._resultType = resultType
        self._operandType = operandType


# Inner class from Java (originally nested)
class Operation:
    """
    Class Operation
    """

    def __init__(self, type: Any, operator: Any, operand1: Any, operand2: Any, operand3: Any):
        self.type = type
        self.operator = operator
        self.operand1 = operand1
        self.operand2 = operand2
        self.operand3 = operand3


    def validateOperandType(self, operand: Any, type: Any) -> None:
        operandType = None
        if isinstance(operand, Operation) and (operandType = (operand).type) != type:
            raise RuntimeError("cannot use " + operandType.name + " operands with " + type.name + " operators")

    def evaluateOperand(self, operand: Any, variables: dict) -> Any:
        if isinstance(operand, Operation):
            return (operand).eval(variables)
        if not (isinstance(operand, String)):
            return operand
        value = None
        if variables is None or (value = variables.get(operand)) is None:
            raise RuntimeError("no value for variable \"" + operand + "\"")
        return value

    def toString(self) -> str:
        # switch (self.operator.numberOfOperands):
            # case 3:
                return "(" + self.operand1 + self.operator.string + self.operand2 + ":" + self.operand3 + ")"
            # case 2:
                return "(" + self.operand1 + self.operator.string + self.operand2 + ")"
            # default:
                return "(" + self.operator.string + self.operand1 + ")"


# Inner class from Java (originally nested)
class Compiler:
    """
    Class Compiler
    """

    def __init__(self):
        self.tokeniser = None


    def compile(self, preReadOperand: Any, preReadOperator: Any, nestingLevel: int, endOfExpressionChar: str, terminatePrecedence: int) -> Any:
        operand = (preReadOperand is not None) ? preReadOperand : self.getOperand(nestingLevel)
        operator = (preReadOperator is not None) ? preReadOperator : self.tokeniser.getOperator(endOfExpressionChar)
        while operator != Operator.END:
            if operator == Operator.TERNARY:
                operand2 = self.compile(None, None, nestingLevel, ':', -1)
                operand3 = self.compile(None, None, nestingLevel, endOfExpressionChar, -1)
                operand = Operation.tenaryOperationFactory(operator, operand, operand2, operand3)
                operator = Operator.END
            else:
                nextOperand = self.getOperand(nestingLevel)
                nextOperator = self.tokeniser.getOperator(endOfExpressionChar)
                if nextOperator == Operator.END:
                    operand = Operation.binaryOperationfactory(operator, operand, nextOperand)
                    operator = Operator.END
                    if preReadOperator is None or endOfExpressionChar == '\0':
                        continue
                    self.tokeniser.pushBack(Operator.END)
                elif nextOperator.precedence <= terminatePrecedence:
                    operand = Operation.binaryOperationfactory(operator, operand, nextOperand)
                    self.tokeniser.pushBack(nextOperator)
                    operator = Operator.END
                elif operator.precedence >= nextOperator.precedence:
                    operand = Operation.binaryOperationfactory(operator, operand, nextOperand)
                    operator = nextOperator
                else:
                    operand = Operation.binaryOperationfactory(operator, operand, self.compile(nextOperand, nextOperator, nestingLevel, endOfExpressionChar, operator.precedence))
                    operator = self.tokeniser.getOperator(endOfExpressionChar)
                    if operator != Operator.END or preReadOperator is None or endOfExpressionChar == '\0':
                        continue
                    self.tokeniser.pushBack(Operator.END)
        return operand

    def getOperand(self, nestingLevel: int) -> Any:
        operand = self.tokeniser.getOperand()
        if operand == Tokeniser.START_NEW_EXPRESSION:
            operand = self.compile(None, None, nestingLevel + 1, ')', -1)
        elif isinstance(operand, Operator):
            return Operation.unaryOperationfactory(operand, self.getOperand(nestingLevel))
        return operand

