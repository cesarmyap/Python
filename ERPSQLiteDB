import sqlite3
from datetime import datetime
import json

class BusinessDatabase:
    def __init__(self, db_name='business_erp.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()
        
    def create_tables(self):
        """Create all necessary tables for the business system"""
        
        # 1. Employees/HR Module
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            position TEXT,
            department TEXT,
            hire_date DATE,
            salary DECIMAL(10, 2),
            status TEXT DEFAULT 'Active',
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # 2. Clients/CRM Module
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            client_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            contact_person TEXT,
            email TEXT,
            phone TEXT,
            address TEXT,
            city TEXT,
            country TEXT,
            tax_id TEXT,
            credit_limit DECIMAL(10, 2),
            payment_terms TEXT DEFAULT 'NET30',
            status TEXT DEFAULT 'Active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            assigned_to INTEGER,
            FOREIGN KEY (assigned_to) REFERENCES employees(employee_id)
        )
        ''')
        
        # 3. Suppliers Module
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS suppliers (
            supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            contact_person TEXT,
            email TEXT,
            phone TEXT,
            address TEXT,
            city TEXT,
            country TEXT,
            tax_id TEXT,
            lead_time_days INTEGER,
            payment_terms TEXT DEFAULT 'NET30',
            status TEXT DEFAULT 'Active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # 4. Products/Inventory Module
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            sku TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            category TEXT,
            unit_price DECIMAL(10, 2) NOT NULL,
            cost_price DECIMAL(10, 2),
            unit_of_measure TEXT DEFAULT 'pcs',
            reorder_level INTEGER DEFAULT 10,
            current_stock INTEGER DEFAULT 0,
            supplier_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
        )
        ''')
        
        # 5. Client Inquiries
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS client_inquiries (
            inquiry_id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            inquiry_date DATE DEFAULT CURRENT_DATE,
            inquiry_details TEXT,
            priority TEXT DEFAULT 'Normal',
            status TEXT DEFAULT 'Open',
            assigned_to INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES clients(client_id),
            FOREIGN KEY (assigned_to) REFERENCES employees(employee_id)
        )
        ''')
        
        # 6. Inquiry Products (Many-to-many relationship)
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS inquiry_products (
            inquiry_product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            inquiry_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            notes TEXT,
            FOREIGN KEY (inquiry_id) REFERENCES client_inquiries(inquiry_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
        ''')
        
        # 7. Quotations
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS quotations (
            quotation_id INTEGER PRIMARY KEY AUTOINCREMENT,
            quotation_number TEXT UNIQUE NOT NULL,
            client_id INTEGER NOT NULL,
            inquiry_id INTEGER,
            issue_date DATE DEFAULT CURRENT_DATE,
            expiry_date DATE,
            status TEXT DEFAULT 'Draft', -- Draft, Sent, Accepted, Rejected, Expired
            total_amount DECIMAL(10, 2),
            tax_percentage DECIMAL(5, 2) DEFAULT 0,
            tax_amount DECIMAL(10, 2),
            grand_total DECIMAL(10, 2),
            terms_and_conditions TEXT,
            prepared_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES clients(client_id),
            FOREIGN KEY (inquiry_id) REFERENCES client_inquiries(inquiry_id),
            FOREIGN KEY (prepared_by) REFERENCES employees(employee_id)
        )
        ''')
        
        # 8. Quotation Items
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS quotation_items (
            quotation_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            quotation_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price DECIMAL(10, 2) NOT NULL,
            discount_percentage DECIMAL(5, 2) DEFAULT 0,
            discount_amount DECIMAL(10, 2) DEFAULT 0,
            line_total DECIMAL(10, 2) NOT NULL,
            estimated_delivery_days INTEGER,
            FOREIGN KEY (quotation_id) REFERENCES quotations(quotation_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
        ''')
        
        # 9. Sales Orders
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales_orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_number TEXT UNIQUE NOT NULL,
            client_id INTEGER NOT NULL,
            quotation_id INTEGER,
            order_date DATE DEFAULT CURRENT_DATE,
            expected_delivery_date DATE,
            status TEXT DEFAULT 'Pending', -- Pending, Confirmed, Processing, Shipped, Delivered, Cancelled
            total_amount DECIMAL(10, 2),
            tax_amount DECIMAL(10, 2),
            grand_total DECIMAL(10, 2),
            payment_terms TEXT,
            shipping_address TEXT,
            billing_address TEXT,
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES clients(client_id),
            FOREIGN KEY (quotation_id) REFERENCES quotations(quotation_id),
            FOREIGN KEY (created_by) REFERENCES employees(employee_id)
        )
        ''')
        
        # 10. Sales Order Items
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales_order_items (
            order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price DECIMAL(10, 2) NOT NULL,
            discount_amount DECIMAL(10, 2) DEFAULT 0,
            line_total DECIMAL(10, 2) NOT NULL,
            status TEXT DEFAULT 'Pending',
            FOREIGN KEY (order_id) REFERENCES sales_orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
        ''')
        
        # 11. Purchase Orders
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS purchase_orders (
            po_id INTEGER PRIMARY KEY AUTOINCREMENT,
            po_number TEXT UNIQUE NOT NULL,
            supplier_id INTEGER NOT NULL,
            order_id INTEGER, -- Link to sales order if needed
            issue_date DATE DEFAULT CURRENT_DATE,
            expected_delivery_date DATE,
            status TEXT DEFAULT 'Draft', -- Draft, Sent, Confirmed, Received, Cancelled
            total_amount DECIMAL(10, 2),
            tax_amount DECIMAL(10, 2),
            grand_total DECIMAL(10, 2),
            payment_terms TEXT,
            shipping_terms TEXT,
            confirmed_date DATE,
            confirmed_by_supplier TEXT,
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id),
            FOREIGN KEY (order_id) REFERENCES sales_orders(order_id),
            FOREIGN KEY (created_by) REFERENCES employees(employee_id)
        )
        ''')
        
        # 12. Purchase Order Items
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS purchase_order_items (
            po_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            po_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price DECIMAL(10, 2) NOT NULL,
            line_total DECIMAL(10, 2) NOT NULL,
            expected_date DATE,
            received_quantity INTEGER DEFAULT 0,
            status TEXT DEFAULT 'Pending',
            FOREIGN KEY (po_id) REFERENCES purchase_orders(po_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
        ''')
        
        # 13. Goods Receipt / Material Receiving
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS goods_receipts (
            receipt_id INTEGER PRIMARY KEY AUTOINCREMENT,
            receipt_number TEXT UNIQUE NOT NULL,
            po_id INTEGER NOT NULL,
            receipt_date DATE DEFAULT CURRENT_DATE,
            received_by INTEGER,
            supplier_delivery_note TEXT,
            status TEXT DEFAULT 'Received',
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (po_id) REFERENCES purchase_orders(po_id),
            FOREIGN KEY (received_by) REFERENCES employees(employee_id)
        )
        ''')
        
        # 14. Goods Receipt Items
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS goods_receipt_items (
            receipt_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            receipt_id INTEGER NOT NULL,
            po_item_id INTEGER NOT NULL,
            quantity_received INTEGER NOT NULL,
            unit_price DECIMAL(10, 2),
            batch_number TEXT,
            expiry_date DATE,
            location TEXT,
            condition TEXT DEFAULT 'Good',
            notes TEXT,
            FOREIGN KEY (receipt_id) REFERENCES goods_receipts(receipt_id),
            FOREIGN KEY (po_item_id) REFERENCES purchase_order_items(po_item_id)
        )
        ''')
        
        # 15. Delivery Notes
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS delivery_notes (
            delivery_id INTEGER PRIMARY KEY AUTOINCREMENT,
            delivery_number TEXT UNIQUE NOT NULL,
            order_id INTEGER NOT NULL,
            delivery_date DATE DEFAULT CURRENT_DATE,
            shipped_by INTEGER,
            shipping_method TEXT,
            tracking_number TEXT,
            status TEXT DEFAULT 'Preparing',
            delivery_address TEXT,
            received_by_client TEXT,
            received_date DATE,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (order_id) REFERENCES sales_orders(order_id),
            FOREIGN KEY (shipped_by) REFERENCES employees(employee_id)
        )
        ''')
        
        # 16. Delivery Note Items
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS delivery_note_items (
            delivery_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            delivery_id INTEGER NOT NULL,
            order_item_id INTEGER NOT NULL,
            quantity_delivered INTEGER NOT NULL,
            batch_number TEXT,
            notes TEXT,
            FOREIGN KEY (delivery_id) REFERENCES delivery_notes(delivery_id),
            FOREIGN KEY (order_item_id) REFERENCES sales_order_items(order_item_id)
        )
        ''')
        
        # 17. Invoices
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS invoices (
            invoice_id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_number TEXT UNIQUE NOT NULL,
            order_id INTEGER NOT NULL,
            delivery_id INTEGER,
            invoice_date DATE DEFAULT CURRENT_DATE,
            due_date DATE,
            status TEXT DEFAULT 'Unpaid', -- Unpaid, Partially Paid, Paid, Overdue, Cancelled
            subtotal DECIMAL(10, 2),
            tax_amount DECIMAL(10, 2),
            grand_total DECIMAL(10, 2),
            amount_paid DECIMAL(10, 2) DEFAULT 0,
            balance_due DECIMAL(10, 2),
            payment_terms TEXT,
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (order_id) REFERENCES sales_orders(order_id),
            FOREIGN KEY (delivery_id) REFERENCES delivery_notes(delivery_id),
            FOREIGN KEY (created_by) REFERENCES employees(employee_id)
        )
        ''')
        
        # 18. Receipts
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS receipts (
            receipt_id INTEGER PRIMARY KEY AUTOINCREMENT,
            receipt_number TEXT UNIQUE NOT NULL,
            invoice_id INTEGER NOT NULL,
            receipt_date DATE DEFAULT CURRENT_DATE,
            receipt_type TEXT, -- Provisional, Official
            payment_method TEXT,
            amount DECIMAL(10, 2) NOT NULL,
            reference_number TEXT,
            notes TEXT,
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (invoice_id) REFERENCES invoices(invoice_id),
            FOREIGN KEY (created_by) REFERENCES employees(employee_id)
        )
        ''')
        
        # 19. Inventory Transactions
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory_transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            transaction_type TEXT, -- Purchase, Sale, Return, Adjustment
            reference_id INTEGER, -- PO ID, SO ID, etc.
            reference_number TEXT,
            quantity_change INTEGER NOT NULL,
            unit_cost DECIMAL(10, 2),
            transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            performed_by INTEGER,
            notes TEXT,
            FOREIGN KEY (product_id) REFERENCES products(product_id),
            FOREIGN KEY (performed_by) REFERENCES employees(employee_id)
        )
        ''')
        
        # 20. Sales Forecasting Data
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales_forecasts (
            forecast_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            forecast_date DATE,
            forecast_period TEXT, -- Daily, Weekly, Monthly, Quarterly, Yearly
            forecasted_quantity INTEGER,
            actual_quantity INTEGER,
            confidence_level DECIMAL(5, 2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
        ''')
        
        # 21. Communication Logs
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS communication_logs (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            entity_type TEXT, -- Client, Supplier, Inquiry, Quotation, Order
            entity_id INTEGER,
            communication_type TEXT, -- Email, Phone, Meeting
            subject TEXT,
            message TEXT,
            direction TEXT, -- Incoming, Outgoing
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (created_by) REFERENCES employees(employee_id)
        )
        ''')
        
        # Create indexes for better performance
        self.create_indexes()
        
        # Insert sample data
        self.insert_sample_data()
        
        self.conn.commit()
        print("Database and tables created successfully!")
    
    def create_indexes(self):
        """Create indexes for frequently queried columns"""
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_clients_email ON clients(email)",
            "CREATE INDEX IF NOT EXISTS idx_suppliers_email ON suppliers(email)",
            "CREATE INDEX IF NOT EXISTS idx_products_sku ON products(sku)",
            "CREATE INDEX IF NOT EXISTS idx_products_category ON products(category)",
            "CREATE INDEX IF NOT EXISTS idx_sales_orders_client ON sales_orders(client_id)",
            "CREATE INDEX IF NOT EXISTS idx_sales_orders_status ON sales_orders(status)",
            "CREATE INDEX IF NOT EXISTS idx_purchase_orders_supplier ON purchase_orders(supplier_id)",
            "CREATE INDEX IF NOT EXISTS idx_invoices_status ON invoices(status)",
            "CREATE INDEX IF NOT EXISTS idx_inventory_transactions_product ON inventory_transactions(product_id)",
            "CREATE INDEX IF NOT EXISTS idx_inventory_transactions_date ON inventory_transactions(transaction_date)",
            "CREATE INDEX IF NOT EXISTS idx_quotations_client ON quotations(client_id)",
            "CREATE INDEX IF NOT EXISTS idx_quotations_status ON quotations(status)"
        ]
        
        for index_sql in indexes:
            self.cursor.execute(index_sql)
    
    def insert_sample_data(self):
        """Insert initial sample data for testing"""
        
        # Check if data already exists
        self.cursor.execute("SELECT COUNT(*) FROM employees")
        if self.cursor.fetchone()[0] == 0:
            
            # Insert sample employee
            self.cursor.execute('''
            INSERT INTO employees (first_name, last_name, email, phone, position, department, hire_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', ('John', 'Doe', 'john@company.com', '+1234567890', 'Sales Manager', 'Sales', '2023-01-15'))
            
            # Insert sample client
            self.cursor.execute('''
            INSERT INTO clients (company_name, contact_person, email, phone, address, city, country)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', ('ABC Corporation', 'Jane Smith', 'jane@abccorp.com', '+0987654321', '123 Main St', 'New York', 'USA'))
            
            # Insert sample supplier
            self.cursor.execute('''
            INSERT INTO suppliers (company_name, contact_person, email, phone, address, city, country, lead_time_days)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', ('Global Supplies Ltd', 'Robert Johnson', 'robert@globalsupplies.com', '+1122334455', '456 Supplier Ave', 'London', 'UK', 14))
            
            # Insert sample products
            sample_products = [
                ('SKU001', 'Laptop Pro', 'High-performance laptop', 'Electronics', 1200.00, 900.00),
                ('SKU002', 'Wireless Mouse', 'Ergonomic wireless mouse', 'Accessories', 25.00, 15.00),
                ('SKU003', 'Monitor 24"', '24-inch LED monitor', 'Electronics', 300.00, 200.00)
            ]
            
            for sku, name, desc, category, price, cost in sample_products:
                self.cursor.execute('''
                INSERT INTO products (sku, name, description, category, unit_price, cost_price, current_stock)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (sku, name, desc, category, price, cost, 100))
            
            self.conn.commit()
            print("Sample data inserted successfully!")
    
    def generate_quotation_number(self):
        """Generate unique quotation number"""
        prefix = "QUOT"
        year = datetime.now().year
        month = datetime.now().strftime('%m')
        
        self.cursor.execute("SELECT COUNT(*) FROM quotations WHERE quotation_number LIKE ?", 
                           (f"{prefix}{year}{month}%",))
        count = self.cursor.fetchone()[0] + 1
        
        return f"{prefix}{year}{month}{count:04d}"
    
    def generate_order_number(self):
        """Generate unique order number"""
        prefix = "SO"
        year = datetime.now().year
        month = datetime.now().strftime('%m')
        
        self.cursor.execute("SELECT COUNT(*) FROM sales_orders WHERE order_number LIKE ?", 
                           (f"{prefix}{year}{month}%",))
        count = self.cursor.fetchone()[0] + 1
        
        return f"{prefix}{year}{month}{count:04d}"
    
    def generate_po_number(self):
        """Generate unique purchase order number"""
        prefix = "PO"
        year = datetime.now().year
        month = datetime.now().strftime('%m')
        
        self.cursor.execute("SELECT COUNT(*) FROM purchase_orders WHERE po_number LIKE ?", 
                           (f"{prefix}{year}{month}%",))
        count = self.cursor.fetchone()[0] + 1
        
        return f"{prefix}{year}{month}{count:04d}"
    
    def update_inventory(self, product_id, quantity_change, transaction_type, reference_id, reference_number, notes=""):
        """Update inventory and log transaction"""
        # Get current stock
        self.cursor.execute("SELECT current_stock, cost_price FROM products WHERE product_id = ?", (product_id,))
        result = self.cursor.fetchone()
        
        if result:
            current_stock, unit_cost = result
            new_stock = current_stock + quantity_change
            
            # Update product stock
            self.cursor.execute('''
            UPDATE products SET current_stock = ? WHERE product_id = ?
            ''', (new_stock, product_id))
            
            # Log inventory transaction
            self.cursor.execute('''
            INSERT INTO inventory_transactions 
            (product_id, transaction_type, reference_id, reference_number, quantity_change, unit_cost, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (product_id, transaction_type, reference_id, reference_number, quantity_change, unit_cost, notes))
            
            return True
        return False
    
    def get_client_statement(self, client_id, start_date=None, end_date=None):
        """Generate statement of accounts for a client"""
        query = '''
        SELECT 
            i.invoice_number,
            i.invoice_date,
            i.due_date,
            i.grand_total,
            i.amount_paid,
            i.balance_due,
            i.status,
            GROUP_CONCAT(DISTINCT o.order_number) as order_numbers
        FROM invoices i
        LEFT JOIN sales_orders o ON i.order_id = o.order_id
        WHERE o.client_id = ?
        '''
        
        params = [client_id]
        
        if start_date:
            query += " AND i.invoice_date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND i.invoice_date <= ?"
            params.append(end_date)
        
        query += " GROUP BY i.invoice_id ORDER BY i.invoice_date DESC"
        
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    def get_sales_statistics(self, start_date, end_date):
        """Get sales statistics for the given period"""
        query = '''
        SELECT 
            strftime('%Y-%m', i.invoice_date) as month,
            COUNT(DISTINCT i.invoice_id) as invoice_count,
            COUNT(DISTINCT o.client_id) as client_count,
            SUM(i.grand_total) as total_sales,
            AVG(i.grand_total) as avg_invoice_amount,
            SUM(i.balance_due) as outstanding_amount
        FROM invoices i
        JOIN sales_orders o ON i.order_id = o.order_id
        WHERE i.invoice_date BETWEEN ? AND ?
        GROUP BY strftime('%Y-%m', i.invoice_date)
        ORDER BY month
        '''
        
        self.cursor.execute(query, (start_date, end_date))
        return self.cursor.fetchall()
    
    def get_product_availability(self, product_id=None, category=None):
        """Check product availability and stock levels"""
        query = '''
        SELECT 
            p.product_id,
            p.sku,
            p.name,
            p.category,
            p.current_stock,
            p.reorder_level,
            p.unit_price,
            CASE 
                WHEN p.current_stock <= 0 THEN 'Out of Stock'
                WHEN p.current_stock <= p.reorder_level THEN 'Low Stock'
                ELSE 'In Stock'
            END as stock_status,
            s.company_name as supplier_name,
            s.lead_time_days
        FROM products p
        LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id
        WHERE 1=1
        '''
        
        params = []
        
        if product_id:
            query += " AND p.product_id = ?"
            params.append(product_id)
        if category:
            query += " AND p.category = ?"
            params.append(category)
        
        query += " ORDER BY p.current_stock ASC"
        
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    def close(self):
        """Close database connection"""
        self.conn.close()

# Example usage
if __name__ == "__main__":
    # Create database
    db = BusinessDatabase('business_system.db')
    
    # Example: Check product availability
    products = db.get_product_availability()
    print("\nProduct Availability:")
    for product in products:
        print(f"{product[2]} - Stock: {product[4]}, Status: {product[7]}")
    
    # Example: Generate a quotation number
    quot_number = db.generate_quotation_number()
    print(f"\nGenerated Quotation Number: {quot_number}")
    
    # Close connection
    db.close()
