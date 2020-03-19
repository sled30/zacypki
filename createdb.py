import sqlite3



def conn():
    connect = sqlite3.connect('data/storageDB') # 'data/mydb'
    return connect
def create_db():
    """ create structure db """


    create_source = "CREATE TABLE IF NOT EXISTS `agregator` ( \
	           `id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL , \
                  `number_advert` varchar(20) NOT NULL, \
            	  `advert_text` varchar(20) NOT NULL,  \
                  `status` varchar(20) NOT NULL,\
                  `short_text_advert` varchar(50) NOT NULL, \
                  `name_organisation` varchar(50) NOT NULL, \
                  `long_text_advert` varchar(50) NOT NULL,  \
                  `advert_type` varchar(20) NOT NULL, \
                  `createtion_date` varchar(50) NOT NULL, \
                  `end_advert_date` varchar(50) NOT NULL, \
                  `region` varchar(50) NOT NULL, \
                  `date_of_conclusion` varchar(50) NOT NULL, \
                  `url` varchar(50) NOT NULL) "


    create_source_index = "CREATE INDEX `number_advert` ON `agregator` (`number_advert`)"
#    create_ids_index = "CREATE INDEX `phone` ON `ids` (`phone`, `date`)"
    connect = conn()
    with connect:
        connect.execute(create_source)
    #    connect.execute(create_ids)
        connect.execute(create_source_index)
    #    connect.execute(create_ids_index)
        connect.close
        return True

create_db()
