import os

EXCLUDED_DIRS = {'__pycache__', '.git', '.venv', '.pytest_cache', 'node_modules', 'dist', 'build'}

def list_structure(start_path='.', output_file='project_structure.txt'):
    with open(output_file, 'w') as f:
        def walk_dir(current_path, prefix=''):
            entries = [e for e in os.listdir(current_path) if e not in EXCLUDED_DIRS]
            entries.sort()
            for index, entry in enumerate(entries):
                full_path = os.path.join(current_path, entry)
                connector = '└── ' if index == len(entries) - 1 else '├── '
                f.write(f'{prefix}{connector}{entry}\n')
                if os.path.isdir(full_path):
                    extension = '    ' if index == len(entries) - 1 else '│   '
                    walk_dir(full_path, prefix + extension)

        f.write(f'{start_path}/\n')
        walk_dir(start_path)

if __name__ == "__main__":
    list_structure()
