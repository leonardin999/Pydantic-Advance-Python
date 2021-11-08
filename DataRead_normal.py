"""
Basic example showing how to read an validate data from a file
without using pydantic.
data: Book information {title, subtitle,author,...,price }
"""
import json

def main() -> None:
	''' Main Fucntion'''
	with open("./data.json") as books:
		data = json.load(books)
		# print information of the First Book
		print(data[0])
		# print information of the Second Book title
		print(data[1]['title'])

if __name__ =="__main__":
	main()