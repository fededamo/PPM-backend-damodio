# Progetto PPM 2026 - Event Management System

**Studente:** Federico D'Amodio  
**Project type:** Full-Stack Web Application (traccia "Event Management System")  
**Framework:** Django  

Progetto per l'esame di Progettazione e Produzione Multimediale. 
È un'applicazione web che permette di gestire eventi e relative iscrizioni.

## Funzionalità principali
- **Due tipi di utenti**: `Organizer` (crea e gestisce eventi) e `Attendee` (esplora e si iscrive agli eventi).
- **Gestione Eventi**: Operazioni CRUD (creazione, lettura, modifica, eliminazione) protette in base all'autore.
- **Iscrizioni**: Gli utenti base possono iscriversi e disiscriversi dagli eventi.
- **Locandine**: Caricamento e visualizzazione delle immagini degli eventi (tramite la libreria `Pillow`).

## Struttura
- `users/`: app per la gestione degli utenti e dei ruoli (tramite un CustomUser).
- `backend/`: app principale con la logica per eventi, categorie, location e iscrizioni.
- `templates/`: file HTML per l'interfaccia.

## Account Demo e Database
Il progetto include un database SQLite (`db.sqlite3`) già popolato con dati di prova, non è necessario lanciare script aggiuntivi.

Credenziali per testare il sito:
- **Admin (Superuser):** username: `admin` / password: `admin`
- **Organizer (Crea eventi):** username: `org_demo` / password: `password123`
- **Attendee (Utente base):** username: `att_demo` / password: `password123`

## Ruoli nel dettaglio
- **Organizer:** Può creare nuovi eventi, ma può modificare o eliminare **solo** i propri. Può vedere chi è iscritto ai suoi eventi. Non può iscriversi agli eventi.
- **Attendee:** Può vedere tutti gli eventi pubblici e iscriversi o disiscriversi. Non ha permessi per creare o modificare gli eventi.

## Come testare in locale
Per verificare che tutto funzioni:
1. Fai login come **Organizer** (`org_demo`).
2. Crea un nuovo evento dalla dashboard, caricando anche una locandina.
3. Prova a modificare l'evento appena creato per vedere che i permessi sono corretti.
4. Fai logout.
5. Fai login come **Attendee** (`att_demo`).
6. Cerca l'evento creato prima e iscriviti.
7. Clicca di nuovo sul bottone rosso per annullare l'iscrizione.
8. (Opzionale) Se da Attendee provi ad accedere all'URL `/events/create/`, il sistema ti bloccherà mostrando un messaggio di errore.

## Installazione Locale
Per avviare il progetto sul tuo computer:
1. Clona la repository.
2. Crea un virtual environment e attivalo:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Su Windows: venv\Scripts\activate
   ```
3. Installa le librerie necessarie:
   ```bash
   pip install -r requirements.txt
   ```
4. Esegui le migrazioni del database:
   ```bash
   python manage.py migrate
   ```
5. (Opzionale) Se vuoi ricreare i dati demo, puoi usare il comando:
   ```bash
   python manage.py populate_db
   ```
6. Avvia il server:
   ```bash
   python manage.py runserver
   ```
7. Apri il browser all'indirizzo `http://127.0.0.1:8000/`.

## Link al sito live
*Link al deploy:* https://ppm-backend-damodio.onrender.com
