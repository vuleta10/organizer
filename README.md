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

Svi testovi odjednom:

```bash
pytest
```

### Unit testovi

Testiraju servisni sloj sa mokovanim repozitorijumima, ne zahtevaju bazu:

```bash
pytest tests/unit
```

### Integracioni testovi

Testiraju API preko pravih HTTP zahteva i pišu u pravu PostgreSQL bazu, pa prvo treba pokrenuti bazu:

```bash
docker compose up -d db
```

Zatim, pošto se testovi pokreću sa host mašine (van kontejnera), treba podesiti env varijable da gađaju bazu preko host porta (`55432`, ne `db`, jer to ime važi samo unutar Docker mreže):

```bash
# Windows PowerShell
$env:POSTGRES_HOST="localhost"
$env:POSTGRES_PORT="55432"
$env:POSTGRES_USER="postgres"
$env:POSTGRES_PASSWORD="postgres"
$env:POSTGRES_DB="organizer_db"

pytest tests/integration
```

```bash
# Linux / macOS
export POSTGRES_HOST=localhost
export POSTGRES_PORT=55432
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=postgres
export POSTGRES_DB=organizer_db

pytest tests/integration
```

Integracioni testovi koriste fiksan skup test korisnika (`utest1`–`utest8`). Prvi test koji se pokreće (`test_00_setup.py`) briše te korisnike i njihove taskove iz baze ako postoje od ranijeg pokretanja, pa ih ponovo upisuje - tako da je paket testova moguće pokretati više puta zaredom nad istom bazom bez ručnog resetovanja.

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
