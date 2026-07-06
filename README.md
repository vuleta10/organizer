# Organizer API

REST API za organizaciju zadataka (task organizer), napravljen u Flask-u, sa Flask-RESTX (Swagger/OpenAPI dokumentacija), SQLAlchemy i PostgreSQL bazom, po slojevitoj arhitekturi Repository / Service / Routes.

## Pokretanje sa Dockerom (preporučeno)

Potrebno: [Docker](https://www.docker.com/) i Docker Compose.

```bash
git clone <link-ka-repo>
cd organizer
cp .env.example .env
docker compose up --build
```

API je dostupan na `http://localhost:5000`, a Swagger dokumentacija na `http://localhost:5000/swagger.html`.

PostgreSQL je izložen na host portu `55432` (mapiran na kontejnerski `5432`) ako želiš da se povežeš nekim database klijentom. Sam API komunicira sa `db` servisom direktno preko interne Docker mreže.

Za gašenje:

```bash
docker compose down
```

## Pokretanje lokalno bez Dockera

Potrebno: Python 3.12+, pokrenut PostgreSQL.

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Linux / macOS

pip install -r requirements.txt
```

Napravi `.env` fajl (po uzoru na `.env.example`) sa `POSTGRES_HOST` podešenim na lokalnu Postgres instancu (npr. `localhost`) i odgovarajućim portom/kredencijalima.

```bash
python -m app.app
```

## Pokretanje testova

```bash
pytest
```

Unit testovi testiraju servisni sloj sa mokovanim repozitorijumima; integracioni testovi testiraju API preko HTTP zahteva i zahtevaju dostupnu PostgreSQL bazu (ista `.env` konfiguracija kao gore).

## Struktura projekta

```
app/
  models/         SQLAlchemy modeli (User, Task)
  repositories/    Sloj za pristup podacima
  services/        Sloj sa poslovnom logikom
  routes/          Flask-RESTX namespace-ovi / HTTP sloj
  database.py      Podešavanje engine-a i sesije
  swagger.py       Flask-RESTX Api instanca
  app.py           Ulazna tačka aplikacije
tests/
  unit/            Testovi servisnog sloja sa mokovanim repozitorijumima
  integration/      Testovi API-ja nad pravom bazom
```

## Pregled API-ja

- `POST /users/register` - registracija novog korisnika
- `POST /users/login` - prijava
- `PUT /users/change-password` - promena lozinke
- `POST /tasks` - kreiranje zadatka
- `GET /tasks/user/<user_id>` - lista zadataka korisnika
- `GET /tasks/user/<user_id>/<date>` - lista zadataka korisnika za dati datum (`YYYY-MM-DD`)
- `PUT /tasks/<task_id>` - izmena zadatka
- `DELETE /tasks/<task_id>` - brisanje zadatka
