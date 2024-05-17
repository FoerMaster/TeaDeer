from core.model import *
def sort(
        results,
        destination_folder_dear = 'TeaDeer/training/preparing/deer',
        destination_folder_musk_dear = 'TeaDeer/training/preparing/musk_dar',
        destination_folder_roe_dear = 'TeaDeer/training/preparing/roe_dear'
):
    os.makedirs(destination_folder_dear, exist_ok=True)
    os.makedirs(destination_folder_musk_dear, exist_ok=True)
    os.makedirs(destination_folder_roe_dear, exist_ok=True)

    for result in results:
        dear_class = result.classes
        if dear_class == 0:
            shutil.copy(result, destination_folder_dear)
        elif dear_class == 1:
            shutil.copy(result, destination_folder_dear)
        elif dear_class == 2:
            shutil.copy(result, destination_folder_roe_dear)
