from services.migration_service import migrate_data

if __name__ == "__main__":
    excel_file = "RESIDENCIAxlsx.ods"

    migrate_data(excel_file)
