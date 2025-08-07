import os

EXCLUDE_DIRS = {'venv', '.env', '__pycache__', 'node_modules', '.git'}

def print_tree(start_path, indent=''):
    for item in os.listdir(start_path):
        if item.startswith('.'):
            continue
        path = os.path.join(start_path, item)
        if os.path.isdir(path):
            if item not in EXCLUDE_DIRS:
                print(indent + f'[DIR] {item}')
                print_tree(path, indent + '    ')
        else:
            print(indent + f'      {item}')

print_tree('.')
