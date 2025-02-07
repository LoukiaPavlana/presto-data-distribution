# MongoDB Deployment

## References
* [Installation Guide](https://www.digitalocean.com/community/tutorials/how-to-configure-remote-access-for-mongodb-on-ubuntu-20-04)

## Version:

```jsx
cat /etc/lsb-release
```
## Dependencies
DISTRIB_ID=Ubuntu
DISTRIB_RELEASE=16.04
DISTRIB_CODENAME=xenial
DISTRIB_DESCRIPTION="Ubuntu 16.04.7 LTS"

### **1. Import the MongoDB Public Key**

MongoDB requires a public key to verify the packages. Run this command to import it:

```bash
wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
```

### **2. Create the MongoDB List File**

Next, add the MongoDB repository to your package manager sources. For **Ubuntu 16.04**, run:

```bash
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list
```

This command sets the MongoDB 4.4 repository. MongoDB 4.4 is compatible with Ubuntu 16.04 (Xenial).

### **3. Update Package Database**

Update your local package database to include the MongoDB packages:

```bash
sudo apt-get update
```

### **4. Install MongoDB**

Now, install MongoDB by running:

```bash
sudo apt-get install -y mongodb-org
```

This will install the MongoDB server along with its related tools.

### **5. Start MongoDB**

Once the installation is complete, you can start the MongoDB service:

```bash
sudo systemctl start mongod
```

### **6. Enable MongoDB to Start on Boot**

To make sure MongoDB starts automatically on boot:

```bash
sudo systemctl enable mongod
```

### **7. Verify Installation**

To confirm that MongoDB is running properly, use:  **To run mongo shell: mongosh**

```bash
sudo systemctl status mongod
```

```jsx
mongo --username presto_user --password --authenticationDatabase presto
```
