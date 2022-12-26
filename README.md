# family tree generator
* Our project aims to convert the data available from the electoral database into a computer readable format that can be easily stored in the database and later on used to find the family tree of an individual along with labeled relations.

* Conversion of PDF into BSON using OCR (Optical Character Recognition) : As informed to us in the problem statement, we have collected the PDF files of details of people from the Electoral Roll PDF. The next step was to store the data from these PDF files into a database so that it can be fed into our algorithm to find the relationships of a particular individual. This task had to be automated as the PDF files had a huge number of entries and this could not be done manually.

* We extracted boxed images from these PDF files containing a particular person’s details and then applied OCR ( optical character recognition ) on it. This helped us to automate the process of reading details from the PDF files. The extracted information was later on fed into the MongoDB database and it got converted into BSON format.

### Algorithm

1. We are fetching the relevant data from the electoral roll website using web scraping. From the scraped data, we are retrieving information based on the address/location of a particular individual. This in turn would help us know the people who are residing in the same locality as the individual and hence it is probable that they might belong to the individual’s family.

2. Then we are finding the relatives of the particular individual based on relations given in the data and are building a graph with dependencies which are later being resolved to get clear associations amongst the various individuals. This data is then formed into a tree-like structure and relations of the individual are labeled and displayed by the API.

3. The API has three end points and we have described them below :
   - It provides details of an individual on the basis of their voter ID number.
   - It provides visualized data on the basis of the various states.
   - It provides the family tree of an individual along with the labeled relations.
