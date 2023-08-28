from aiida import load_profile
from aiida.engine import submit, run
from aiida import load_profile
from aiida.orm import Int
from aiida_worktree.nodes.test_worktree import AddAndMultiplyWorkChain

load_profile()

# submit(AddAndMultiplyWorkChain, x=Int(1), y=Int(2), z=Int(3))
submit(AddAndMultiplyWorkChain, x=Int(1), y=Int(2), z=Int(3))
