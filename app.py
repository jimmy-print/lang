import flask
import copy
import lang, atoms
import traceback
from atoms import OnestepFinishedExecution, FinishedExecution
from atoms import OnestepFinishedExecutionNoPrint

app = flask.Flask(__name__)

@app.route('/')
def main():
    return flask.render_template('index.html')
on_line = None
@app.route('/receive', methods=['POST'])
def proc():
    gen = tuple(flask.request.form.values())

    raw_code = tuple(gen)[0]
    on_line = tuple(gen)[1]

    assert int(on_line) >= 0
    on_line = int(on_line)


    if on_line == 0:
        return generate_visual_representation(raw_code)
    elif on_line >= 0:
        return all_code_vis

stack = [0]
@app.route('/next', methods=['POST'])
def next():
    global tree, orig_tree, stack

    gen = flask.request.form.values()
    tuplegen = tuple(gen)

    on_line = tuplegen[0]
    on_line = int(on_line)
    
    tree = all_code_ast[on_line]['tree']
    orig_tree = all_code_ast[on_line]['orig_tree']
    
    try:
        atoms.run_onestep(tree, orig_tree, stack)
    except OnestepFinishedExecutionNoPrint as e:
        return {'status': e.status,
                'stack': stack[1:len(stack)],
                'print_msg': -1,
                'global_variables': atoms.global_variables}
        # because in below func, coords is based on the expansion
        # of a tree that has had its root node removed, unlike global_tree
    except OnestepFinishedExecution as e:
        return {'status': e.status,
                'stack': stack[1:len(stack)],
                'print_msg': str(e),
                'global_variables': atoms.global_variables}
    except FinishedExecution as e:
        stack = [0]
        return {'status': e.status,
                'stack': None,
                'print_msg': None,
                'global_variables': atoms.global_variables}
    else:
        print('Oh no')



def get_coords_and_lines_from_transformed_unrooted_tree(unrooted_tree):
    pkg = atoms.iterate_through_node_not_root(unrooted_tree) 
    depth = max(i[0] for i in pkg)

    x = 200
    y = 30
    min_vert_step = 65

    horz_step = None
    vert_step = None
    depth = 0
    coords = []
    lines = []
    xs = [None]
    max_horzs = [200]
    eager = list(atoms.iterate_through_node_not_root(unrooted_tree))
    for i, DFF in enumerate(atoms.iterate_through_node_not_root(unrooted_tree)):
        if DFF[1] == atoms.INDEX_TOO_BIG:
            assert i == len(eager) - 1
            break


        if i != 0:
            last_depth = eager[i - 1][0]
        else:
            last_depth = DFF[0]
        depth = DFF[0]

        if depth > last_depth:
            max_horzs.append(max_horzs[-1] - 40)

            max_horz = max_horzs[-1]
            length = len(DFF[1].parent.nodes)
            try:
                horz_step = ((length - 1) / 2) * (max_horz / (length - 1))
            except ZeroDivisionError:
                horz_step = 0

            x -= horz_step

            xs.append(x)


            y += min_vert_step * (depth - last_depth)
        elif depth < last_depth:

            #horz_step = max_horz_step / len(DFF[1].parent.nodes)
            length = len(DFF[1].parent.nodes)
            [max_horzs.pop() for i in range(last_depth - depth)]
            max_horz = max_horzs[-1]
            try:
                horz_step = ((length - 1) / 2) * (max_horz / (length - 1))
            except ZeroDivisionError:
                horz_step = 0


            y -= min_vert_step * (last_depth - depth)

            [xs.pop() for i in range(last_depth - depth)]

            x = xs[-1] + horz_step
            xs[-1] = x
        else:
            length = len(DFF[1].parent.nodes)
            max_horz = max_horzs[-1]
            try:
                horz_step = max_horz / (length - 1)
            except ZeroDivisionError:
                horz_step = 0
            x += horz_step
            xs[-1] = x

        coords.append((x, y, DFF[1].v, tuple(DFF[3])      ))

    for i, (coord, DFF) in enumerate(zip(coords, atoms.iterate_through_node_not_root(unrooted_tree))):
        parent_node = DFF[1].parent
        try:
            ii = [i[1] for i in atoms.iterate_through_node_not_root(unrooted_tree)].index(parent_node)
            lines.append(
            (
                coord, coords[ii]
            ))
        except ValueError:
            pass


    return coords, lines

all_code_ast = []
all_code_vis = []

def generate_visual_representation(raw_code):

    # TODO: *breadth* first search should allow for detection of neighbouring node
    # (on the same level) collisions, which would allow for 'perfect' non-intersecting
    # graph visualisations.
    raw_code_wo_front_back_whitespace = raw_code.strip()
    raw_exprs = raw_code_wo_front_back_whitespace.split(';')
    if raw_exprs[-1] == '':
        raw_exprs.pop()

    exprs = []
    for raw_expr in raw_exprs:
        no_newlines = lang.rm_char_instances(raw_expr, '\n')
        also_no_redundant_spaces = lang.compress_whitespace(no_newlines)
        exprs.append(also_no_redundant_spaces)


    for line in exprs:
        tokens = lang.expand_sigil(lang.get_tokens(line))
        tokens_no_whitespace = filter(lambda token: not lang.is_whitespace(token), tokens)


        rooted_tree = lang.get_tree(tokens_no_whitespace)
        transformed_tree = atoms.transform_ast(rooted_tree)
        unrooted_tree = transformed_tree.nodes[0]
        
        tree_ = copy.deepcopy(transformed_tree)
        orig_tree_ = copy.deepcopy(tree_)

        coords, lines = get_coords_and_lines_from_transformed_unrooted_tree(unrooted_tree)

        all_code_ast.append(
            {
                'tree': tree_,
                'orig_tree': orig_tree_,
             })
        all_code_vis.append(
            {
             'coords': coords,
             'lines': lines,
             })

    return all_code_vis
    


if __name__ == '__main__':
    try:
        app.run()
    except Exception:
        traceback.print_exc()
