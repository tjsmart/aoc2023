import ast


def rewrite_312(src: str) -> str:
    """
    rewrite 3.12 to 3.10 for pypy support
    """
    lines = src.splitlines()
    root = ast.parse(src)

    type_nodes: list[ast.AST] = []
    rw = False
    for node in ast.walk(root):
        match node:
            case ast.FunctionDef() | ast.ClassDef():
                if node.type_params:
                    line = lines[node.lineno - 1]
                    start, _, rest = line.partition('[')
                    _, _, end = rest.partition(']')
                    lines[node.lineno - 1] = start + end
                    rw = True

            case ast.TypeVar() | ast.ParamSpec() | ast.TypeVarTuple():
                type_nodes.append(node)
                rw = True

            case ast.TypeAlias():
                type_nodes.append(node)
                del lines[node.lineno -1]
                assert not node.end_lineno or node.end_lineno == node.lineno
                rw = True

    if not rw:
        # nothing to rewrite
        return src

    last_import = None
    for node in ast.iter_child_nodes(root):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            last_import = node
        else:
            break

    if not last_import:
        insert_at = 0
    else:
        insert_at = last_import.end_lineno or last_import.lineno

    lines[insert_at:insert_at] = ["import typing", ""]
    insert_at += 2

    new_code = []
    for node in type_nodes:
        match node:
            case ast.TypeVar():
                # TypeVar(name='T', bound=Name(id='int', ctx=Load()))
                try:
                    bound_str = f", bound={node.bound.id}"# type: ignore
                except AttributeError:
                    bound_str = ""
                new_code.append(f"{node.name} = typing.TypeVar(\"{node.name}\"{bound_str})")

            case ast.ParamSpec():
                # ParamSpec(name='P')
                new_code.append(f"{node.name} = typing.ParamSpec(\"{node.name}\")")

            case ast.TypeAlias():
                # TypeAlias(
                #     name=Name(id='Alias', ctx=Store()),
                #     type_params=[],
                #     value=Name(id='int', ctx=Load())
                # )
                if node.type_params:
                    raise NotImplemented(node.type_params)

                new_code.append(f"{node.name.id}: typing.TypeAlias = {ast.unparse(node.value)}")

    new_code.append("")
    lines[insert_at:insert_at] = new_code

    if lines[-1]:
        lines.append("")

    return "\n".join(lines)
