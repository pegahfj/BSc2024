import scipy.io as sio

def load_patients_EEG_data():
    alpha_responder_day0 = sio.loadmat('/Users/pegz/Desktop/BachelorProject/BSc2024/subGraphDevelopement/sourceData/new_format/alpha_window_Kij_resp176_1.mat')
    alpha_responder_day7 = sio.loadmat('/Users/pegz/Desktop/BachelorProject/BSc2024/subGraphDevelopement/sourceData/new_format/alpha_window_Kij_resp176_2.mat')
    alpha_non_responder_day0 = sio.loadmat('/Users/pegz/Desktop/BachelorProject/BSc2024/subGraphDevelopement/sourceData/new_format/alpha_window_Kij_non_resp176_1.mat')
    alpha_non_responder_day7 = sio.loadmat('/Users/pegz/Desktop/BachelorProject/BSc2024/subGraphDevelopement/sourceData/new_format/alpha_window_Kij_non_resp176_2.mat')


    # Create a dictionary to store the matrices
    sample_groups_dict = {
        'alpha_responder_day0': alpha_responder_day0['alpha_window_Kij_resp176_1'],
        'alpha_responder_day7': alpha_responder_day7['alpha_window_Kij_resp176_2'],
        'alpha_non_responder_day0': alpha_non_responder_day0['alpha_window_Kij_non_resp176_1'],
        'alpha_non_responder_day7': alpha_non_responder_day7['alpha_window_Kij_non_resp176_2']
    }

    return sample_groups_dict