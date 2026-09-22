shop/
│
├── migrations/
│   ├── __init__.py
│   └── 0001_initial.py
│
├── templates/
│   └── shop/
│       ├── shop_home.html
│       ├── product_detail.html
│       ├── purchase_confirm.html
│       └── transaction_history.html
│
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_services.py
│   ├── test_views.py
│   └── test_security.py
│
├── __init__.py
├── admin.py
├── apps.py
├── forms.py
├── models.py
├── services.py
├── urls.py
└── views.py


| Archivo/parte      |      M1      |    M2 (tú)   |      M3      |
| ------------------ | :----------: | :----------: | :----------: |
| `models.py`        | 🟢 Principal |    Revisa    |    Revisa    |
| `migrations/`      |      🟢      |              |              |
| `admin.py`         |      🟢      |              |              |
| ORM/model queries  |      🟢      |      🟡      |              |
| `services.py`      |              | 🟢 Principal |              |
| `forms.py`         |              |      🟢      |              |
| `views.py`         |              | 🟢 Principal |      🟡      |
| `urls.py`          |              |      🟡      | 🟢 Principal |
| Templates          |              |              |      🟢      |
| Catálogo UI        |              |              |      🟢      |
| Filtros UI         |              |  🟡 backend  |      🟢      |
| Historial backend  |              |      🟢      |              |
| Historial UI       |              |              |      🟢      |
| `test_models.py`   |      🟢      |              |              |
| `test_services.py` |              |      🟢      |              |
| `test_views.py`    |              |      🟡      |      🟢      |
| Seguridad          |              |      🟢      |      🟡      |
| Documentación      |      🟡      |      🟡      |      🟢      |
| Integración final  |      🟢      |      🟢      |      🟢      |
