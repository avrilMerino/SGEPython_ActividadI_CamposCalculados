from odoo import models, fields, api
from datetime import date

class EmailUser(models.Model):
    _name = "email.user"
    _description = "Usuario de correo electrónico"

    name = fields.Char(string="Nombre completo", required=True)
    email = fields.Char(string="Dirección de correo", required=True)
    password = fields.Char(string="Contraseña", required=True)
    quota = fields.Integer(string="Cuota (MB)", default=1024)
    active = fields.Boolean(string="Activo", default=True)

    # Fecha de nacimiento (sin default=True)
    fecNac = fields.Date(string="Fecha de nacimiento")

    # Campos calculados
    edad = fields.Integer(string="Edad", compute="_calcula_edad", store=True, readonly=True)
    mayorEdad = fields.Boolean(string="Mayor de edad", compute="_calcula_mayor_edad", store=True)
    correoCorporativo = fields.Char(string="Correo corporativo", compute="_calcular_correo", store=True)

    domain = fields.Char(string="Dominio", default="midominio.com")
    forwarding = fields.Char(string="Reenvío a")
    notes = fields.Text(string="Notas")

#funcion para cálculo de edad
    @api.depends("fecNac")
    def _calcula_edad(self):
        for registro in self:
            if registro.fecNac:
                hoy = date.today()
                nacimiento = registro.fecNac

                edad = hoy.year - nacimiento.year
                if (hoy.month, hoy.day) < (nacimiento.month, nacimiento.day):
                    edad -= 1

                registro.edad = edad
            else:
                registro.edad = 0

#funcion para ver su es mayor de edad
    @api.depends("edad")
    def _calcula_mayor_edad(self):
        for registro in self:
            registro.mayorEdad = (registro.edad >= 18)

#funcion para cálculo del correo corporativo
    @api.depends("name")
    def _calcular_correo(self):
        for registro in self:
            if not registro.name:
                registro.correoCorporativo = ""
                continue

            #Separo por espacios y quito huecos dobles
            partes = registro.name.strip().split()
            inicial = partes[0][0] if len(partes[0]) > 0 else ""

            apellido1 = partes[1] if len(partes) >= 2 else ""
            apellido2 = partes[2] if len(partes) >= 3 else ""

            #InicalNombre+Apellido1+Apellido2@empresa.es
            registro.correoCorporativo = f"{inicial}{apellido1}{apellido2}@empresa.es".lower()
