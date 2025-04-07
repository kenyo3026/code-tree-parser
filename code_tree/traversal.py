from types import FunctionType
from typing import Union, Tuple, Dict

import tree_sitter


class DFSTraversal():
    """ The base class of Depth First Search Traversal. """
    def __init__(self, trace_strategy:Union[Tuple[FunctionType, Dict], FunctionType]=None, store_strategy:str=None, step_threshold:int=3000):
        self.total_step = 0
        self.step_threshold = step_threshold
        self.cursor = None
        self.caches = []
        self.nodes = []
        self.traced = {} if store_strategy else []
        self.ignore_type = ['initializer_list']
        if isinstance(trace_strategy, tuple):
            self.trace_strategy, self.trace_kwargs = trace_strategy
        elif callable(trace_strategy):
            self.trace_strategy, self.trace_kwargs = trace_strategy, {}
        else:
            self.trace_strategy, self.trace_kwargs = None, 0
        self.store_strategy = store_strategy


    def _traverse(self, came_up:bool):
        """ The function mainly used for recursive traversal process.

        Args:
            camp_up (bool): the bool status of the current state of tree traversal.
        """
        self.step += 1
        if self.step == self.step_threshold:
            return

        if not came_up:
            self.nodes.append(self.cursor.node)

            if self.trace_strategy and callable(self.trace_strategy):
                if traced:= self.trace_strategy(self.cursor.node, **self.trace_kwargs):
                    if not self.store_strategy:
                        self.traced.append(traced)
                    elif self.store_strategy == 'dict':
                        value = traced.pop(self.store_strategy)
                        self.traced[value] = traced
                    elif self.store_strategy == 'dict_append':
                        key, value = traced
                        if key in self.traced:
                            self.traced[key].append(value)
                        else:
                            self.traced[key] = [value]
            if self.cursor.node.type in self.ignore_type:
                self._traverse(True)
            elif (self.cursor.goto_first_child()):
                self._traverse(False)
            elif (self.cursor.goto_next_sibling()):
                self._traverse(False)
            elif (self.cursor.goto_parent()):
                self._traverse(True)
        else:
            if (self.cursor.goto_next_sibling()):
                self._traverse(False)
            elif (self.cursor.goto_parent()):
                self._traverse(True)
        
        return self.cursor


    def traverse(self, cursor:tree_sitter.TreeCursor):
        """ Perform DFS traversal for cst/ast tree. 
        
        Args:
            cursor  (tree_sitter.TreeCursor): the current cst/ast tree cursor.

        Returns:
            nodes (list): the list with all the nodes of tree.
            state_nodes (dict): the dict with the qualifying program statement nodes.
        """
        origin_node = cursor.node
        self.cursor = cursor
        self.step = 0
        self.cursor = self._traverse(False)
        self.total_step += self.step

        while self.cursor.node != origin_node:
            self.step = 0
            self.cursor = self._traverse(False)
            self.total_step += self.step

        return self.traced