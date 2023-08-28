# -*- coding: utf-8 -*-
from aiida_worktree import node, WorkTree
from aiida.engine import calcfunction
import time
from aiida.orm import Int
from aiida.engine import WorkChain, calcfunction


@node()
@calcfunction
def add(x, y, t):
    time.sleep(t.value)
    return x + y


@node()
@calcfunction
def multiply(x, y, t):
    time.sleep(t.value)
    return x * y


def generate_add_multiply():

    add_multiply = WorkTree(name="test_add_multiply")
    add_multiply.nodes.new(add, "add1")
    add_multiply.nodes.new(multiply, "multiply1")
    add_multiply.links.new(
        add_multiply.nodes["add1"].outputs[0],
        add_multiply.nodes["multiply1"].inputs["x"],
    )
    return add_multiply


class AddAndMultiplyWorkChain(WorkChain):
    @classmethod
    def define(cls, spec):
        super().define(spec)
        spec.input("x")
        spec.input("y")
        spec.input("z")
        spec.outline(
            cls.add_multiply,
            cls.inspect_add_multiply,
            cls.add_multiply_2,
            cls.inspect_add_multiply_2,
            cls.results,
        )
        spec.output("sum")
        spec.output("product")

    def add_multiply(self):
        from aiida_worktree.engine.worktree import WorkTree

        add_multiply = generate_add_multiply()
        add_multiply.nodes["add1"].set(
            {"x": self.inputs.x, "y": self.inputs.y, "t": Int(10)}
        )
        add_multiply.nodes["multiply1"].set({"y": self.inputs.y, "t": Int(10)})
        ntdata = add_multiply.to_submit_dict()
        add_multiply.process = self.submit(WorkTree, **ntdata)
        self.ctx.wt_add_multiply = add_multiply.to_dict()
        self.to_context(**{"add_multiply": add_multiply.process})

    def inspect_add_multiply(self):
        from aiida_worktree import WorkTree

        wt_add_multiply = WorkTree.from_dict(self.ctx.wt_add_multiply)
        self.ctx.wt_add_multiply.update()
        self.ctx.sum = Int(1).store()
        # self.ctx.sum = self.ctx.wt_add_multiply.nodes["add1"].node.outputs.result

    def add_multiply_2(self):
        from aiida_worktree.engine.worktree import WorkTree

        add_multiply = generate_add_multiply()
        add_multiply.nodes["add1"].set(
            {"x": self.ctx.sum, "y": self.inputs.y, "t": Int(10)}
        )
        add_multiply.nodes["multiply1"].set({"y": self.inputs.y, "t": Int(10)})
        ntdata = add_multiply.to_submit_dict()
        add_multiply.process = self.submit(WorkTree, **ntdata)
        self.ctx.wt_add_multiply_2 = add_multiply.to_dict()
        self.to_context(**{"add_multiply_2": add_multiply.process})

    def inspect_add_multiply_2(self):
        self.ctx.wt_add_multiply_2.update()
        self.ctx.product = Int(2).store
        # self.ctx.product = self.ctx.wt_add_multiply_2.nodes["multiply1"].node.outputs.result

    def results(self):
        self.out("sum", self.ctx.sum)
        self.out("product", self.ctx.product)
