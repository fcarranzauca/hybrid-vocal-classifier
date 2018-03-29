"""
feature extraction
"""

# from hvc
from .parseconfig import parse_config
from . import features
from .parse.extract import _validate_feature_group_and_convert_to_list


def extract(config_file=None,
            data_dirs=None,
            file_format=None,
            annotation_file=None,
            labels_to_use=None,
            feature_group=None,
            feature_list=None,
            output_dir=None,
            spect_params=None,
            return_features=True):
    """high-level function for feature extraction.
    Accepts either a config file or a set of parameters and
    uses them to extract features from audio files that are then used to train machine learning classifiers.
    Returns features and/or saves them to a file.

    Parameters
    ----------
    config_file : string
        filename of YAML file that configures feature extraction
    data_dirs : list
        of str, directories that contain audio files from which features should be extracted.
        hvc.extract attempts to create an annotation.csv file based on the audio file types in
        the directories.
    annotation_file : str
        filename of an annotation.csv file
    labels_to_use : str
        either
            a string representing unique set of labels which, if
            a syllable/segment is annotated with that label, then features
            will be calculated for that syllable
            e.g., 'iabcdef' or '012345'
        or
            'all'
                in which case features are extracted from all syllable segments
    feature_group : str
        One of the following set: {'knn', 'svm', 'flatwindow'}
        Shorthand way of specifying a list of features to extract, see docs for more detail.
    feature_list : list
        list of features to extract
    output_dir : str
        absolute path to directory in which to save extracted features
    spect_params : dict
        parameters to compute spectrograms,
        i.e., as defined for hvc.audiofileIO.Spectrogram
    return_features : bool
        if True, returns features and labels
    """
    if config_file and (data_dirs or file_format or annotation_file or labels_to_use
                        or feature_group or feature_list or output_dir or spect_params):
        raise ValueError('Cannot specify config_file and other parameters '
                         'when calling hvc.extract, '
                         'please specify either config_file or all other '
                         'parameters ')

    if config_file and data_dirs:
        raise ValueError('Please specify either config_file or data_dirs, '
                         'not clear which to use when both are specified')

    if config_file and annotation_file:
        raise ValueError('Please specify either config_file or annotation_file, '
                         'not clear which to use when both are specified')

    if config_file:
        extract_config = parse_config(config_file, 'extract')
        print('Parsed extract config.')

        todo_list = extract_config['todo_list']
        for ind, todo in enumerate(todo_list):

            print('Completing item {} of {} in to-do list'.format(ind + 1, len(todo_list)))

            extract_init_params = {'feature_list': todo['feature_list']}
            if 'feature_list_group_ID' in todo:
                extract_init_params['feature_list_group_ID'] = todo['feature_list_group_ID']
                extract_init_params['feature_group_ID_dict'] = todo['feature_group_ID_dict']

            # segment_params defined for todo_list item takes precedence over any default
            # defined for `extract` config
            if 'segment_params' in todo:
                extract_init_params['segment_params'] = todo['segment_params']
            else:
                extract_init_params['segment_params'] = extract_config['segment_params']

            if 'spect_params' in todo:
                extract_init_params['spect_params'] = todo['spect_params']
            else:
                extract_init_params['spect_params'] = extract_config['spect_params']

            fe = features.extract.FeatureExtractor(**extract_init_params)

            extract_params = {
                'output_dir': todo['output_dir'],
                'labels_to_use': todo['labels_to_use'],
                'file_format': todo['file_format']
            }

            if 'data_dirs' in todo:
                extract_params['data_dirs'] = todo['data_dirs']
                extract_params['data_dirs_validated'] = True
            elif 'annotation_file' in todo:
                extract_params['annotation_file'] = todo['annotation_file']

            fe.extract(**extract_params)

    elif data_dirs or annotation_file:
        if data_dirs and annotation_file:
            raise ValueError('hvc.extract received values for both data_dirs and '
                             'annotation_file arguments, unclear which to use. '
                             'Please only specify one or the other.')

        if feature_group and feature_list:
            raise ValueError('hvc.extract received values for both feature_group and '
                             'feature_list arguments, unclear which to use. '
                             'Please only specify one or the other.')

        extract_init_params = {}
        if spect_params is None:
            spect_params = {'ref': 'default'}
        if feature_group:
            if type(feature_group) != str and type(feature_group) != list:
                raise TypeError('feature_group must be str or list but instead was {}'
                                .format(type(feature_group)))
            if type(feature_group) == str:
                feature_list = _validate_feature_group_and_convert_to_list(feature_group)
            elif type(feature_group) == list:
                (feature_list,
                 feature_list_group_ID,
                 feature_group_ID_dict) = _validate_feature_group_and_convert_to_list(feature_group)
                extract_init_params['feature_list_group_ID'] = feature_list_group_ID
                extract_init_params['feature_group_ID_dict'] = feature_group_ID_dict
            extract_init_params['feature_list'] == feature_list

        extract_init_params = {
            'spect_params': spect_params,
        }
        fe = features.extract.FeatureExtractor(**extract_init_params)

        extract_params = {}
        if data_dirs:
            extract_params['data_dirs'] = data_dirs
        elif annotation_file:
            extract_params['annotation_file'] = annotation_file
        fe.extract(**extract_params)