import camelot

pdf_path = "test.pdf"

tables = camelot.read_pdf(pdf_path, pages = "1-end")

print(len(tables))


print(tables[0].df)
for i in range(len(tables)):
	tables[i].to_csv(f"table_{i}.csv")
