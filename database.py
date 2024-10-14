"""Работа с базой данных"""

import sqlite3 as sq
from io import StringIO

def make_file_with_all_participants(all_participants):
	output = StringIO()

	column_names = ['telegram_id', 'funpay_id']
	output.write('\t'.join(column_names) + '\n')

	# Записываем строки с данными
	for row in all_participants:
		output.write('\t'.join(map(str, row)) + '\n')

	# Возвращаемся в начало объекта StringIO
	output.seek(0)

	return output

class DatabaseSQ:

	def __init__(self, db_file):
		self.file = db_file
	# 	self.connection = sq.connect(db_file)

	def create_table(self):
		with sq.connect(self.file) as con:
			cur = con.cursor()
			cur.execute("CREATE TABLE IF NOT EXISTS users (telegram_id INTEGER PRIMARY KEY, funpay_id INTEGER UNIQUE)")
			con.commit()

	def get_user(self, chat_id):
		with sq.connect(self.file) as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM users WHERE telegram_id = ?', (chat_id,)).fetchall()
			return bool(result)

	def add_user(self, chat_id):
		with sq.connect(self.file) as con:
			cur = con.cursor()
			cur.execute('INSERT INTO users (telegram_id) VALUES (?)', (chat_id,))
			con.commit()

	def add_funpay_id(self, chat_id, funpay_id):
		with sq.connect(self.file) as con:
			cur = con.cursor()
			try:
				cur.execute('UPDATE users SET funpay_id = ? WHERE telegram_id = ?', (funpay_id,chat_id,))
				con.commit()
				return True
			except Exception as ex:
				return False

	def get_info(self, chat_id):
		with sq.connect(self.file) as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM users WHERE telegram_id = ?', (chat_id,)).fetchall()
			return result

	def get_all_info(self):
		with sq.connect(self.file) as con:
			cur = con.cursor()
			res = cur.execute('SELECT * FROM users WHERE funpay_id IS NOT NULL').fetchall()
			return res