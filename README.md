# Comprehensive Python & Odoo Development Guide

## Table of Contents
- [1. Native Python Knowledge](#1-native-python-knowledge)
- [2. Odoo-Specific Knowledge](#2-odoo-specific-knowledge)
- [3. Odoo Development Workflow](#3-odoo-development-workflow)
- [4. Resources & Best Practices](#4-resources--best-practices)

---

## 1. Native Python Knowledge

### Data Types

#### Basic Data Types
| Type | Description | Examples | Common Uses in Odoo |
|------|-------------|----------|---------------------|
| **String (str)** | Text data | `name = "Product A"`, `code = 'P001'` | Product names, codes, references |
| **Integer (int)** | Whole numbers | `quantity = 42`, `priority = 1` | Quantities, IDs, counts, sequence numbers |
| **Float** | Decimal numbers | `price = 1500.75`, `weight = 2.5` | Prices, measurements, rates |
| **Boolean** | True/false values | `active = True`, `available = False` | Status flags, visibility controls |

#### Composite Data Types
| Type | Description | Example | 
|------|-------------|---------|
| **List** | Ordered, mutable collection | `products = ['Laptop', 'Mouse']` |
| **Dictionary** | Key-value pairs | `product = {'name': 'Laptop', 'price': 1500.75}` |
| **Tuple** | Ordered, immutable collection | `dimensions = (10, 20, 30)` |

#### Complex Data Structures

**List of Dictionaries** (commonly used in Odoo)
```python
products = [
    {
        'name': 'Laptop',
        'price': 1500.00,
        'specs': {
            'processor': 'i7',
            'ram': '16GB',
            'storage': '512GB'
        }
    },
    {
        'name': 'Mouse',
        'price': 25.50,
        'specs': {
            'type': 'Wireless',
            'dpi': '1600',
            'buttons': 6
        }
    }
]
```

**Accessing Nested Data**
```python
# Basic access
print(products[0]['name'])                 # Output: Laptop

# Nested access
print(products[0]['specs']['processor'])   # Output: i7

# Iterating through complex structures
for product in products:
    print(f"Product: {product['name']}")
    print("Specifications:")
    for key, value in product['specs'].items():
        print(f"  - {key}: {value}")
```

### Comparison Operators

| Operator | Description | Example | Odoo Domain Example |
|----------|-------------|---------|---------------------|
| `==` | Equal to | `price == 1000` | `[('price', '=', 1000)]` |
| `!=` | Not equal to | `price != 1000` | `[('price', '!=', 1000)]` |
| `>` | Greater than | `price > 1000` | `[('price', '>', 1000)]` |
| `>=` | Greater than or equal | `price >= 1000` | `[('price', '>=', 1000)]` |
| `<` | Less than | `price < 1000` | `[('price', '<', 1000)]` |
| `<=` | Less than or equal | `price <= 1000` | `[('price', '<=', 1000)]` |
| `in` | Contained in | `status in ['new', 'used']` | `[('status', 'in', ['new', 'used'])]` |
| `not in` | Not contained in | `status not in ['broken']` | `[('status', 'not in', ['broken'])]` |

### Variables and Assignment

**Basic Variables**
```python
# Variables are created when assigned a value
name = "Product A"       # String assignment
price = 1500.75          # Float assignment
is_available = True      # Boolean assignment
count = None             # None value (similar to null in other languages)

# Multiple assignment
x, y, z = 1, 2, 3
```

**Variable Naming Conventions**
- Use lowercase with underscores for variable names (snake_case)
- Constants are typically uppercase: `MAX_ITEMS = 100`
- Class names use CamelCase: `class ProductTemplate:`
- Avoid reserved keywords (if, for, class, etc.)

### Looping Structures

**For Loops**
```python
# Iterating through a list
products = ['Laptop', 'Mouse', 'Keyboard']
for product in products:
    print(product)

# Iterating with index
for i, product in enumerate(products):
    print(f"{i}: {product}")
    
# Iterating through dictionary
product_info = {'name': 'Laptop', 'price': 1500.75, 'qty': 5}
for key, value in product_info.items():
    print(f"{key}: {value}")
```

**List Comprehensions**
```python
# Basic list comprehension
prices = [100, 200, 300, 400, 500]
doubled_prices = [p * 2 for p in prices]  # [200, 400, 600, 800, 1000]

# List comprehension with condition
expensive = [p for p in prices if p > 300]  # [400, 500]

# Dictionary comprehension
price_map = {f"item_{i}": price for i, price in enumerate(prices)}
# {'item_0': 100, 'item_1': 200, 'item_2': 300, 'item_3': 400, 'item_4': 500}
```

**While Loops**
```python
# Basic while loop
counter = 0
while counter < 5:
    print(counter)
    counter += 1
```

### Conditional Statements

**Basic If Statement**
```python
if quantity <= 0:
    print("Out of stock")
```

**If-Else Statement**
```python
if price > 1000:
    category = 'premium'
else:
    category = 'standard'
```

**If-Elif-Else Chain**
```python
if quantity > 100:
    discount = 0.2  # 20% discount
elif quantity > 50:
    discount = 0.1  # 10% discount
elif quantity > 20:
    discount = 0.05  # 5% discount
else:
    discount = 0    # No discount
```

**Conditional with AND/OR**
```python
# Using AND (both conditions must be True)
if product.active and product.quantity > 0:
    state = 'available'

# Using OR (at least one condition must be True)
if product.price < 100 or product.on_sale:
    featured = True
    
# Complex condition with parentheses for clarity
if (price > 1000 and quantity > 5) or (is_premium and quantity > 0):
    eligible_for_discount = True
```

**Ternary Operator (Conditional Expression)**
```python
# Format: value_if_true if condition else value_if_false
status = "In Stock" if quantity > 0 else "Out of Stock"
```

---

## 2. Odoo-Specific Knowledge

### Odoo Model Structure

**Basic Model Definition**
```python
from odoo import models, fields, api

class ProductCustom(models.Model):
    _name = 'product.custom'       # Database table name
    _description = 'Custom Product' # User-friendly description
    
    # Basic fields
    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code')
    price = fields.Float(string='Price')
    quantity = fields.Integer(string='Quantity', default=1)
    active = fields.Boolean(string='Active', default=True)
    
    # Relational fields
    category_id = fields.Many2one('product.category', string='Category')
    tag_ids = fields.Many2many('product.tag', string='Tags')
    variant_ids = fields.One2many('product.variant', 'product_id', string='Variants')
    
    # Computed field
    @api.depends('price', 'quantity')
    def _compute_total(self):
        for record in self:
            record.total = record.price * record.quantity
    
    total = fields.Float(string='Total', compute='_compute_total', store=True)
    
    # Constraints
    _sql_constraints = [
        ('unique_code', 'UNIQUE(code)', 'The code must be unique!')
    ]
    
    @api.constrains('price')
    def _check_price(self):
        for record in self:
            if record.price < 0:
                raise ValidationError("Price cannot be negative")
                
    # CRUD methods override
    @api.model
    def create(self, vals):
        if not vals.get('code'):
            vals['code'] = self.env['ir.sequence'].next_by_code('product.custom')
        return super(ProductCustom, self).create(vals)
```

### Common Field Types

| Field Type | Description | Example |
|------------|-------------|---------|
| `Char` | String | `name = fields.Char(string='Name')` |
| `Text` | Multiline text | `description = fields.Text(string='Description')` |
| `Integer` | Whole number | `quantity = fields.Integer(string='Quantity')` |
| `Float` | Decimal number | `price = fields.Float(string='Price', digits=(16, 2))` |
| `Monetary` | Currency amount | `amount = fields.Monetary(string='Amount', currency_field='currency_id')` |
| `Boolean` | True/False | `active = fields.Boolean(string='Active')` |
| `Date` | Date only | `date = fields.Date(string='Date')` |
| `Datetime` | Date and time | `created_at = fields.Datetime(string='Created At')` |
| `Selection` | Dropdown | `state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed'), ('done', 'Done')], string='State', default='draft')` |
| `Binary` | File storage | `image = fields.Binary(string='Image')` |
| `Html` | HTML content | `content = fields.Html(string='Content')` |

### Relational Fields

| Field Type | Description | Example |
|------------|-------------|---------|
| `Many2one` | Many records can reference one record | `category_id = fields.Many2one('product.category', string='Category')` |
| `One2many` | One record can reference many records | `variant_ids = fields.One2many('product.variant', 'product_id', string='Variants')` |
| `Many2many` | Many records can reference many records | `tag_ids = fields.Many2many('product.tag', string='Tags')` |
| `Reference` | Dynamic relation to different models | `related_to = fields.Reference(selection=[('product.template', 'Product'), ('res.partner', 'Partner')], string='Related To')` |

### Odoo ORM Methods

**Record Operations**
```python
# Environment access
self.env                      # Access the environment
self.env.user                 # Current user
self.env.company              # Current company
self.env.context              # Current context

# Model access
self.env['product.template']  # Access a model

# Create
vals = {'name': 'New Product', 'price': 100}
new_product = self.env['product.template'].create(vals)

# Read
product = self.env['product.template'].browse(1)  # By ID
print(product.name)

# Search
products = self.env['product.template'].search([('price', '>', 100)])

# Search count
count = self.env['product.template'].search_count([('active', '=', True)])

# Search with limit and order
products = self.env['product.template'].search(
    [('price', '>', 0)], 
    limit=10, 
    order='price DESC'
)

# Read specific fields
products = self.env['product.template'].search_read(
    [('active', '=', True)],
    fields=['name', 'price']
)

# Update
product.write({'price': 150})

# Unlink (delete)
product.unlink()
```

### Odoo Domain Format

**Basic Domain Format**
```python
# Format: [(field_name, operator, value), ...]
domain = [('price', '>', 100)]
```

**Complex Domain Examples**
```python
# AND condition (implicit between list items)
domain = [
    ('price', '>', 100),
    ('quantity', '>', 0)
]  # price > 100 AND quantity > 0

# OR condition
domain = [
    '|',
    ('price', '<', 100),
    ('discount', '>', 0)
]  # price < 100 OR discount > 0

# Multiple OR conditions
domain = [
    '|', '|',
    ('state', '=', 'sale'),
    ('state', '=', 'done'),
    ('state', '=', 'paid')
]  # state = sale OR state = done OR state = paid

# Combining AND and OR
domain = [
    '&',
    ('price', '>', 100),
    '|',
    ('state', '=', 'available'),
    ('special_offer', '=', True)
]  # price > 100 AND (state = available OR special_offer = True)

# Negation
domain = [
    ('active', '=', True),
    '!',
    ('price', '=', 0)
]  # active = True AND NOT (price = 0)
```

### Computed Fields and Depends

**Computed Fields**
```python
# Basic computed field
@api.depends('price', 'quantity')
def _compute_total(self):
    for record in self:
        record.total = record.price * record.quantity

total = fields.Float(string='Total', compute='_compute_total')

# Stored computed field (saved in database)
@api.depends('line_ids.price', 'line_ids.quantity')
def _compute_order_total(self):
    for order in self:
        order.total = sum(line.price * line.quantity for line in order.line_ids)

total = fields.Float(string='Total', compute='_compute_order_total', store=True)

# Computed field with search method
@api.depends('line_ids.price')
def _compute_is_expensive(self):
    for order in self:
        order.is_expensive = order.total > 1000

def _search_is_expensive(self, operator, value):
    # Return domain for searching records
    if operator == '=' and value:
        return [('total', '>', 1000)]
    return [('total', '<=', 1000)]

is_expensive = fields.Boolean(
    string='Is Expensive', 
    compute='_compute_is_expensive',
    search='_search_is_expensive'
)
```

### Onchange and Constraints

**Onchange Methods**
```python
@api.onchange('product_id')
def _onchange_product(self):
    if self.product_id:
        self.price = self.product_id.list_price
        self.name = self.product_id.name
    else:
        self.price = 0.0
        self.name = ''
```

**Constraints**
```python
# SQL constraints
_sql_constraints = [
    ('unique_code', 'UNIQUE(code)', 'The code must be unique!'),
    ('positive_price', 'CHECK(price >= 0)', 'Price must be positive!')
]

# Python constraints
@api.constrains('start_date', 'end_date')
def _check_dates(self):
    for record in self:
        if record.start_date and record.end_date and record.start_date > record.end_date:
            raise ValidationError("End date cannot be before start date")
```

---

## 3. Odoo Development Workflow

### Module Structure
```
my_module/
├── __init__.py              # Python package initialization
├── __manifest__.py          # Module metadata
├── controllers/             # Web controllers (routes)
│   ├── __init__.py
│   └── controllers.py
├── data/                    # Data files (XML)
│   └── initial_data.xml
├── demo/                    # Demo data (XML)
│   └── demo.xml
├── models/                  # Business logic and data models
│   ├── __init__.py
│   └── models.py
├── security/               
│   ├── ir.model.access.csv  # Access rights
│   └── security.xml         # Record rules
├── static/                  # Static assets
│   ├── description/         # Module screenshots/description
│   ├── src/                 # Source files (JS, CSS)
│   └── lib/                 # Third-party libraries
└── views/                   # UI definitions (XML)
    ├── templates.xml        # QWeb templates
    └── views.xml            # Form, tree, search views
```

### Manifest File (\_\_manifest\_\_.py)
```python
{
    'name': 'My Module',
    'version': '1.0',
    'summary': 'Short summary',
    'description': """
        Detailed description of module functionality.
        Can span multiple lines.
    """,
    'author': 'Your Name',
    'website': 'https://www.example.com',
    'category': 'Uncategorized',
    'depends': [
        'base',
        'sale',
        'product',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/views.xml',
        'views/templates.xml',
        'data/initial_data.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'assets': {
        'web.assets_backend': [
            'my_module/static/src/js/file.js',
            'my_module/static/src/css/style.css',
        ],
    },
}
```

### Launching Odoo

**Terminal Commands**
```bash
# Run Odoo with configuration file
python odoo-17.0.post20250206/odoo-bin -c odoo.conf

# Run Odoo with specific database
python odoo-17.0.post20250206/odoo-bin -c odoo.conf -d v17_erajaya_training

# Run Odoo and update specific module
python odoo-17.0.post20250206/odoo-bin -c odoo.conf -d v17_erajaya_training -u my_module

# Run Odoo in developer mode
python odoo-17.0.post20250206/odoo-bin -c odoo.conf --dev=all

# Common parameters
# -d DATABASE     Specify database name
# -u MODULE       Update module
# -i MODULE       Install module
# --dev=all       Enable all developer features
# --test-enable   Enable tests
# --stop-after-init  Stop server after initialization
```

### Creating a New Module

**Scaffold Command**
```bash
# Basic scaffold command
./odoo-bin scaffold <module_name> <path>

# Example
./odoo-bin scaffold arkana_academy custom-addons
```

**Manual Module Creation**
1. Create module directory structure
2. Create `__manifest__.py` with module metadata
3. Add `__init__.py` files in each directory
4. Create models, views, security files
5. Install module using Odoo UI or update command

### Common Development Tasks

**Creating a Model**
1. Define model class in `models/models.py`
2. Add model access rights in `security/ir.model.access.csv`
3. Create views in `views/views.xml` (form, tree, search)
4. Add menu items in views file

**Adding a Field to Existing Model**
1. Create model class that inherits the existing model
2. Add new field to the model
3. Update the view to display the new field

**Example: Extending an Existing Model**
```python
# In models/models.py
class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'
    
    custom_field = fields.Char('Custom Field')
    
# In views/views.xml
<record id="product_template_form_view_inherit" model="ir.ui.view">
    <field name="name">product.template.form.inherit</field>
    <field name="model">product.template</field>
    <field name="inherit_id" ref="product.product_template_form_view"/>
    <field name="arch" type="xml">
        <field name="categ_id" position="after">
            <field name="custom_field"/>
        </field>
    </field>
</record>
```

---

## 4. Resources & Best Practices

### Development Best Practices

1. **Naming Conventions**
   - Use snake_case for Python identifiers (variables, functions, methods)
   - Use CamelCase for class names
   - Prefix private methods and variables with underscore (_)

2. **Code Organization**
   - Organize models into logical files (e.g., product.py, sale.py)
   - Keep views organized by model
   - Use separate files for data, demo data, security

3. **Security**
   - Always define proper access rights (ir.model.access.csv)
   - Use record rules for row-level security (security.xml)
   - Validate user inputs to prevent security issues

4. **Performance**
   - Use stored computed fields when appropriate
   - Avoid computing values in loops
   - Use prefetch-friendly patterns (e.g., recordset.mapped())
   - Add indexes on frequently filtered fields

5. **Testing**
   - Write tests for critical business logic
   - Use test tags to organize tests
   - Test edge cases and error conditions

### Debugging Techniques

1. **Logging**
   ```python
   import logging
   _logger = logging.getLogger(__name__)
   
   _logger.info('This is an info message')
   _logger.warning('This is a warning')
   _logger.error('This is an error: %s', error_message)
   ```

2. **Debugger**
   - Use `--dev=all` to enable interactive debugger
   - Add `breakpoint()` or `import pdb; pdb.set_trace()` in your code
   - Use developer mode in UI (activate in settings)

3. **SQL Log**
   - Enable SQL logging to see database queries
   - Add to odoo.conf: `log_level = debug_sql`

### Common Design Patterns

1. **Delegation Inheritance**
   ```python
   class ProductSet(models.Model):
       _name = 'product.set'
       _inherits = {'product.template': 'template_id'}
       
       template_id = fields.Many2one('product.template', required=True, ondelete='cascade')
       # Additional fields specific to sets
   ```

2. **Extension Inheritance**
   ```python
   class ProductExtension(models.Model):
       _inherit = 'product.template'
       
       # Add or modify fields and methods
   ```

3. **Abstract Models**
   ```python
   class ProductMixin(models.AbstractModel):
       _name = 'product.mixin'
       
       # Common fields and methods
       
   class ConcreteProduct(models.Model):
       _name = 'concrete.product'
       _inherit = ['product.mixin']
       
       # Additional fields and methods
   ```

### Additional Resources

**Official Documentation**
- [Odoo Development Documentation](https://www.odoo.com/documentation/17.0/developer.html)
- [Odoo ORM API Reference](https://www.odoo.com/documentation/17.0/developer/reference/orm.html)
- [Official Python Documentation](https://docs.python.org/3/)

**Community Resources**
- [Odoo Community Association (OCA)](https://odoo-community.org/)
- [OCA GitHub Repositories](https://github.com/OCA)
- [Odoo Forum](https://www.odoo.com/forum/help-1)

**Books and Tutorials**
- "Odoo Development Essentials" by Daniel Reis
- "Odoo 17 Development Cookbook" (when available)
- "Fluent Python" by Luciano Ramalho (for Python best practices)

---

## Repository Information

**Project Information**
- Repository name: erajaya-training-17
- Organization: PT Erajaya Swasembada Tbk
- Purpose: Training repository for Odoo development

**License**
This documentation is released under the MIT License.
