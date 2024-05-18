from core.model import *

import shutil
import os
def sort(
        results,
        destination_folder_dear = 'TeaDeer/training/preparing/deer',
        destination_folder_musk_dear = 'TeaDeer/training/preparing/musk_dar',
        destination_folder_roe_dear = 'TeaDeer/training/preparing/roe_dear',
        destination_folder_unknown='dist/незвестно',
        remove_originals=False,
):
    os.makedirs(destination_folder_dear, exist_ok=True)
    os.makedirs(destination_folder_musk_dear, exist_ok=True)
    os.makedirs(destination_folder_roe_dear, exist_ok=True)
    os.makedirs(destination_folder_unknown, exist_ok=True)
    for result in results:

        if len(result.boxes.cls) > 0:
            dear_class = int(result.boxes.cls[0])
            if dear_class == 0:

                shutil.move(result.path, destination_folder_dear)
            elif dear_class == 1:
                shutil.move(result.path, destination_folder_musk_dear)
            elif dear_class == 2:
                shutil.move(result.path, destination_folder_roe_dear)
        else:
            shutil.move(result.path, destination_folder_unknown)