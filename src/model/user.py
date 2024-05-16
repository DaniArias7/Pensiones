class Usuario:
    def __init__(self, name, age, civil_status):
        self.name = name
        self.age = age
        self.civil_status = civil_status

    def es_igual(self, comparar_con):
        assert(self.name == comparar_con.name)
        assert(self.age == comparar_con.age)
        assert(self.civil_status == comparar_con.civil_status)