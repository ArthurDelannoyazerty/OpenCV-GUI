import re
from qtpy.QtWidgets import QDockWidget
from NodeGraphQt import (
    NodeGraph,
    PropertiesBinWidget,
    NodesTreeWidget,
    NodesPaletteWidget
)

from NodeGraphQt import BaseNode
# from examples.nodes import basic_nodes


# UI: create the widget wrapper that can be docked to the main window.
class NodeGraphPanel(QDockWidget):
    """
    Widget wrapper for the node graph that can be docked to
    the main window.
    """
    def __init__(self, graph, parent=None):
        super(NodeGraphPanel, self).__init__(parent)
        self.setObjectName('nodeGraphQt.NodeGraphPanel')
        self.setWindowTitle('CV2 pipeline visualisation')
        self.setWidget(graph.widget)

# utils
def slugify(s):
    return re.sub(r'[^a-z0-9-]', r'', s.lower()).replace('-', '_')

# Below individual NodeGraph default constructor (1-in => 1-out)
def node_constructor(self):
    BaseNode.__init__(self)
    self.add_input('in A')
    self.add_output('out A')

class CvNodeGraph():
    def __init__(self, main_window):
        self.main_window = main_window
        self.graph = graph = NodeGraph()
        self.panel = NodeGraphPanel(graph)

        for key, value in self.main_window.transformer.commands.items():
            if 'inputs' in value:
                # Defines dynamic class input/output/colors/labels based on `commands.txt`
                pass
            else:
                # A default class for command with simple 1-in/1-out
                cls = type(slugify(key), (BaseNode, ), {
                    # acts as a namespace
                    "__identifier__": 'nodes.transform',
                    "NODE_NAME": key,
                    "__init__": node_constructor
                })
                print("register", cls)
                graph.register_node(cls)


    def add_node(self, pipelineitem):
        key = 'nodes.transform' + '.' + slugify(pipelineitem.transformation_item.name)
        print("adding node to graph:", key)
        self.graph.create_node(key, text_color='#feab20')

