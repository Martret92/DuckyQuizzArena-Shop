# Ducky Quiz Arenas — Equipo 4 `shop`

Repositorio de trabajo del **Equipo 4** para el proyecto académico **Ducky Quiz Arenas**, desarrollado con Django dentro del certificado **IFCD0112**.

## Responsabilidad del Equipo 4

El Equipo 4 desarrolla la aplicación Django:

```text
shop
```

Su responsabilidad principal es gestionar la **tienda y la economía basada en Ducky Coins**.

El alcance incluye principalmente:

* `Wallet`
* `ShopItem`
* `Transaction`
* historial económico
* catálogo de tienda
* compras
* integración con el inventario del Ducky
* validación de saldo
* operaciones económicas atómicas
* Django Admin
* consultas ORM
* tests

## Dependencias principales

La aplicación `shop` depende especialmente de:

### `accounts`

Proporciona el usuario y su perfil.

El saldo oficial de Ducky Coins se encuentra en:

```python
user.profile.ducky_coins
```

`shop.Wallet` no debe mantener un segundo saldo independiente.

### `duckies`

Proporcionará principalmente:

* `Ducky`
* `Item`
* `InventoryItem`

La tienda no duplicará los objetos de `duckies`.

Conceptualmente:

```text
duckies.Item
     │
     ▼
shop.ShopItem
     │
     ▼
Compra
     │
     ▼
duckies.InventoryItem
     │
     ▼
Ducky
```

## Modelos previstos de `shop`

### `Wallet`

Relación económica 1:1 con el usuario.

```text
User 1 ───── 1 Wallet
```

La Wallet sirve como raíz del historial económico, pero el saldo oficial permanece en `Profile.ducky_coins`.

### `ShopItem`

Representa las condiciones comerciales de un `duckies.Item`.

```text
Item 1 ───── 0..1 ShopItem
```

Contendrá información como precio, disponibilidad y si el producto está destacado, sin duplicar nombre, rareza, imagen o tipo del Item.

### `Transaction`

Representa movimientos de Ducky Coins.

Tipos iniciales previstos:

```text
REWARD
PURCHASE
ADJUSTMENT
```

Las transacciones positivas representan entradas de monedas y las negativas, salidas.

`Transaction` no gestiona XP.

## Organización del equipo

### Miembro 1 — Jaime

Responsable principalmente de:

* `models.py`
* `Wallet`
* `ShopItem`
* `Transaction`
* relaciones y restricciones
* migraciones
* Django Admin
* consultas ORM
* diseño del historial económico

### Miembro 2 — Henry

Responsable principalmente de:

* formularios
* vistas
* comprobación de saldo
* motor de compra
* `purchase_item()`
* integración con inventario
* seguridad
* transacciones atómicas

### Miembro 3 — Fernando

Responsable principalmente de:

* URLs
* templates
* catálogo visual
* ficha de producto
* historial
* mensajes
* filtros
* tests
* documentación

Los tres integrantes deberán comprender el funcionamiento global de `shop`.

## Flujo Git

No se trabaja directamente sobre `main`.

La estructura de ramas del Equipo 4 es:

```text
main
  │
  └── team/shop
         │
         ├── feature/wallet
         ├── feature/shop-items
         ├── feature/transactions
         ├── feature/shop-catalog
         ├── feature/purchase
         ├── feature/history
         └── feature/shop-tests
```

También podrán utilizarse ramas específicas como:

```text
docs/...
fix/...
```

Flujo habitual:

```text
team/shop
    ↓
rama de trabajo
    ↓
commits
    ↓
push
    ↓
Pull Request
    ↓
revisión
    ↓
team/shop
```

Las ramas de trabajo se eliminan después de integrarse cuando ya no son necesarias.

## Convención de commits

Usaremos mensajes breves y descriptivos, por ejemplo:

```text
feat: añadir modelo Wallet
feat: relacionar ShopItem con duckies Item
test: añadir tests del modelo Wallet
fix: impedir compra con saldo insuficiente
docs: documentar flujo de ramas
refactor: simplificar lógica económica
```

## Plan de trabajo

Seguiremos como referencia los sprints definidos para el Equipo 4.

### Sprint 0 — Preparación del equipo

Sprint organizativo añadido por el Equipo 4:

* preparar repositorio
* configurar Git
* definir ramas
* comprobar entorno Django
* documentar el proyecto

### Sprint 1 — Economía

* Wallet
* acceso a la información económica
* visualización del saldo

### Sprint 2 — Tienda

* ShopItem
* catálogo
* interfaz de tienda

### Sprint 3 — Compra

* Transaction
* `purchase_item()`
* confirmación de compra

### Sprint 4 — Integración

Integración con:

```text
shop
 ↓
Item
 ↓
InventoryItem
 ↓
Ducky
```

### Sprint 5 — Calidad

* seguridad
* atomicidad
* concurrencia
* filtros
* historial
* tests
* documentación

## Instalación local

Crear y activar un entorno virtual de Python.

Después instalar las dependencias:

```bash
pip install -r requirements.txt
```
### Configuración de la SECRET_KEY

La clave secreta de Django no se almacena en el repositorio.

Antes de ejecutar Django, define la variable de entorno `DJANGO_SECRET_KEY`.

En PowerShell:

```powershell
$env:DJANGO_SECRET_KEY="tu-clave-local"
```
Puedes generar una clave nueva desde Django con:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
La variable debe estar disponible en la terminal desde la que ejecutes `manage.py`.

Aplicar migraciones:

```bash
python manage.py migrate
```

Comprobar el proyecto:

```bash
python manage.py check
```

Ejecutar el servidor:

```bash
python manage.py runserver
```

## Decisiones confirmadas relevantes

* `accounts.Profile.ducky_coins` es la única fuente oficial del saldo de Ducky Coins.
* `Wallet` existirá, pero no almacenará un segundo saldo independiente.
* Durante un registro normal deberán existir `User`, `Profile`, `Ducky` y `Wallet`.
* La tienda no está restringida únicamente al rol `STUDENT`.
* Los objetos vendidos pertenecen a `duckies.Item`.
* Una compra añade un `InventoryItem` pero no equipa automáticamente el objeto.
* `shop.Transaction` registra únicamente movimientos de Ducky Coins.
* `shop` no gestiona actualmente la XP.

## Decisiones pendientes de confirmación

Algunas decisiones transversales siguen pendientes de confirmación del profesor y no se consideran contratos cerrados en este repositorio.

Entre ellas:

* atomicidad global de la creación de `User + Profile + Ducky + Wallet` durante el registro;
* funcionamiento global de las recompensas de XP;
* responsabilidad final sobre la concesión de XP.

Estas decisiones se coordinan fuera de `shop` antes de modificar contratos compartidos.

## Estado actual

Proyecto en fase inicial de desarrollo.

El repositorio parte del código base proporcionado por el profesor y el Equipo 4 desarrollará progresivamente la aplicación `shop`.
