import aiida
import time
import pytest

aiida.load_profile()


def test_run_order(wg_engine):
    """Test the order.
    Nodes should run in parallel and only depend on the input nodes."""
    wg = wg_engine
    wg.submit(wait=True)
    wg.nodes["add2"].ctime < wg.nodes["add4"].ctime


@pytest.mark.skip(reason="The test is not stable.")
def test_reset_node(wg_engine):
    """Modify a node during the excution of a WorkGraph."""
    wg = wg_engine
    wg.name = "test_reset"
    wg.submit()
    time.sleep(15)
    wg.nodes["add3"].set({"y": aiida.orm.Int(10).store()})
    wg.save()
    wg.wait()
    wg.update()
    assert wg.nodes["add5"].node.outputs.sum == 21
    assert wg.process.base.extras.get("workgraph_queue_index") == 1
    assert len(wg.process.base.extras.get("workgraph_queue")) == 1


def test_max_number_jobs():
    from aiida_workgraph import WorkGraph, build_node
    from aiida.orm import load_code
    from aiida.orm import Int

    # Use the calcjob: ArithmeticAddCalculation
    arithmetic_add = build_node(
        "aiida.calculations.arithmetic.add.ArithmeticAddCalculation"
    )
    code = load_code("add@localhost")

    wg = WorkGraph("test_max_number_jobs")
    N = 15
    # Create N nodes
    for i in range(N):
        temp = wg.nodes.new(
            arithmetic_add, name=f"add{i}", x=Int(1), y=Int(1), code=code
        )
        # Set a sleep option for each job (e.g., 2 seconds per job)
        temp.set({"metadata.options.sleep": 2})

    # Set the maximum number of running jobs inside the WorkGraph
    wg.max_number_jobs = 5
    wg.submit(wait=True)
    wg.nodes["add2"].ctime < wg.nodes["add10"].ctime
