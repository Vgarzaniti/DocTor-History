from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gestión de Pacientes")  # Título de la ventana
        self.setGeometry(100, 100, 800, 600)  # Tamaño de la ventana (x, y, ancho, alto)

        # Crear un widget central
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Layout principal
        layout = QVBoxLayout()
        
        # Etiqueta de ejemplo
        label = QLabel("Bienvenido a la aplicación de gestión de pacientes")
        layout.addWidget(label)

        # Asignar el layout al widget central
        central_widget.setLayout(layout)
