# Mongo Population
## Requirements

* Python 3.5.2
* pymongo 3.13
* pip 20.3.4

## 1. Install MongoDB Shell

**Download the MongoDB Shell Package:**

```jsx
wget https://downloads.mongodb.com/compass/mongodb-mongosh_1.10.5_amd64.deb
```

**Install the package:**

```jsx
sudo dpkg -i mongodb-mongosh_1.10.5_amd64.deb
```

**Verify Installation:**

```jsx
mongosh --version
```

## 2. Verify Connection and Start MongoDB Shell

```jsx
mongosh
```

### 3. Create db

```jsx
use mongodb_presto;
```

### 4. Create Collections for each table

```jsx
db.createCollection("web_returns")
db.createCollection("store_returns")
db.createCollection("catalog_sales")
db.createCollection("catalog_returns")
db.createCollection("web_sales")
db.createCollection("store_sales")
db.createCollection("catalog_page")
```

### 5. Run Custom Scripts for each table

from root folder:
python web_sales.py

python web_returns.py

...

### some usefull commands:

```jsx
use mongodb1; #switch database or create
db.catalog_page.countDocuments() #show number of entries
db.catalog_page.find().pretty() #show entries
```
