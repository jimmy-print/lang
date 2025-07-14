import flask
import lang, atoms

app = flask.Flask(__name__)

@app.route('/')
def main():
    return flask.render_template('a.html')

@app.route('/receive', methods=['POST'])
def proc():
    gen = flask.request.form.values()
    raw_code = tuple(gen)[0]
    return generate_visual_representation(raw_code)

def generate_visual_representation(raw_code):
    raw_code_wo_front_back_whitespace = raw_code.strip()
    raw_exprs = raw_code_wo_front_back_whitespace.split(';')
    if raw_exprs[-1] == '':
        raw_exprs.pop()

    exprs = []
    for raw_expr in raw_exprs:
        no_newlines = lang.rm_char_instances(raw_expr, '\n')
        also_no_redundant_spaces = lang.compress_whitespace(no_newlines)
        exprs.append(also_no_redundant_spaces)

    # just handle the first expr for now.
    line = exprs[0]
    tokens = lang.expand_sigil(lang.get_tokens(line))
    tokens_no_whitespace = filter(lambda token: not lang.is_whitespace(token), tokens)
    tree = lang.get_tree(tokens_no_whitespace)
    unrooted_tree = atoms.run(tree, getting=True)
    unrooted_tree = unrooted_tree.nodes[0]
    print(atoms.new_get_vis_stack_str(unrooted_tree))
    pkg = atoms.iterate_through_node_not_root(unrooted_tree) 
    depth = max(i[0] for i in pkg)

    x = 200
    y = 0
    min_vert_step = 75

    horz_step = None
    vert_step = None
    depth = 0
    coords = []
    lines = []
    xs = [None]
    max_horzs = [200]
    eager = list(atoms.iterate_through_node_not_root(unrooted_tree))
    for i, DFF in enumerate(atoms.iterate_through_node_not_root(unrooted_tree)):
        if i != 0:
            last_depth = eager[i - 1][0]
        else:
            last_depth = DFF[0]
        depth = DFF[0]
        print(DFF)

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
            print(x)


            y += min_vert_step * (depth - last_depth)
        elif depth < last_depth:
            print('\t', DFF)
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
            print(xs[-1])
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

        coords.append((x, y, DFF[1].v))

    for i, (coord, DFF) in enumerate(zip(coords, atoms.iterate_through_node_not_root(unrooted_tree))):
        parent_node = DFF[1].parent
        try:
            ii = [i[1] for i in atoms.iterate_through_node_not_root(unrooted_tree)].index(parent_node)
            print(ii)
            lines.append(
            (
                coord, coords[ii]
            ))
        except ValueError:
            pass


    return {'coords':coords, 'lines':lines}
