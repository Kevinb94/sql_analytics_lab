## 🏗 Data Modeling Layers

This project follows a layered analytics engineering architecture commonly used in production data platforms:

```
Source (Raw) → Staging → Reporting
```

### 1️⃣ Source Layer

- Raw tables created directly from CMS NPI files  
- Minimal to no transformation  
- Schema mirrors original file structure  
- Focused on ingestion accuracy  

**Purpose:**  
Preserve the original dataset in its most faithful form and serve as the immutable base layer for all downstream transformations.

---

### 2️⃣ Staging Layer

- Data cleaning and normalization  
- Standardized column naming conventions  
- Type casting and validation  
- Deduplication  
- Data quality checks  
- Flattening or restructuring fields when necessary  

**Purpose:**  
Prepare structured, reliable datasets optimized for analytics workflows and consistent joins.

---

### 3️⃣ Reporting Layer

- Aggregated datasets  
- Provider-level and taxonomy-level summaries  
- Location-based reporting models  
- Performance-optimized tables  
- Analytics-ready schemas  

**Purpose:**  
Deliver business-ready, query-efficient datasets designed for fast aggregations and analytical workloads.