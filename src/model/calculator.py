class CalculadoraPensional:


    """Almacenamos los mensajes y validaciones de ahorro pensional en una sola clase"""
    def validaciones_tipo_ahorro_pensional(self, edad, salario, semanas_laboradas, rentabilidad_fondo, tasa_administracion):
        mensaje_error = ""

        if not isinstance(salario, (int, float)):
            raise TypeError("El salario debe ser numérico. ")

        if not isinstance(edad, int):
            raise TypeError("La edad debe ser un entero. ")

        if not isinstance(semanas_laboradas, (int, float)):
            raise TypeError("Las semanas laboradas deben ser numéricas. ")

        if not isinstance(tasa_administracion, (int, float)):
            mensaje_error += "La tasa de administración debe ser numérica. "

        if rentabilidad_fondo < 0 or rentabilidad_fondo > 1:
            mensaje_error += "La rentabilidad de fondo debe estar entre 0 y 1. "

        if semanas_laboradas < 0:
            mensaje_error += "Las semanas laboradas tienen que ser positivas. "

        if edad <= 0:
            mensaje_error += "La edad ingresada es negativa, ingrese una edad válida. "

        if salario <= 0:
            mensaje_error += "El salario debe ser mayor a 0. "

        return mensaje_error
    
    
    """Almacenamos los mensajes y validaciones de calculo pensional en una sola clase"""
    def validaciones_tipo_calculo_pension(self, edad, ahorro_pensional_esperado, sexo, estado_civil, esperanza_vida):
        mensaje_error = ""

        if not isinstance(sexo, str):
            mensaje_error += "El sexo debe ser un string, no un número. Debe ser 'masculino' o 'femenino'. "

        if not isinstance(estado_civil, str):
            mensaje_error += "El estado civil debe ser 'soltero' o 'casado', tu ingresaste un número. "

        if not isinstance(edad, int):
            raise TypeError("La edad debe ser un entero, ingresa una edad válida. ")

        if sexo not in ['masculino', 'femenino']:
            raise TypeError ("El sexo debe ser 'masculino' o 'femenino'. ")

        if estado_civil not in ['casado', 'soltero']:
            raise TypeError ("El estado civil debe ser 'casado' o 'soltero'. ")

        if not isinstance(esperanza_vida, (int, float)):
            raise TypeError ("La esperanza de vida debe ser numérica. ")

        if not isinstance(ahorro_pensional_esperado, (int, float)):
            raise TypeError("El ahorro pensional esperado debe ser int o float. ")

        if edad < 0:
            mensaje_error += "La edad no puede ser negativa, ingrese una edad válida. "

        if edad > 90:
            mensaje_error += "La edad debe estar entre 1-90, ingrese una edad válida. "

        if edad > esperanza_vida:
            mensaje_error += "La edad no puede ser mayor a la esperanza de vida. "

        if esperanza_vida < 0:
            mensaje_error += "La esperanza de vida debe ser mayor a 0. "

        return mensaje_error
    

    """Método que se encargad del cálculo del ahorro pensional y recoge el mensaje de error en las validaciones de tipo"""
    def calculo_ahorro_pensional(self, edad, salario, semanas_laboradas, rentabilidad_fondo, tasa_administracion):
        mensaje_error = self.validaciones_tipo_ahorro_pensional(edad, salario, semanas_laboradas, rentabilidad_fondo, tasa_administracion)
        aportes_mensuales = salario * 0.12
        ahorro_pensional_esperado = aportes_mensuales * semanas_laboradas * rentabilidad_fondo * (1 - tasa_administracion)

        """Si se devuelve un mensaje de error, se muestra con el cálculo, sino solo se devuelve el cálculo"""
        if mensaje_error:
            return ahorro_pensional_esperado, mensaje_error
        return ahorro_pensional_esperado, None

    """Método con el calculo de la pension, que recoge un mensaje de error de las validaciones, si hay mensajed de error se devuelve con el cálculo, sino solo el calculo"""
    def calculo_pension(self, edad, ahorro_pensional_esperado, sexo, estado_civil, esperanza_vida):
        mensaje_error = self.validaciones_tipo_calculo_pension(edad, ahorro_pensional_esperado, sexo, estado_civil, esperanza_vida)
        factor_sexo = 0
    
        if sexo == 'masculino':
            if estado_civil == 'soltero':
                factor_sexo = 0.06
            elif estado_civil == 'casado':
                factor_sexo = 0.08
        elif sexo == 'femenino':
            if estado_civil == 'soltero':
                factor_sexo = 0.07
            elif estado_civil == 'casado':
                factor_sexo = 0.09

        pension_esperada = ahorro_pensional_esperado * (1 + factor_sexo) * (edad / (esperanza_vida - edad)) 

        if mensaje_error:
            return pension_esperada, mensaje_error
        return pension_esperada, ""
