from typing import List


class StatementTracer:

    @staticmethod
    def trace_function_definition(node):
        if node.type in ['function_definition']:#, 'function_declarator']:
            start_point = node.start_point[0]
            end_point = node.end_point[0]
            nodes = node.children

            if node.type == 'function_definition':
                for node in nodes:
                    if node.type == 'function_declarator':
                        nodes = node.children
                        break

            for node in nodes:
                if node.type == 'identifier':
                    func_name = node.text.decode("utf-8")
                    traced = {
                        'name': func_name,
                        'start_line': start_point,
                        'end_line': end_point,
                    }
                    return traced
        return None

    @staticmethod
    def trace_ast(node):
        traced = node.type
        return traced


    @staticmethod
    def trace_function_data(node, code:list, file_name:str, commit_sha:str, **kwargs):
        if node.type in ['function_definition']:#, 'function_declarator']:
            start_point = node.start_point[0]
            end_point = node.end_point[0]
            nodes = node.children

            if node.type == 'function_definition':
                for node in nodes:
                    if node.type == 'function_declarator':
                        nodes = node.children
                        break

            for node in nodes:
                if node.type == 'identifier':
                    func_name = node.text.decode("utf-8")
                    traced = {
                        'func': func_name,
                        'file': file_name,
                        'commit_sha': commit_sha,
                        'start_line': start_point,
                        'end_line': end_point,
                        'code_text': '\n'.join(code[start_point:end_point+1]) 
                    }
                    return traced
        return None


    @staticmethod
    def trace_specify_node_ast(node, node_points:List[int]):
        if node.start_point[0] in node_points:
            return node.type#, node.text
        return


    @staticmethod
    def trace_specify_nodes(node, node_points:List[int]):
        if (point:= node.start_point[0]) in node_points:
            return point, node
        return None