## AWS Lamda - MICListCC
# Requirement:

1. Download the xlsx
2. Store the xlsx
3. Read the tab titled "MICs List by CC"
4. Create a list of dict containing all rows (except row 1). The values in row 1 would be the keys for in each dict.
5. Store the list from step 4) as a .json file in an AWS S3 bucket
6. The above function should be run as an AWS Lambda
