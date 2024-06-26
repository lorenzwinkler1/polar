from .dist_transformer import DistTransformer
from .if_transformer import IfTransformer
from .multi_assign_transformer import MultiAssignTransformer
from .type_inferer import TypeInferer
from .conditions_to_arithm import ConditionsToArithm
from .update_info_transformer import UpdateInfoTransformer
from .conditions_reducer import ConditionsReducer
from .conditions_normalizer import ConditionsNormalizer
from .constants_transformer import ConstantsTransformer
from .loop_guard_transformer import LoopGuardTransformer
from ..program import Program
from ..assignment import FunctionalAssignment
import settings


def normalize_program(program: Program) -> Program:
    # Transform the loop-guard into an if-statement
    program = LoopGuardTransformer().execute(program)
    # Transform non-constant distributions parameters
    program = DistTransformer().execute(program)
    # Flatten if-statements
    program = IfTransformer().execute(program)
    # Make sure every variable has only 1 assignment
    program = MultiAssignTransformer().execute(program)
    # Create aliases for expressions in conditions.
    program = ConditionsReducer().execute(program)
    # Replace/Add constants in loop body
    program = ConstantsTransformer().execute(program)
    # Update program info like variables and symbols
    program = UpdateInfoTransformer(ignore_unsolvability=True).execute(program)
    # Infer types for variables
    if not settings.disable_type_inference:
        program = TypeInferer().execute(program)
    # Update dependency graph (because finite variables are now detected)
    program = UpdateInfoTransformer().execute(program)
    # Turn all conditions into normalized form
    program = ConditionsNormalizer().execute(program)
    # Convert all conditions to arithmetic
    if settings.cond2arithm:
        program = ConditionsToArithm().execute(program)
    # Pass the "exact functional moments" parameter to the FunctionalAssignment class
    FunctionalAssignment.exact_func_moments = settings.exact_func_moments

    return program
