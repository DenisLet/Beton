import openpyxl

data = [
    ('SCORE', *(0, 0)),
    ('ULTRA', 0, 0, 0, 0),
    ('SUPER', 2, 0, 0, 2),
    ('HUGE', 1, 1, 0, 0),
    ('STRONG', 3, 0, 1, 2),
    ('LITE', 3, 2, 1, 0),
    ('EQUAL', 14, 1, 3, 10)
]

# Create a new workbook and select the active sheet
workbook = openpyxl.Workbook()
sheet = workbook.active

# Iterate over the data and write it to the sheet
for row_data in data:
    sheet.append(row_data)

# Save the workbook as an Excel file
workbook.save('table.xlsx')