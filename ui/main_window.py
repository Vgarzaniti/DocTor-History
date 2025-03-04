from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QTextEdit, QSizePolicy, QTableWidgetItem, QTableWidget
from PyQt6.QtCore import Qt
import os
from db.connection import get_db 
from db.queries import get_all_pacientes

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("App con Header Azul")
        self.setGeometry(100, 100, 600, 400)

        # Crear el header (Encabezado)
        header = QLabel("Bienvenido a mi App", self)
        header.setObjectName("header")  # Asignar ID para CSS
        header.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)  # Evitar expansión vertical

        # Alinear el header al inicio del layout
        header.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        # Crear un widget de contenido (ejemplo: un área de texto)
        self.table = QTableWidget(self)
        self.load_data()  # Cargar los datos de la base de datos

        # Layout principal
        layout = QVBoxLayout()
        layout.addWidget(header)  # Header arriba
        layout.addWidget(self.table, 1)  # Tabla ocupa el espacio restante

        # Widget contenedor
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
    # Ruta del archivo CSS dentro de "assets"
        css_path = os.path.join(os.path.dirname(__file__),"..", "assets", "windowMain.css")

        # Cargar CSS si el archivo existe
        if os.path.exists(css_path):
            with open(css_path, "r") as file:
                self.setStyleSheet(file.read())
    def load_data(self):
        # Usar la función `get_db` para obtener la sesión de SQLAlchemy
        db = next(get_db())  # Asumiendo que `get_db` es una función que devuelve un generador para la sesión de la base de datos

        try:
            # Llamar a la función de consulta en queries.py
            pacientes = get_all_pacientes(db)

            # Configurar el número de filas y columnas de la tabla
            self.table.setRowCount(len(pacientes))  # Número de filas en la tabla
            self.table.setColumnCount(5)  # Cinco columnas (Nombre, Apellido, Edad, Obra Social, Número de Obra Social)
            self.table.setHorizontalHeaderLabels(["Nombre", "Apellido", "Edad", "Obra Social", "Número de Obra Social"])

            # Llenar la tabla con los datos de la base de datos
            for row_idx, paciente in enumerate(pacientes):
                # Llenar los datos de cada paciente en la tabla
                self.table.setItem(row_idx, 0, QTableWidgetItem(paciente.nombre))  # Nombre
                self.table.setItem(row_idx, 1, QTableWidgetItem(paciente.apellido))  # Apellido
                self.table.setItem(row_idx, 2, QTableWidgetItem(str(paciente.edad)))  # Edad
                
                # Obtener la Obra Social y el número de obra social del paciente
                if paciente.pacientexobrasocial:
                    obra_social = paciente.pacientexobrasocial[0].obrasocial  # Asumimos que un paciente tiene al menos una obra social
                    numero_obrasocial = paciente.pacientexobrasocial[0].numeroobrasocial
                    self.table.setItem(row_idx, 3, QTableWidgetItem(obra_social.nombre))  # Nombre de la Obra Social
                    self.table.setItem(row_idx, 4, QTableWidgetItem(str(numero_obrasocial)))  # Número de Obra Social
                else:
                    self.table.setItem(row_idx, 3, QTableWidgetItem("No tiene"))  # Si no tiene obra social
                    self.table.setItem(row_idx, 4, QTableWidgetItem("N/A"))  # Número de Obra Social
        except Exception as e:
            print(f"Error al cargar los datos: {e}")

        finally:
            db.close()  # Cerrar la sesión de la base de datos 
        
        
        

