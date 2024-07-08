class db_config:
    def __init__(self):
        self.data = {
            'user': 'root',
            'password': 'root',
            'host': 'localhost',
            'database': 'Food_orders',
        }

    def get_config(self):
          return self.data
