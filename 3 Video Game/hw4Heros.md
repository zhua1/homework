
# Heroes Of Pymoli Data Analysis
* Of the 1163 active players, the vast majority are male (82%). There also exists, a smaller, but notable proportion of female players (17%). The rest are undisclosed/others (1%).

* Our peak age demographic falls between 20-24 (46%) with secondary groups falling between 15-19 (14%) and 25-29 (12%).

* The most popular and profitable item purchased is "Mourning Blade" at a price of $3.64.
-----


```python
import os
import pandas as pd

os.chdir(os.path.join(os.environ["HOMEPATH"], 'Desktop', 'UCIRV201804DATA3-Class-Repository-DATA', '02-Homework', '04-Numpy-Pandas', 'Generators', 'HeroesOfPymoli', 'generated_data'))
print()
print('Make sure your input files (players_complete.csv, purchase_data_3.csv) are in this folder:')
print()
print(os.getcwd())
```

    
    Make sure your input files (players_complete.csv, purchase_data_3.csv) are in this folder:
    
    C:\Users\meifl\Desktop\UCIRV201804DATA3-Class-Repository-DATA\02-Homework\04-Numpy-Pandas\Generators\HeroesOfPymoli\generated_data
    

## Player Count


```python
player = pd.read_csv('players_complete.csv')
# Read in player csv and find # of players
playerNum = player.shape[0]
pd.DataFrame({'Number of Players': [playerNum]})
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Number of Players</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1163</td>
    </tr>
  </tbody>
</table>
</div>



## Purchasing Analysis (Total)


```python
purchase = pd.read_csv('purchase_data_3.csv')
# Get number of unique items
unique_item = len(purchase['Item ID'].unique())
# Get average price
average_price = purchase.Price.sum() / purchase.shape[0]
# Get number of purchases
purchases = purchase.shape[0]
# Get total revenue
revenue = purchase.Price.sum()

pd.DataFrame({'Number of Unique Items': [unique_item],
             'Average Price': ['${:,.2f}'.format(average_price)],
             'Number of Purchases': [purchases],
             'Total Revenue': ['${:,.2f}'.format(revenue)]})
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Average Price</th>
      <th>Number of Purchases</th>
      <th>Number of Unique Items</th>
      <th>Total Revenue</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>$2.92</td>
      <td>78</td>
      <td>64</td>
      <td>$228.10</td>
    </tr>
  </tbody>
</table>
</div>



## Gender Demographics


```python
# Groupby gender and get counts
total_count = purchase.groupby('Gender').count().iloc[:,0]
percentage = total_count / sum(total_count)
# Put in dataframe
df = pd.DataFrame({'Percentage of Players': percentage,
              'Total Count': total_count}).sort_values('Total Count', ascending = False)
df.index.name = ''
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Percentage of Players</th>
      <th>Total Count</th>
    </tr>
    <tr>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Male</th>
      <td>0.820513</td>
      <td>64</td>
    </tr>
    <tr>
      <th>Female</th>
      <td>0.166667</td>
      <td>13</td>
    </tr>
    <tr>
      <th>Other / Non-Disclosed</th>
      <td>0.012821</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>




## Purchasing Analysis (Gender)


```python
purchase_value = purchase.groupby('Gender').sum()['Price']
average_purchase = purchase_value / total_count

df2 = pd.DataFrame({'Purchase Count': total_count,
              'Average Purchase Price': average_purchase.map('${:,.2f}'.format),
              'Total Purchase Value': purchase_value.map('${:,.2f}'.format),
              'Normalized Totals': (purchase_value / playerNum).map('${:,.2f}'.format)})
df2 = df2[['Purchase Count', 'Average Purchase Price', 'Total Purchase Value', 'Normalized Totals']]
df2
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Purchase Count</th>
      <th>Average Purchase Price</th>
      <th>Total Purchase Value</th>
      <th>Normalized Totals</th>
    </tr>
    <tr>
      <th>Gender</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Female</th>
      <td>13</td>
      <td>$3.18</td>
      <td>$41.38</td>
      <td>$0.04</td>
    </tr>
    <tr>
      <th>Male</th>
      <td>64</td>
      <td>$2.88</td>
      <td>$184.60</td>
      <td>$0.16</td>
    </tr>
    <tr>
      <th>Other / Non-Disclosed</th>
      <td>1</td>
      <td>$2.12</td>
      <td>$2.12</td>
      <td>$0.00</td>
    </tr>
  </tbody>
</table>
</div>



## Age Demographics


```python
# Get age bin dataframe
bins = [0, 10, 14, 19, 24, 29, 34, 39, 40]
labels = ['<10', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '+40']
df3 = pd.cut(purchase['Age'], bins=bins, labels=labels).to_frame().Age.value_counts(sort = False).to_frame()
df3['Percentage'] = round(df3.Age / df3.Age.sum(), 2)
df3.columns = ['Total Count', 'Percentage of Players']
df3 = df3[['Percentage of Players', 'Total Count']]
df3
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Percentage of Players</th>
      <th>Total Count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>&lt;10</th>
      <td>0.06</td>
      <td>5</td>
    </tr>
    <tr>
      <th>10-14</th>
      <td>0.04</td>
      <td>3</td>
    </tr>
    <tr>
      <th>15-19</th>
      <td>0.14</td>
      <td>11</td>
    </tr>
    <tr>
      <th>20-24</th>
      <td>0.46</td>
      <td>36</td>
    </tr>
    <tr>
      <th>25-29</th>
      <td>0.12</td>
      <td>9</td>
    </tr>
    <tr>
      <th>30-34</th>
      <td>0.09</td>
      <td>7</td>
    </tr>
    <tr>
      <th>35-39</th>
      <td>0.08</td>
      <td>6</td>
    </tr>
    <tr>
      <th>+40</th>
      <td>0.01</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>



## Purchasing Analysis (Age)


```python
df4 = pd.cut(purchase['Age'], bins=bins, labels=labels).to_frame().Age.value_counts(sort = False).to_frame()
df4.columns = ['Purchase Count']
df4['Total Purchase Value'] = purchase.groupby(pd.cut(purchase['Age'], bins=bins, labels=labels)).sum()['Price']
df4['Average Purchase Price'] = (df4['Total Purchase Value'] / df4['Purchase Count']).map('${:,.2f}'.format)
df4['Normalized Totals'] = (df4['Total Purchase Value'] / playerNum).map('${:,.2f}'.format)
df4['Total Purchase Value'] = df4['Total Purchase Value'].map('${:,.2f}'.format)
 
df4 = df4.iloc[:, [0,2,1,3]]
df4
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Purchase Count</th>
      <th>Average Purchase Price</th>
      <th>Total Purchase Value</th>
      <th>Normalized Totals</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>&lt;10</th>
      <td>5</td>
      <td>$2.76</td>
      <td>$13.82</td>
      <td>$0.01</td>
    </tr>
    <tr>
      <th>10-14</th>
      <td>3</td>
      <td>$2.99</td>
      <td>$8.96</td>
      <td>$0.01</td>
    </tr>
    <tr>
      <th>15-19</th>
      <td>11</td>
      <td>$2.76</td>
      <td>$30.41</td>
      <td>$0.03</td>
    </tr>
    <tr>
      <th>20-24</th>
      <td>36</td>
      <td>$3.02</td>
      <td>$108.89</td>
      <td>$0.09</td>
    </tr>
    <tr>
      <th>25-29</th>
      <td>9</td>
      <td>$2.90</td>
      <td>$26.11</td>
      <td>$0.02</td>
    </tr>
    <tr>
      <th>30-34</th>
      <td>7</td>
      <td>$1.98</td>
      <td>$13.89</td>
      <td>$0.01</td>
    </tr>
    <tr>
      <th>35-39</th>
      <td>6</td>
      <td>$3.56</td>
      <td>$21.37</td>
      <td>$0.02</td>
    </tr>
    <tr>
      <th>+40</th>
      <td>1</td>
      <td>$4.65</td>
      <td>$4.65</td>
      <td>$0.00</td>
    </tr>
  </tbody>
</table>
</div>



## Top Spenders


```python
df5 = purchase.groupby('SN')['Price'].sum().sort_values(ascending = False).to_frame()
df5.columns = ['Total Purchase Value']
df5['Purchase Count'] = purchase.groupby('SN')['SN'].count()
df5['Average Purchase Price'] = (df5['Total Purchase Value'] / df5['Purchase Count']).map('${:,.2f}'.format)
df5['Total Purchase Value'] = df5['Total Purchase Value'].map('${:,.2f}'.format)
df5 = df5.iloc[:, [1,2,0]]
df5.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Purchase Count</th>
      <th>Average Purchase Price</th>
      <th>Total Purchase Value</th>
    </tr>
    <tr>
      <th>SN</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Sundaky74</th>
      <td>2</td>
      <td>$3.71</td>
      <td>$7.41</td>
    </tr>
    <tr>
      <th>Aidaira26</th>
      <td>2</td>
      <td>$2.56</td>
      <td>$5.13</td>
    </tr>
    <tr>
      <th>Eusty71</th>
      <td>1</td>
      <td>$4.81</td>
      <td>$4.81</td>
    </tr>
    <tr>
      <th>Chanirra64</th>
      <td>1</td>
      <td>$4.78</td>
      <td>$4.78</td>
    </tr>
    <tr>
      <th>Alarap40</th>
      <td>1</td>
      <td>$4.71</td>
      <td>$4.71</td>
    </tr>
  </tbody>
</table>
</div>



## Most Popular Items


```python
df6 = purchase.groupby(['Item ID', 'Item Name'])['Item ID'].count().sort_values(ascending = False).to_frame()
df6.columns = ['Purchase Count']
df6['Total Purchase Value'] = purchase.groupby(['Item ID', 'Item Name'])['Price'].sum()
df6['Item Price'] = (df6['Total Purchase Value'] / df6['Purchase Count']).map('${:,.2f}'.format)
df6['Total Purchase Value'] = df6['Total Purchase Value'].map('${:,.2f}'.format)
df6 = df6.iloc[:, [0,2,1]]
df6.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>Purchase Count</th>
      <th>Item Price</th>
      <th>Total Purchase Value</th>
    </tr>
    <tr>
      <th>Item ID</th>
      <th>Item Name</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>94</th>
      <th>Mourning Blade</th>
      <td>3</td>
      <td>$3.64</td>
      <td>$10.92</td>
    </tr>
    <tr>
      <th>98</th>
      <th>Deadline, Voice Of Subtlety</th>
      <td>2</td>
      <td>$1.29</td>
      <td>$2.58</td>
    </tr>
    <tr>
      <th>117</th>
      <th>Heartstriker, Legacy of the Light</th>
      <td>2</td>
      <td>$4.71</td>
      <td>$9.42</td>
    </tr>
    <tr>
      <th>111</th>
      <th>Misery's End</th>
      <td>2</td>
      <td>$1.79</td>
      <td>$3.58</td>
    </tr>
    <tr>
      <th>154</th>
      <th>Feral Katana</th>
      <td>2</td>
      <td>$4.11</td>
      <td>$8.22</td>
    </tr>
  </tbody>
</table>
</div>



## Most Profitable Items


```python
df7 = purchase.groupby(['Item ID', 'Item Name'])['Price'].sum().sort_values(ascending = False).to_frame()
df7.columns = ['Total Purchase Value']
df7['Purchase Count'] = purchase.groupby(['Item ID', 'Item Name'])['Item ID'].count()
df7['Item Price'] = (df7['Total Purchase Value'] / df7['Purchase Count']).map('${:,.2f}'.format)
df7['Total Purchase Value'] = df7['Total Purchase Value'].map('${:,.2f}'.format)
df7 = df7.iloc[:, [1,2,0]]
df7.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>Purchase Count</th>
      <th>Item Price</th>
      <th>Total Purchase Value</th>
    </tr>
    <tr>
      <th>Item ID</th>
      <th>Item Name</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>94</th>
      <th>Mourning Blade</th>
      <td>3</td>
      <td>$3.64</td>
      <td>$10.92</td>
    </tr>
    <tr>
      <th>117</th>
      <th>Heartstriker, Legacy of the Light</th>
      <td>2</td>
      <td>$4.71</td>
      <td>$9.42</td>
    </tr>
    <tr>
      <th>93</th>
      <th>Apocalyptic Battlescythe</th>
      <td>2</td>
      <td>$4.49</td>
      <td>$8.98</td>
    </tr>
    <tr>
      <th>90</th>
      <th>Betrayer</th>
      <td>2</td>
      <td>$4.12</td>
      <td>$8.24</td>
    </tr>
    <tr>
      <th>154</th>
      <th>Feral Katana</th>
      <td>2</td>
      <td>$4.11</td>
      <td>$8.22</td>
    </tr>
  </tbody>
</table>
</div>


