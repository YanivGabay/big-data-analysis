
# Graph Database Query



```cypher
// Create Users
CREATE (u1:User {user_id: 1}),
       (u2:User {user_id: 2});

// Create Products
CREATE (p1:Product {product_id: 1, price: 100}),
       (p2:Product {product_id: 2, price: 200});

// Create Events
CREATE (e1:Event {event_type: 'view', event_time: timestamp()}),
       (e2:Event {event_type: 'purchase', event_time: timestamp()});

// Create Categories
CREATE (c1:Category {category_code: 'electronics'}),
       (c2:Category {category_code: 'clothing'});

// Create Brands
CREATE (b1:Brand {brand: 'BrandA'}),
       (b2:Brand {brand: 'BrandB'});

// Create Sessions
CREATE (s1:Session {user_session: 'session1'}),
       (s2:Session {user_session: 'session2'});

// Create Relationships
// User performs Event
CREATE (u1)-[:PERFORMS]->(e1),
       (u2)-[:PERFORMS]->(e2);

// Event involves Product
CREATE (e1)-[:INVOLVES]->(p1),
       (e2)-[:INVOLVES]->(p2);

// Event occurs in Session
CREATE (e1)-[:OCCURS_IN]->(s1),
       (e2)-[:OCCURS_IN]->(s2);

// Product belongs to Category
CREATE (p1)-[:BELONGS_TO]->(c1),
       (p2)-[:BELONGS_TO]->(c2);

// Product branded as Brand
CREATE (p1)-[:BRANDED_AS]->(b1),
       (p2)-[:BRANDED_AS]->(b2);
```