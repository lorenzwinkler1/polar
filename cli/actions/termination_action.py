from argparse import Namespace

from inputparser.parser import parse_program
from program.condition.true_cond import TrueCond
from program.transformer import normalize_program
from termination.termination_analyzer import TerminationAnalyzer
from .action import Action


class TerminationAction(Action):

    def __init__(self, cli_args: Namespace):
        self.cli_args = cli_args

    def __call__(self, *args, **kwargs):
        benchmark = args[0]
        program = parse_program(benchmark)
        guard = program.loop_guard
        if program.is_probabilistic:
            raise NotImplementedError("Only deterministic programs are supported by termination analysis")
        # remove the loop condition from the program to allow for normalization
        program.loop_guard = TrueCond()
        program = normalize_program(program)

        TerminationAnalyzer.analyze(program, guard)
