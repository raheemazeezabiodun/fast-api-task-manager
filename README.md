DATABASE CREATION

```sql

CREATE DATABASE deep_medical_app;
CREATE USER deep_medical_user WITH PASSWORD 'deepmedical';
GRANT ALL PRIVILEGES ON DATABASE deep_medical_user TO deep_medical_app;
ALTER USER deep_medical_user WITH SUPERUSER;
```