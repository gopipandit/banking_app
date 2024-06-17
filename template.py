import os
from pathlib import Path
import logging


list_of_files = [
    'main.py',
    'models/__init__.py',
    'models/person.py',
    'models/account.py',
    'models/exceptions.py',
    'database/ __init__.py',
    'database/ db.py'
    ]

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)


    if filedir:
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating {filedir} for {filename}")

    if not filepath.exists() or filepath.stat().st_size == 0:
        with open(filepath,"w") as f:
            pass
        logging.info(f"Creating empty file {filename}")
    else:
        logging.info(f"This file {filename} already exists.")