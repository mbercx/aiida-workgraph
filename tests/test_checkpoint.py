import aiida
import os

aiida.load_profile()


def test_checkpoint(decorated_delay_add):
    from aiida_worktree import WorkTree
    import time

    wt = WorkTree(name="test_checkpoint")
    add1 = wt.nodes.new(decorated_delay_add, "add1", x=1, y=2, t=10)
    add2 = wt.nodes.new(decorated_delay_add, "add2", y=2, t=10)
    add3 = wt.nodes.new(decorated_delay_add, "add3", y=2, t=10)
    add4 = wt.nodes.new(decorated_delay_add, "add4", y=2, t=10)
    wt.links.new(add1.outputs[0], add2.inputs[0])
    wt.links.new(add2.outputs[0], add3.inputs[0])
    wt.links.new(add3.outputs[0], add4.inputs[0])
    wt.submit(wait=True)
    time.sleep(10)
    os.system("verdi daemon restart")
    time.sleep(10)
    wt.wait(timeout=100)
    assert wt.nodes["add4"].node.outputs.result == 9


def test_checkpoint_2(decorated_delay_add):
    from aiida_worktree import WorkTree
    import time

    wt = WorkTree(name="test_checkpoint")
    add1 = wt.nodes.new(decorated_delay_add, "add1", x=1, y=2, t=10)
    add21 = wt.nodes.new(decorated_delay_add, "add21", y=2, t=1)
    add22 = wt.nodes.new(decorated_delay_add, "add22", y=2, t=20)
    add31 = wt.nodes.new(decorated_delay_add, "add31", y=2, t=1)
    add32 = wt.nodes.new(decorated_delay_add, "add32", y=2, t=20)
    add4 = wt.nodes.new(decorated_delay_add, "add4", t=10)
    wt.links.new(add1.outputs[0], add21.inputs[0])
    wt.links.new(add1.outputs[0], add22.inputs[0])
    wt.links.new(add21.outputs[0], add31.inputs[0])
    wt.links.new(add22.outputs[0], add32.inputs[0])
    wt.links.new(add31.outputs[0], add4.inputs[0])
    wt.links.new(add32.outputs[0], add4.inputs[1])
    wt.submit(wait=True)
    # time.sleep(10)
    # os.system('verdi daemon restart')
    # time.sleep(10)
    wt.wait(timeout=100)
    assert wt.nodes["add4"].node.outputs.result == 14
