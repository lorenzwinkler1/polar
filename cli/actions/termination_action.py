from argparse import Namespace

from termcolor import colored

from cli.common import get_moment
from inputparser.goal_parser import MOMENT, GoalParser
from inputparser.parser import parse_program
from program.condition.condition import Condition
from program.condition.true_cond import TrueCond
from program.transformer import normalize_program
from recurrences.rec_builder import RecBuilder
from termination.termination_condition import TerminationCondition
from .action import Action


class TerminationAction(Action):
    loop_guard: Condition

    def __init__(self, cli_args: Namespace):
        self.cli_args = cli_args

    def __call__(self, *args, **kwargs):
        benchmark = args[0]
        program = parse_program(benchmark)
        self.loop_guard = program.loop_guard
        if program.is_probabilistic:
            raise NotImplementedError("Only deterministic programs are supported by termination analysis")
        # remove the loop condition from the program to allow for normalization
        program.loop_guard = TrueCond()
        program = normalize_program(program)
        goal_strings = [f"{symbol}" for symbol in self.loop_guard.get_free_symbols()]
        goals = [GoalParser.parse(goal) for goal in goal_strings]

        closed_forms = self.get_closed_forms(goals, program)
        self.handle_termination(closed_forms)

    def get_closed_forms(self, goals, program):
        solvers = {}
        rec_builder = RecBuilder(program)

        closed_forms = {}
        for goal_type, goal_data in goals:
            if goal_type != MOMENT:
                print(colored(f"Only Moment goals (not {goal_type}) are supported in termination analysis at the moment."))
            monom = goal_data[0]
            moment, is_exact = get_moment(
                monom, solvers, rec_builder, self.cli_args, program
            )
            id = goal_data[0]
            closed_forms[id] = moment
        return closed_forms

    def handle_termination(self, closed_forms):
        print()
        print(colored("-------------------", "cyan"))
        print(colored("-   Termination   -", "cyan"))
        print(colored("-------------------", "cyan"))
        print()

        # normalze the termination condition
        termination_condition = TerminationCondition(self.loop_guard, closed_forms)

        witness = termination_condition.get_witness()

        if witness is None:
            print("Program termination could not be determined")
            return
        if witness.is_termination_witness():
            print(colored("Program terminates. Witness found:", "green"))
        else:
            print(colored("Program does not terminate. Witness found:", "green"))
        print(witness)
