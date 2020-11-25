import pandas
import csd_dataset.dataset_header
import os
import helpers.console_logger
import app_config


def split_data(dataset, partners, column_names):
    logger = helpers.console_logger.console_logger("Splitting dataset")
    counter = 1
    if not os.path.exists(app_config.app_config['split_partners_data_dir']):
        os.makedirs(app_config.app_config['split_partners_data_dir'])
    for partner in partners:
        logger.run_execution_timer()
        dataset.loc[dataset['partner_id'] == partner].to_csv(os.path.join(app_config.app_config['split_partners_data_dir'], partner),
                                                             sep='\t', columns=column_names, index=False)
        logger.log_with_execution_time(f'{counter} / {len(partners)}')
        counter+=1
    logger.log_total_time()


def save_partners_list(partners):
    with open('partners_list.py', "w") as f:
        f.write('partners = \\\n[\n')
        for partner in partners[:-1]:
            f.write(f'  \'{partner}\',\n')
        f.write(f'  \'{partner}\'\n')
        f.write("]")


if __name__ == "__main__":
    logger = helpers.console_logger.console_logger("Reading data")
    logger.log("Starting operation...")
    csd = pandas.read_csv(app_config.app_config['criteo_search_data_path'], sep='\t',
                          names=csd_dataset.dataset_header.columns, low_memory=False)
    logger.log_total_time()

    logger = helpers.console_logger.console_logger("Extracting list of unique partners")
    partners = csd['partner_id'].unique()
    logger.log_total_time()

    logger = helpers.console_logger.console_logger("Saving list of partners to file")
    save_partners_list(partners)
    logger.log_total_time()

    split_data(csd, partners, csd_dataset.dataset_header.columns)


