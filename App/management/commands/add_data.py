from typing import Any
from App.models import Book
import pandas as pd
from django.core.management.base import BaseCommand
from sqlalchemy import create_engine

class Command(BaseCommand):
    help = "A command to add data from excel file to database"

    def handle(self, *args: Any, **options: Any) -> str | None:
        try:
            # Read the Excel file
            df = pd.read_excel('book.xlsx')
            self.stdout.write(self.style.SUCCESS(f'Successfully read {df.shape[0]} rows from Excel file.'))
            # Create a SQLAlchemy engine for the SQLite database
            engine = create_engine('sqlite:///db.sqlite3')
            
            # Insert the DataFrame into the database table
            df['published_date'] = pd.to_datetime(df['published_date'], errors='coerce').dt.date
            df.to_sql(Book._meta.db_table, con=engine, if_exists='append', index=False)
            # books = Book.objects.all()
            # for book in books:
            #     self.stdout.write(self.style.SUCCESS(f'{book.book_name} - {book.published_date}'))
            self.stdout.write(self.style.SUCCESS('Successfully inserted data into the database.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'An error occurred: {e}'))