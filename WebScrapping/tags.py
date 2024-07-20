from bs4 import BeautifulSoup
import json

with open('scrapping.html', 'r', encoding='utf-8') as f:  # specify encoding
    html_doc = f.read()

soup = BeautifulSoup(html_doc, 'html.parser')

parent_divs = soup.find_all('div',class_='yKfJKb row')

# product names
divs = soup.find_all('div', class_='KzDlHZ')
name_p = []
for div in divs:
    text = div.text.strip()  # Strip any leading/trailing whitespace
    name_p.append(text)


# #product original price
op=[]
for parent in parent_divs:
    # Find child divs with the class that contains the original price
    original_price_divs = parent.find_all('div', class_='yRaY8j ZYYwLA')
    for original_price_div in original_price_divs:
        original_price = original_price_div.text.strip()
        op.append(original_price)

# # missing price from which item
# missing_price_divs = []
# for parent in parent_divs:
#     # Check if this parent div contains the original price class
#     original_price_divs = parent.find_all('div', class_='yRaY8j ZYYwLA')
#     if not original_price_divs:
#         missing_price_divs.append(parent)
# # Print the missing price divs and the number of them
# print(f'Number of divs missing the original price: {len(missing_price_divs)}')
# for div in missing_price_divs:
#     print(div.prettify())

#IQOO Neo9 Pro (Conqueror Black, 256 GB)

#current price
cp=[]
for parent1 in parent_divs:
    current_price_divs = parent1.find_all('div', class_='Nx9bqj _4b5DiR')
    for current_price_div in current_price_divs:
        current_price = current_price_div.text.strip()
        cp.append(current_price)

# #features
parent_divs1 = soup.find_all('div','_6NESgJ')
li_items_2d_list = []
for div in parent_divs1:
    ul = div.find('ul', class_='G4BRas')
    if ul:
        li_items = [li.text.strip() for li in ul.find_all('li', class_='J+igdf')]
        li_items_2d_list.append(li_items)

import pandas as pd

min_length = min(len(name_p), len(cp), len(op), len(li_items_2d_list))
if len(name_p) > min_length:
    name_p = name_p[:min_length]
if len(cp) > min_length:
    cp = cp[:min_length]
if len(op) > min_length:
    op = op[:min_length]
if len(li_items_2d_list) > min_length:
    li_items_2d_list = li_items_2d_list[:min_length]


df = pd.DataFrame({'Product_Name':name_p,'Features':li_items_2d_list,'Original_Price':op,'Current_Price':cp})
print(df)
df.to_csv('products_data1.csv', index=False)
# print(len(op))
# print(len(name_p))
# print(len(cp))
# print(len(li_items_2d_list))
