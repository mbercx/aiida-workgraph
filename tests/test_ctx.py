import aiida

aiida.load_profile()


def test_workgraph_ctx(decorated_add):
    """Set/get data to/from context."""
    from aiida_workgraph import WorkGraph
    from aiida.orm import Float

    wg = WorkGraph(name="test_workgraph_ctx")
    wg.ctx = {"x": Float(2), "data.y": Float(3)}
    add1 = wg.nodes.new(decorated_add, "add1", x="{{x}}", y="{{data.y}}")
    wg.submit(wait=True)
    assert add1.outputs["result"].value == 5


def test_node_to_ctx(decorated_add):
    """Set/get data to/from context."""
    from aiida_workgraph import WorkGraph
    from aiida.orm import Float

    wg = WorkGraph(name="test_node_to_ctx")
    add1 = wg.nodes.new(decorated_add, "add1", x=Float(2).store(), y=Float(3).store())
    add1.to_ctx = [["result", "sum"]]
    add2 = wg.nodes.new(decorated_add, "add2", y="{{ sum }}")
    wg.links.new(add1.outputs[0], add2.inputs["x"])
    wg.submit(wait=True)
    assert add2.outputs["result"].value == 10
