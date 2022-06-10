import requests
import lxml.html as lh
import pandas as pd
from IPython.display import display

url1 = 'https://hotinsocialmedia.com/most-followed-instagram-accounts/'  # Instagram
url2 = ''  # Youtube
url3 = ''  # TikTok
page = requests.get(url1)  # Store the contents of the website under doc
doc = lh.fromstring(page.content)  # Parse data that are stored between <tr>..</tr> of HTML
tr_elements = doc.xpath('//tr')

# Check the length of the first 12 rows
[len(T) for T in tr_elements[:5]]

tr_elements = doc.xpath('//tr')  # Create empty list
col = []
i = 0  # For each row, store each first element (header) and an empty list
for t in tr_elements[0]:
    i += 1
    name = t.text_content()
    print('%d:"%s"' % (i, name))
    col.append((name, []))

print(len(tr_elements))

# Since out first row is the header, data is stored on the second row onwards
for j in range(1, len(tr_elements)):
    # T is our j'th row
    T = tr_elements[j]

    # If row is not of size 10, the //tr data is not from our table
    if len(T) != 5:
        break

    # i is the index of our column
    i = 0

    # Iterate through each element of the row
    for t in T.iterchildren():
        data = t.text_content()
        # Check if row is empty
        if i > 0:
            # Convert any numerical value to integers
            try:
                data = int(data)
            except:
                pass
        # Append the data to the empty list of the i'th column
        col[i][1].append(data)
        # Increment i for the next column
        i += 1

[len(C) for (title, C) in col]

Dict = {title: column for (title, column) in col}
df = pd.DataFrame(Dict)

# Display crated Data Frame with headers and indexes
display(df)

# CSV file
df.to_csv('instagram.csv', index=False, encoding='utf-8')

# Excel file
df.to_excel('instagram.xlsx', index=False, encoding='utf-8')

# Text file
with open('instagram.txt', 'w', encoding='utf8', newline='') as f:
    dfAsString = df.to_string(header=True, index=False)
    f.write(dfAsString)