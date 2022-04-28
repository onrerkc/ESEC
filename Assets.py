from os import path

root = path.dirname(__file__)

application_name = "ESEC Göğüs Kanseri Tespiti"
application_version = "0.01.20.04"
application_author = "Onur Erikçi"
application_author_contact = "onurerikci@yaani.com"

application_icon64 = path.join(root, 'assets\\visuals\\x64\\application_icon.ico')
application_icon16 = path.join(root, 'assets\\visuals\\x16\\application_icon.ico')
image_icon16 = path.join(root, 'assets\\visuals\\x16\\image_icon.ico')
add_image_icon16 = path.join(root, 'assets\\visuals\\x16\\add_image_icon.ico')
add_image_icon48 = path.join(root, 'assets\\visuals\\x48\\add_image_icon.ico')
edit_image_icon16 = path.join(root, 'assets\\visuals\\x16\\edit_image_icon.ico')
remove_image_icon16 = path.join(root, 'assets\\visuals\\x16\\remove_image_icon.ico')
detection_icon16 = path.join(root, 'assets\\visuals\\x16\\detection_icon.ico')
change_network_icon16 = path.join(root, 'assets\\visuals\\x16\\change_network_icon.ico')
prediction_icon16 = path.join(root, 'assets\\visuals\\x16\\predict_icon.ico')
prediction_results_icon16 = path.join(root, 'assets\\visuals\\x16\\prediction_results_icon.ico')
clear_results_icon16 = path.join(root, 'assets\\visuals\\x16\\clear_results_icon.ico')
save_results_icon16 = path.join(root, 'assets\\visuals\\x16\\save_results_icon.ico')

default_tumour_detection_network = path.join(root, 'assets\\pretrained_neural_networks\\tumour_detection_network\\esec_tumour_detection_network.h5')
default_habit_detection_network = path.join(root, 'assets\\pretrained_neural_networks\\habit_detection_network\\esec_habit_detection_network.h5')
