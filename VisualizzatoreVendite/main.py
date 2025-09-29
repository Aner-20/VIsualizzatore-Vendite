import sys 
from PyQt5.QtWidgets import *
import pandas as pd
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.df = None 
        self.setWindowTitle("Visualizzatore Vendite")
        self.resize(800, 600)
        self.center_window()
        self.initUI()
      
        
    def initUI(self):
        central_widget = QWidget()
        central_widget.setStyleSheet(f"""
           QWidget{{
               background-color: #006400;
               color: #f8f9fa;
           }}
           
           QPushButton{{
               background-color: #000;
               font-size: 14px;
               border-radius: 10px;
               padding: 10px 5px;
               border: 2px solid #f8f9fa;
           }}   
           
           QComboBox{{
               background-color: #000;
               color: #f8f9fa;
               selection-background-color: #006400;
               border-radius: 10px
           }}  
           
           QLabel{{
               font-size: 16px;
               font-family: Arial;
           }}                     
                                     
        """)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        
        self.load_btn = QPushButton("Carica CSV")
        self.load_btn.setFixedWidth(300)
        self.load_btn.clicked.connect(self.load_csv)
        main_layout.addWidget(self.load_btn, alignment=Qt.AlignCenter)
        
        self.combo = QComboBox()
        self.combo.setFixedWidth(300)
        self.combo.currentIndexChanged.connect(self.update_plot)
        main_layout.addWidget(self.combo, alignment=Qt.AlignCenter)
        
        
        self.label = QLabel("Seleziona tipo di grafico: ")
        self.combo_chart = QComboBox()
        self.combo_chart.setFixedWidth(300)
        self.combo_chart.addItems(["Linea", "Barre", "Istogramma"])
        self.combo_chart.currentIndexChanged.connect(self.update_plot)
        main_layout.addWidget(self.label, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.combo_chart, alignment=Qt.AlignCenter)
        
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        main_layout.addWidget(self.canvas, alignment=Qt.AlignCenter)
        
        central_widget.setLayout(main_layout)
    
    def load_csv(self):
        path, _ = QFileDialog.getOpenFileName(self, "Apri CSV", "", "CSV Files (*csv)")
        if path:
            self.df = pd.read_csv(path)
            if "Categoria" in self.df.columns:
                categories = self.df["Categoria"].unique()
                self.combo.clear()
                self.combo.addItems(categories)
            
            self.update_plot()
            
    def update_plot(self):
        if self.df is not None:
            self.ax.clear()
            cat = self.combo.currentText()
            chart_type = self.combo_chart.currentText()
            
            data = self.df.copy()
            data['Totale'] = data['Prezzo'] * data['Quantità']
            
            if cat and cat != "Tutte":
                data = data[data['Categoria'] == cat]
            
            # Raggruppo per data
            daily_sales = data.groupby('Data')['Totale'].sum()
            
            # Disegno in base al tipo di grafico
            if chart_type == "Linea":
                daily_sales.plot(ax=self.ax, kind='line', marker='o', color='green')
            elif chart_type == "Barre":
                daily_sales.plot(ax=self.ax, kind='bar', color='skyblue', edgecolor='black')
            elif chart_type == "Istogramma":
                self.ax.hist(data['Totale'], bins=10, color='orange', edgecolor='black')
                self.ax.set_title(f"Istogramma vendite{' - ' + cat if cat != 'Tutte' else ''}")
                self.ax.set_xlabel("Totale singola vendita (€)")
                self.ax.set_ylabel("Frequenza")
            
            # Titolo e assi (solo per linee e barre)
            if chart_type != "Istogramma":
                self.ax.set_title(f"Vendite giornaliere{' - ' + cat if cat != 'Tutte' else ''}")
                self.ax.set_xlabel("Data")
                self.ax.set_ylabel("Totale (€)")
                self.ax.grid(True, alpha=0.3)
                self.figure.autofmt_xdate()
            
            self.canvas.draw()

        
    
    def center_window(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)
    
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_()) # exec() execute method
    
if __name__ == '__main__':
    main()

