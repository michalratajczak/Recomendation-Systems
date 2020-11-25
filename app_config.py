import os

app_config = \
    {
        'root_dir': os.path.dirname(os.path.abspath(__file__)),
        'criteo_search_data_path': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'csd_dataset', 'CriteoSearchData'),
        'split_partners_data_dir': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'partners', 'data'),
        'results_dir': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
    }
