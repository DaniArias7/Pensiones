class ValorInvalidoError(Exception):
    """Excepción personalizada para valores inválidos."""
    pass


class TipoIncorrectoError(Exception):
    """Excepción personalizada para tipos de datos incorrectos."""
    pass


class CalculadoraPensional:
    """Clase para calcular el ahorro pensional y la pensión esperada."""

    @staticmethod
    def validar_tipo(valor, tipo_esperado):
        """Valida el tipo de dato de un valor."""
        if not isinstance(valor, tipo_esperado):
            raise TipoIncorrectoError(f"El valor {valor} debe ser de tipo {tipo_esperado.__name__}.")

    @staticmethod
    def validar_rango(valor, rango_valido, mensaje_error):
        """Valida si un valor se encuentra dentro de un rango válido."""
        if valor not in rango_valido:
            raise ValorInvalidoError(mensaje_error)

    def validar_ahorro_pensional(self, edad, salario, semanas_laboradas, rentabilidad_fondo, tasa_administracion):
        """Valida los parámetros para el cálculo del ahorro pensional."""
        self.validar_tipo(edad, int)
        self.validar_tipo(salario, (int, float))
        self.validar_tipo(semanas_laboradas, (int, float))
        self.validar_tipo(rentabilidad_fondo, (int, float))
        self.validar_tipo(tasa_administracion, (int, float))

        self.validar_rango(rentabilidad_fondo, (0, 1), "La rentabilidad de fondo debe estar entre 0 y 1.")
        self.validar_rango(semanas_laboradas, (0, float('inf')), "Las semanas laboradas deben ser positivas.")
        self.validar_rango(edad, (1, float('inf')), "La edad ingresada debe ser mayor que 0.")
        self.validar_rango(salario, (0, float('inf')), "El salario debe ser mayor que 0.")

    def validar_calculo_pension(self, edad, ahorro_pensional_esperado, sexo, estado_civil, esperanza_vida):
        """Valida los parámetros para el cálculo de la pensión esperada."""
        self.validar_tipo(edad, int)
        self.validar_tipo(ahorro_pensional_esperado, (int, float))
        self.validar_tipo(sexo, str)
        self.validar_tipo(estado_civil, str)
        self.validar_tipo(esperanza_vida, (int, float))

        self.validar_rango(sexo, ('masculino', 'femenino'), "El sexo debe ser 'masculino' o 'femenino'.")
        self.validar_rango(estado_civil, ('casado', 'soltero'), "El estado civil debe ser 'casado' o 'soltero'.")
        self.validar_rango(edad, (1, 90), "La edad debe estar entre 1 y 90.")
        self.validar_rango(esperanza_vida, (edad, float('inf')), "La edad no puede ser mayor que la esperanza de vida.")

    def calculo_ahorro_pensional(self, edad, salario, semanas_laboradas, rentabilidad_fondo, tasa_administracion):
        """Calcula el ahorro pensional esperado."""
        try:
            self.validar_ahorro_pensional(edad, salario, semanas_laboradas, rentabilidad_fondo, tasa_administracion)
        except (ValorInvalidoError, TipoIncorrectoError) as e:
            return None, str(e)

        aportes_mensuales = salario * 0.12
        ahorro_pensional_esperado = aportes_mensuales * semanas_laboradas * rentabilidad_fondo * (1 - tasa_administracion)
        return ahorro_pensional_esperado, None

    def calculo_pension(self, edad, ahorro_pensional_esperado, sexo, estado_civil, esperanza_vida):
        """Calcula la pensión esperada."""
        try:
            self.validar_calculo_pension(edad, ahorro_pensional_esperado, sexo, estado_civil, esperanza_vida)
        except (ValorInvalidoError, TipoIncorrectoError) as e:
            return None, str(e)

        factor_sexo = {
            'masculino': {'soltero': 0.06, 'casado': 0.08},
            'femenino': {'soltero': 0.07, 'casado': 0.09}
        }[sexo][estado_civil]

        pension_esperada = ahorro_pensional_esperado * (1 + factor_sexo) * (edad / (esperanza_vida - edad))
        return pension_esperada, None