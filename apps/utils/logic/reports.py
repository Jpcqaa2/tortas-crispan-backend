

def size_column_excel(excel, reporte, sheet_name):
    for i, column in enumerate(reporte.columns):
        # Calcular el ancho máximo entre los valores de la columna y el nombre de la columna
        max_length = max(reporte[column].astype(str).map(len).max(), len(column))
        excel.sheets[sheet_name].set_column(i, i, max_length + 2)  # +2 para un poco de espacio extra
    