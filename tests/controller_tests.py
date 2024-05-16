import sys
sys.path.append('C:/Users/ACER/Pensiones')
from src.controller.app_controller import ControladorPensiones
from src.model.user import Usuario
import unittest

class ControladorPensionesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.controlador = ControladorPensiones()
        cls.controlador.CrearTablas()

    def setUp(self):
        self.controlador.CrearTablas()

    def tearDown(self):
        self.controlador.CrearTablas()

    def test_crear_tablas(self):
        usuarios = self.controlador.ObtenerUsuarios()
        pensiones = self.controlador.ObtenerPensiones(1)  # Asumiendo que no hay usuarios aún
        self.assertEqual(len(usuarios), 0)
        self.assertEqual(len(pensiones), 0)

    def test_insertar_usuario(self):
        usuario = Usuario("Roxana Suarez", 30, "soltero")
        self.controlador.InsertarUsuario(usuario)
        usuarios = self.controlador.ObtenerUsuarios()
        self.assertEqual(len(usuarios), 1)
        self.assertEqual(usuarios[0].name, "Juan Perez")
        self.assertEqual(usuarios[0].age, 30)
        self.assertEqual(usuarios[0].civil_status, "soltero")

    def test_insertar_usuario_duplicado(self):
        usuario = Usuario("Juan Perez", 30, "soltero")
        self.controlador.InsertarUsuario(usuario)
        usuario_duplicado = Usuario("Juan Perez", 30, "soltero")
        self.controlador.InsertarUsuario(usuario_duplicado)
        usuarios = self.controlador.ObtenerUsuarios()
        self.assertEqual(len(usuarios), 1)

    def test_insertar_pension(self):
        usuario = Usuario("Maria luz", 30, "soltero")
        self.controlador.InsertarUsuario(usuario)
        usuario_id = self.controlador.ObtenerUsuarios()[0].id
        ahorro_pensional = 100000
        pension = 5000
        self.controlador.InsertarPension(usuario_id, ahorro_pensional, pension)
        pensiones = self.controlador.ObtenerPensiones(usuario_id)
        self.assertEqual(len(pensiones), 1)
        self.assertEqual(pensiones[0]["ahorro_pensional"], ahorro_pensional)
        self.assertEqual(pensiones[0]["pension"], pension)

if __name__ == '__main__':
    unittest.main(verbosity=2)
