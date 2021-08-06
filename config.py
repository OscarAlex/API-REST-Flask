class DevelopmentConfig():
    DEBUG= True
    #Base de datos
    MYSQL_HOST= 'localhost'
    MYSQL_USER= 'root'
    MYSQL_PASSWORD= 'password'
    MYSQL_DB= 'work'

config= {
    'development': DevelopmentConfig
}