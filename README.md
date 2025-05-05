# erajaya-training-17

PT Erajaya Swasembada Tbk training repository

# Python Basics for Odoo Development

This guide covers the essential Python concepts needed for Odoo 
development. It includes basic Python syntax and common patterns used in 
Odoo modules.

## Table of Contents
- [Data Types](#data-types)
- [Comparison Operators](#comparison-operators)
- [Variables](#variables)
- [Looping](#looping)
- [Conditional Statements](#conditional-statements)

## Data Types

Common data types you'll encounter in Odoo development.

### String (str)
Used for text data like names and codes:
```python
name = "Product A"             # Product names
code = 'P001'                 # Product codes
```

### Number
For numerical values like prices and quantities:
```python
price = 1500.75               # Float for prices
quantity = 42                 # Integer for quantities
```

### List
For collections of items:
```python
products = ['Laptop', 'Mouse'] # Collection of items
prices = [1500, 25.5]         # List of numbers
```

### Dictionary
For key-value pairs, commonly used in Odoo records:
```python
product = {
    'name': 'Laptop',         # Key-value pairs
    'price': 1500.75,         # Often used in Odoo records
    'qty': 5
}
```

### List of Dictionary
```
products = [
    {
        'name': 'Laptop',
        'price': 1500.00,
        'specs': {
            'processor': 'i7',
            'ram': '16GB',
            'storage': '512GB'
        },
        'supplier': {
            'name': 'TechCorp',
            'contact': '123-456-789'
        }
    },
    {
        'name': 'Mouse',
        'price': 25.50,
        'specs': {
            'type': 'Wireless',
            'dpi': '1600',
            'buttons': 6
        },
        'supplier': {
            'name': 'AccessoryWorld',
            'contact': '987-654-321'
        }
    }
]

# Access single value
print(products[0]['name'])           # Output: Laptop

# Loop through products
for product in products:
    print(f"Name: {product['name']}, Price: {product['price']}")

# Filter products
expensive_products = [p for p in products if p['price'] > 1000]

# Access nested data
print(products[0]['specs']['processor'])  # Output: i7
```

### Boolean
For true/false values:
```python
active = True                 # Status flags
available = False             # Availability checks
```

## Comparison Operators

### Basic Comparisons
```python
price == 1000    # Equal to
price != 1000    # Not equal to
price > 1000     # Greater than
price >= 1000    # Greater than or equal
price < 1000     # Less than
price <= 1000    # Less than or equal
```

### Odoo Domain Examples
```python
[('price', '>', 1000)]        # Price greater than 1000
[('name', '=', 'Laptop')]     # Name equals Laptop
[('qty', '>=', 10)]           # Quantity at least 10
```

### Multiple Conditions
```python
# Odoo domain with multiple conditions
[
    ('price', '>', 1000),
    ('qty', '>', 0),
    '|',                      # OR operator
    ('active', '=', True),
    ('special', '=', True)
]
```

## Variables

### Basic Variables
```python
name = "Product A"
price = 1500.75
is_available = True
```

### Odoo Record Variables
```python
# Record reference
product = self.env['product.template']

# Record set
products = product.search([])

# Single record
laptop = product.browse(1)
```

### Computed Fields
```python
@api.depends('price', 'quantity')
def _compute_total(self):
    self.total = self.price * self.quantity
```

## Looping

### For Loop with Lists
```python
# Iterate through records
for product in products:
    product.price *= 1.1  # Increase price by 10%
```

### For Loop with Dictionary
```python
# Process product data
for key, value in product.items():
    print(f"{key}: {value}")
```

### Recordset Iteration
```python
# Process Odoo recordset
for record in self.search([]):
    record.do_something()
```

### List Comprehension
```python
# Create list of names
names = [p.name for p in products]
```

## Conditional Statements

### Basic If Statement
```python
if product.quantity <= 0:
    product.status = 'out_of_stock'
```

### If-Else Statement
```python
if product.price > 1000:
    product.category = 'premium'
else:
    product.category = 'standard'
```

### If-Elif-Else
```python
if product.quantity > 100:
    discount = 0.2  # 20% discount
elif product.quantity > 50:
    discount = 0.1  # 10% discount
else:
    discount = 0    # No discount
```

### Conditional with AND/OR
```python
if product.active and product.quantity > 0:
    product.state = 'available'

if product.price < 100 or product.on_sale:
    product.featured = True
```


## 💡 Launch Odoo
### Terminal command
Run Odoo:
```bash
python odoo-17.0.post20250206/odoo-bin -c odoo.conf
```

Run Odoo with specific Database:
```bash
python odoo-17.0.post20250206/odoo-bin -c odoo.conf -d v17_yazaki_training -u arkana_academy
```

Run Odoo with specific Database & do Addons upgrade:
```bash
python odoo-17.0.post20250206/odoo-bin -c odoo.conf -d v17_yazaki_training -u arkana_academy
```


## 💡 Scaffold an Odoo Addons
### Basic Command
```bash
./odoo-bin scaffold <module_name> <path>
```

Example:
```bash
./odoo-bin scaffold arkana_academy custom-addons
```

## 📁 Module Structure

After running scaffold, you'll get this structure:
```
library_app/
├── __init__.py
├── __manifest__.py
├── controllers/
│   ├── __init__.py
│   └── controllers.py
├── demo/
│   └── demo.xml
├── models/
│   ├── __init__.py
│   └── models.py
├── security/
│   └── ir.model.access.csv
└── views/
    └── views.xml
```

## Additional Resources
- [Official Python Documentation](https://docs.python.org/3/)
- [Odoo Development 
Documentation](https://www.odoo.com/documentation/17.0/developer.html)
- [Odoo ORM API 
Reference](https://www.odoo.com/documentation/17.0/developer/reference/orm.html)

## Contributing
Feel free to contribute to this guide by submitting pull requests or 
creating issues for improvements.

## License
This documentation is released under the MIT License. See the LICENSE file 
for details.
