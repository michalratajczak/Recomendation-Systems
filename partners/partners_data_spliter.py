import pandas
import csd_dataset.dataset_header
import os
import helpers.console_logger
import config


def split_data(dataset, partners, column_names):
    logger = helpers.console_logger.console_logger("Splitting dataset")
    counter = 1
    if not os.path.exists(os.path.join(config.config['root_dir'], 'data')):
        os.makedirs(os.path.join(config.config['root_dir'], 'data'))
    for partner in partners:
        logger.run_execution_timer()
        dataset.loc[dataset['partner_id'] == partner].to_csv(os.path.join(config.config['root_dir'], 'data', partner), sep='\t', columns=column_names)
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
    csd = pandas.read_csv(os.path.join(config.config['root_dir'], 'csd_dataset', 'CriteoSearchData'), sep='\t', names=csd_dataset.dataset_header.columns, low_memory=False)
    logger.log_total_time()

    logger = helpers.console_logger.console_logger("Extracting list of unique partners")
    partners = csd['partner_id'].unique()
    logger.log_total_time()

    logger = helpers.console_logger.console_logger("Saving list of partners to file")
    save_partners_list(partners)
    logger.log_total_time()

    split_data(csd, partners, csd_dataset.dataset_header.columns)


