import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow  # Importa la ventana principal

def main():
    app = QApplication(sys.argv)  # Crea la aplicación Qt
    window = MainWindow()  # Instancia la ventana principal
    window.show()  # Muestra la ventana
    sys.exit(app.exec())  # Inicia el bucle de eventos de Qt

if __name__ == "__main__":
    main()
