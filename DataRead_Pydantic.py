"""
Basic example showing how to read an validate data from a file with pydantic.
data: Book information {title, subtitle,author,...,price }
"""
import json
import pydantic
from typing import Optional,List

## customize the error message 
class ISBNMissingError(Exception):
	''' Custom error that is raised when both ISBN10 and ISBN13 are missing. '''
	def __init__(self, title: str, message: str) -> None:
		self.title = title
		self.message = message
		super().__init__(message)

class ISBN10FormatError(Exception):
	''' Custom error that is raised when ISBN10 doesn't have the right format. '''
	def __init__(self, value: str, message: str) -> None:
		self.value = value
		self.message = message
		super().__init__(message)


class Book(pydantic.BaseModel):
	title: str
	author: str
	publisher: str
	price: float
	isbn_10: Optional[str]
	isbn_13: Optional[str]
	subtitle: Optional[str]

	## model-level validation
	## validated the value before(pre=) or after(post=) convert into the model 
	@pydantic.root_validator(pre=True)
	@classmethod
	def check_number_visiblity(cls,values):
		""" Make sure there is either an isbn 10 or isbn 13 value defined."""
		if "isbn_10" not in values and "isbn_13" not in values:
			raise ISBNMissingError(
				title=values["title"],message=values["Document should have either isbn10 or isbn13"]
				)
		return values

	## isbn number have a weighted sum of these number should dvisible by 11.
	## create the function to check the validation of these isbn number
	@pydantic.validator("isbn_10")
	@classmethod
	def isbn_10_valid(cls, value) -> None:
		""" Validator to check whether ISBN10 has a valird value
		--> Filter the string of isbn number to the list of character
		--> List of Character shouldn't contain: dasher, empty space,etc..
		--> Digital number 10 has a symbol : X and x in isbn_10 number
		"""
		chars = [c for c in value if c in "0123456789Xx"]
		if len(chars)!=10:
			raise ISBN10FormatError (
				value=value, message="ISBN10 should be 10 digits."
				)

		def int_convert(char: str) -> int:
			if char in "Xx":
				return 10
			return int(char)

		## computed the weighted sum using the List comprehension
		weighted_sum=sum((10-i)*int_convert(x) for i, x in enumerate(chars))
		if weighted_sum %11 !=0:
			raise ISBN10FormatError (
				value=value, message="ISBN10 digit sum should be divisible by 11."
				)
		return value

	class Config:
		## make sure the Attributes of the objects are immutable
		allow_mutation = False
		## Automatically convert all string values to lowcases
		anystr_lower = True

def main() -> None:
	''' Main Fucntion'''
	with open("./data.json") as books:
		data = json.load(books)
		## (**items) using when unpacking the item into keyword arguments
		## --> help to set the right values to the right attributes items Book Class
		libraries: List[Book] = [Book(**item) for item in data]

		#libraries[0].title = "Changing the Title of the Book" # TypeError: "Book" is immutable and does not support item assignment
		# Print the information of the First book:
		print(libraries[0])
		# print the title of the second Book by acessing the attributes of the book class
		print(libraries[1].title)

		# easily convert the datatypes to dictionary type
		print("Without the title:....")
		print(libraries[2].dict(exclude={"title"}))

		print("Only cotain the title:....")
		print(libraries[2].dict(include={"title"}))
if __name__ =="__main__":
	main()