# *_*coding:utf-8 *_*
import datetime
import os
from Log import Logger

import pymysql

log = Logger(filename='save_data_sql.log', level='debug')


def main(table_name, prod_code):
    """
    :param table_name: 数据库表名
    :param prod_code: 期货类型文件夹名称
    :return:
    """
    db = pymysql.connect('localhost', 'root', 'mima123456', 'test')
    cursor = db.cursor()
    # 建表语句
    create_table_sql = '''
                        create table if not exists {} (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                type VARCHAR(20),
                                price FLOAT(10, 1), 
                                quantity INT, 
                                date_time datetime NOT NULL UNIQUE 
                                ) ENGINE=INNODB CHARSET=utf8;
                        '''.format(table_name)
    cursor.execute(create_table_sql)

    # 插入数据
    cur_path = os.getcwd() + os.path.sep + 'data'
    cur_path + os.path.sep + prod_code
    # 前一天写进数据文件
    # file_name = str(datetime.date.today() - datetime.timedelta(days=1)) + '_' + prod_code + '.csv'
    file_name_list = ['2019-02-25_YMH9.csv', '2019-02-26_YMH9.csv', '2019-02-27_YMH9.csv', '2019-02-28_YMH9.csv']
    for file_name in file_name_list:
        datetime.timedelta()
        try:
            with open(cur_path + os.path.sep + prod_code + os.path.sep + file_name, 'r') as f:
                msg = f.read()
            save_data = write_sql_data(msg)

            for data in save_data:
                save_data_sql = "INSERT INTO {}(type, price, quantity, date_time) VALUES {}".format(table_name, data)
                try:
                    cursor.execute(save_data_sql)
                    db.commit()
                    log.logger.info('save a data, data:{}'.format(data))
                except Exception as e:
                    log.logger.error(e)
            cursor.close()
            db.close()
        except Exception as e:
            cursor.close()
            db.close()
            log.logger.error(str(e))


def write_sql_data(msg):
    """
    :param msg: 文件中的数据
    :return: 元组数据
    """
    data_list = msg.split('\n')[1::]
    data_list = data_list[:-1]
    # save_data = list()
    for data in data_list:
        save_data_list = data.split(',')
        save_data_tuple = tuple(save_data_list)
        # data.append(save_data_tuple)
        yield tuple(save_data_tuple)


if __name__ == '__main__':
    main('YM_data', 'YMH9')
