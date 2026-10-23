from getpass import getpass
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL


BASE_DIR = Path(__file__).resolve().parent.parent
CLEAN_DIR = BASE_DIR / "data" / "cleaned"


def main():
	csv_files = sorted(CLEAN_DIR.glob("*_cleaned.csv"))
	if not csv_files:
		raise SystemExit(f"No cleaned CSV files found in {CLEAN_DIR}")

	host = input("MySQL host [localhost]: ").strip() or "localhost"
	port = input("MySQL port [3306]: ").strip() or "3306"
	username = input("MySQL username: ").strip()
	password = getpass("MySQL password: ")
	database = input("MySQL schema/database name: ").strip()

	if not username or not database:
		raise SystemExit("MySQL username and schema/database name are required.")

	connection_url = URL.create(
		"mysql+pymysql",
		username=username,
		password=password,
		host=host,
		port=int(port),
		database=database,
	)

	print(f"\nImporting {len(csv_files)} CSV files into '{database}'.")
	print("Existing tables with matching names will be replaced.\n")

	try:
		with create_engine(connection_url).begin() as connection:
			for csv_file in csv_files:
				table_name = csv_file.stem.removesuffix("_cleaned")
				dataframe = pd.read_csv(csv_file, low_memory=False)
				dataframe.to_sql(
					table_name,
					con=connection,
					if_exists="replace",
					index=False,
					chunksize=1000,
					method="multi",
				)
				print(f"Imported {csv_file.name} -> {table_name} ({len(dataframe)} rows)")
	except Exception as error:
		raise SystemExit(f"Import failed: {error}") from error

	print("\nAll CSV files imported successfully.")


if __name__ == "__main__":
	main()
