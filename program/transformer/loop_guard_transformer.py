from typing import List, Tuple
from .transformer import Transformer
from program import Program
from program.condition import Condition, TrueCond, And
from program.ifstatem import IfStatem


class LoopGuardTransformer(Transformer):
    """
    Transforms a program from "while guard: ..." to "while true: if guard: ..."
    Also it collapses simple top-level if-statements into a single if. For example:
    if cond1: if cond2: stuff end end
    turns into
    if cond1 and cond2: stuff end
    """

    def execute(self, program: Program) -> Program:
        statements, condition = self.__collapse_first_level_ifs__(program.loop_body)
        program.invariant = And(program.loop_guard, condition).simplify()
        program.loop_guard = TrueCond()
        if not isinstance(program.invariant, TrueCond):
            program.loop_body = [IfStatem([program.invariant], [statements])]
        return program

    def __collapse_first_level_ifs__(self, statements: List) -> Tuple[List, Condition]:
        if len(statements) != 1 or not isinstance(statements[0], IfStatem):
            return statements, TrueCond()

        if_statem: IfStatem = statements[0]
        if len(if_statem.branches) != 1 or if_statem.else_branch:
            return statements, TrueCond()

        branch_statms, branch_cond = self.__collapse_first_level_ifs__(if_statem.branches[0])
        condition = And(branch_cond, if_statem.conditions[0]).simplify()

        return branch_statms, condition
