def get_all_keys(d, key=[], output=[]):
    '''
    A recursive function that traverses json keys in a dict `d`,
    and prints the path to all keys
    '''
    if not isinstance(d, dict):
        return '.'.join([k for k in key]) 

    for k, v in d.items():
        key_path = key + [k]
        out = get_all_keys(d[k], key_path, output)
        if not isinstance(out, list):
            output.append(out)

    return list(set(output))