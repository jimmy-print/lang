def get_tokens(s):
    split = s.strip().split()
    def remove_all_instances_of_right_paren(string):
        out = []
        for c in string:
            if c != ')':
                out.append(c)
        return ''.join(out)

    out = []
    for tok in split:
        if ')' not in tok:
            out.append(tok)
        else:
            out.append(remove_all_instances_of_right_paren(tok))
            len_of_right_paren = 0
            for c in tok:
                if c == ')':
                    len_of_right_paren += 1
            for _ in range(len_of_right_paren):
                out.append(')')
    return out
