# 📒 PiNote (v2.6.1)

[![Release](https://img.shields.io/badge/Release-v2.6.1-blue.svg)](https://github.com/frankiio4569/PiNote)
[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](LICENSE)
[![No AI Training](https://img.shields.io/badge/No_AI-Training-red)](NO-AI-TRAINING.md)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)](docker-compose.yml)
[![Built with Flask](https://img.shields.io/badge/Built%20with-Flask-000000.svg?logo=flask&logoColor=white)](app.py)

**PiNote** è un'applicazione web per prendere appunti, progettata per essere **self-hosted**, sicura e facile da usare. Ideale per chi vuole mantenere il controllo sui propri dati senza rinunciare a un'interfaccia moderna.

---

## ✨ Novità della v2.6.1

* ⚠️ **Migliorato avviso No-JS:** Introdotto un sistema di rilevamento dettagliato per i browser con JavaScript disabilitato. Ora l'utente viene informato specificamente su quali funzioni sono limitate (Editor, Temi, Alert) invece di ricevere un errore generico.
* 📝 **Nuovo Editor Markdown (dalla v2.6.0):** Introdotto **EasyMDE**. Scrittura con formattazione visuale (grassetti, liste, tabelle), anteprima "Side-by-Side" e conteggio parole.
* 🎨 **Restyling Grafico:** Interfaccia ripulita e ottimizzata per la modalità scura.

## 🚀 Funzionalità Principali

* 🔐 **Multi-utente & Sicuro:** Sistema di login/registrazione completo. Ogni utente ha il suo database privato e isolato.
* 🛡️ **Note Protette:** Hai informazioni sensibili? Puoi bloccare singole note con una **password dedicata** (crittografata).
* 📝 **Formattazione Ricca:** Scrivi usando Markdown o la barra degli strumenti intuitiva.
* 🕰️ **Cronologia Versioni:** Hai sbagliato a modificare? PiNote salva automaticamente le versioni precedenti. Puoi visualizzarle e recuperare vecchi contenuti in qualsiasi momento.
* 🗑️ **Cestino Sicuro:** Le note cancellate finiscono in un'area di recupero prima dell'eliminazione definitiva.
* 🌗 **Dark Mode:** Supporto nativo per tema Chiaro, Scuro o Automatico (basato sul sistema operativo).
* 🐳 **Docker Ready:** Pronto per essere distribuito in pochi secondi su qualsiasi server o NAS.

---

## 🛠️ Installazione Rapida

Il modo più semplice per avviare PiNote è utilizzare **Docker Compose**.

### Prerequisiti
* Git
* Docker & Docker Compose

### Passaggi
1.  **Clona il repository:**
    ```bash
    git clone [https://github.com/frankiio4569/PiNote.git](https://github.com/frankiio4569/PiNote.git)
    cd PiNote
    ```

2.  **Avvia l'applicazione:**
    ```bash
    docker compose up -d --build
    ```

3.  **Finito!**
    Apri il tuo browser e vai su: **http://localhost:5001**

---

## ⚙️ Configurazione Avanzata
Puoi modificare il file `docker-compose.yml` per personalizzare l'installazione:

* **Porta:** Cambia `"5001:5001"` se vuoi usare una porta diversa (es. `"8080:5001"`).
* **Volume:** I dati vengono salvati in `./pinote_data`. Assicurati di fare il backup di questa cartella per non perdere le tue note.
* **Secret Key:** Nel file `docker-compose.yml`, cambia la variabile `SECRET_KEY` con una stringa casuale per maggiore sicurezza in produzione.

---

## 👨‍💻 Nota dell'Autore
> *Ci tengo a specificare che tutto questo progetto è a scopo personale e didattico. Non sono un professionista del settore, ma mi ha sempre divertito "mettere le mani in pasta" e imparare facendo.*
>
> *Continuerò ad aggiornare, sperimentare e migliorare PiNote nel tempo libero.*
>
> — **Franki (F.P.F.)**

---

## 📄 Licenza e Diritti

Copyright **© 2026 PiNote Franki (F.P.F.)**.

Questo progetto è rilasciato sotto licenza **CC BY-NC-SA 4.0** (Attribuzione - Non commerciale - Condividi allo stesso modo).

* ✅ **Puoi:** Scaricare, usare, modificare e condividere il codice gratuitamente.
* ❌ **Non puoi:** Usare questo software per scopi commerciali o venderlo.
* ⚠️ **Condivisione:** Se modifichi il codice, devi rilasciarlo con la stessa licenza.

### ⛔ NO AI TRAINING
In conformità con la Direttiva UE 2019/790, l'autore **VIETA ESPLICITAMENTE** l'uso di questo codice e dei dati contenuti per l'addestramento di sistemi di Intelligenza Artificiale (LLM, Generative AI, ecc.).
Per dettagli, vedi il file [NO-AI-TRAINING.md](NO-AI-TRAINING.md).

[Leggi la licenza completa](LICENSE)
