import aiida

aiida.load_profile()


def test_node_wait(decorated_add):
    """Run simple calcfunction."""
    from aiida_workgraph import WorkGraph

    wg = WorkGraph(name="test_node_wait")
    add1 = wg.nodes.new(decorated_add, "add1", x=1, y=1)
    add1.to_ctx = [["result", "sum1"]]
    add2 = wg.nodes.new(decorated_add, "add2", x=2, y=2)
    add2.to_ctx = [["result", "sum2"]]
    add3 = wg.nodes.new(decorated_add, "add3", x="{{sum1}}", y="{{sum2}}")
    add3.wait = ["add1", add2]
    wg.submit(wait=True)
    add3.ctime < add1.ctime
    add3.ctime < add2.ctime
    assert add3.outputs[0].value == 6
