from visualinux import *
from visualinux.term import *
from visualinux.model.shape import *
from visualinux.runtime.state import *

from visualinux.evaluation import *

PlotTarget = Box | Container

class View:

    def __init__(self) -> None:
        self.globl = Box(name='Box', label='$', root=Term.CExpr('NULL'), type=None, absts=OrderedDict(), parent=None)
        self.subviews: dict[str, list[PlotTarget]] = {}

    def __str__(self) -> str:
        ss = 'View:\n'
        for name, targets in self.subviews.items():
            ss += f'  {name}:\n'
            for target in targets:
                ss += f'    plot {target!s}\n'
        return ss

    def sync(self) -> State:
        state = State()
        evaluation_result: OrderedDict[str, EvaluationCounter] = OrderedDict()
        for name, targets in self.subviews.items():
            try:
                evaluation_counter.reset()
                state.subviews[name] = show_time_usage(name, lambda: self.sync_subview(name, targets))
                # evaluation_show(name)
                evaluation_result[name] = evaluation_counter.clone()
            except Exception as e:
                print(f'subview {name} sync() error: ' + str(e))
                state.subviews[name] = Subview(name, error=True)
        for name, result in evaluation_result.items():
            pass
        return state

    def sync_subview(self, name: str, targets: list[PlotTarget]):
        subview = Subview(name)
        for shape in targets:
            if vl_debug_on(): printd(f'view eval shape = {shape.format_string_head()}')
            ent = shape.evaluate_on(subview.pool)
            if ent.key.startswith('0x0:'):
                continue
            subview.add_plot(ent.key)
        subview.do_postprocess()
        return subview
