import camelot


def table_extraction(pdf_path):

	tables = camelot.read_pdf(pdf_path, pages = "1-end")

	print(len(tables))


	print(tables[0].df)
	for i in range(len(tables)):
		tables[i].to_csv(f"table_{i}.csv")
