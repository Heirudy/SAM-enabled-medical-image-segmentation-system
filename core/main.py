from monai.data import DataLoader

from CTAI_flask.core import process, predict, get_feature
from CTAI_flask.core.process import process_images



def c_main(path,model_path):



    image_path,maks_path=predict.predict(path,model_path)

    # process.last_process(filename)
    image_info = get_feature.main(image_path,maks_path)

    return image_info

def c_main_3D(path,model_path):



    image_path,maks_path=predict.predict(path,model_path)

    # process.last_process(filename)
    image_info = get_feature.main(image_path,maks_path)

    return image_info
if __name__ == '__main__':
    pass
