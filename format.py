from openpyxl import load_workbook
from openpyxl.utils.exceptions import InvalidFileException, CellCoordinatesException


def adapt_columns(excel_file, sheet_name):
    try:
        wb = load_workbook(excel_file)
        ws = wb[sheet_name]
        columns = "ABCDEFGHIJKL"
        for column in columns:
            ws.column_dimensions[column].width = 25
        wb.save(excel_file)
        wb.close()

    except FileNotFoundError:
        print("Excel file not found.")
    except InvalidFileException:
        print("Invalid Excel file.")
    except CellCoordinatesException:
        print("Error during the table manipulation.")
    except Exception as e:
        print("Error:", e)