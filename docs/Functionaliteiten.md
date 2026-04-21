# Functionele Eisen

## 1. Gebruikersbeheer (Authenticatie & Profiel)

| ID  | Eis                                                                                            |
| --- | ---------------------------------------------------------------------------------------------- |
| F1  | Nieuwe gebruiker kan zich registreren met gebruikersnaam, e-mailadres en wachtwoord            |
| F2  | Wachtwoorden worden veilig gehasht (geen plaintext opslag)                                     |
| F3  | Bestaande gebruiker kan inloggen met gebruikersnaam/e-mail + wachtwoord                        |
| F4  | Alleen ingelogde gebruikers hebben toegang tot het dashboard en transacties                    |
| F5  | Gebruiker kan uitloggen                                                                        |
| F6  | Gebruiker kan zijn/haar profiel bekijken (gebruikersnaam, e-mail)                              |
| F7  | Gebruiker kan wachtwoord wijzigen (met verificatie oud wachtwoord)                             |
| F8  | Gebruiker kan account verwijderen (verwijdert ook alle bijbehorende transacties & categorieën) |

---

## 2. Categorieën Beheren

| ID  | Eis                                                                                                              |
| --- | ---------------------------------------------------------------------------------------------------------------- |
| F9  | Nieuwe gebruiker krijgt standaardcategorieën (bijv. "Boodschappen", "Huur", "Salaris", "Vervoer", "Eten buiten") |
| F10 | Gebruiker kan een nieuwe categorie aanmaken (naam, type = inkomst/uitgave)                                       |
| F11 | Gebruiker kan een bestaande categorie bewerken (naam wijzigen)                                                   |
| F12 | Gebruiker kan een categorie verwijderen (alleen als er geen transacties meer aan hangen, anders foutmelding)     |
| F13 | Categorieën zijn gebruikerspecifiek (gebruiker A ziet niet de categorieën van gebruiker B)                       |

---

## 3. Transacties Bijhouden (CRUD)

| ID  | Eis                                                                                                                            |
| --- | ------------------------------------------------------------------------------------------------------------------------------ |
| F14 | Gebruiker kan een transactie toevoegen met: bedrag (positief getal), datum, beschrijving (optioneel), categorie (uit dropdown) |
| F15 | Inkomsten (positief effect op saldo) en uitgaven (negatief effect) worden onderscheiden via categorietype                      |
| F16 | Gebruiker kan een bestaande transactie bewerken (alle velden)                                                                  |
| F17 | Gebruiker kan een transactie verwijderen (met bevestigingsvraag)                                                               |
| F18 | Gebruiker kan een transactie bekijken in detail (bijv. popup of aparte pagina)                                                 |
| F19 | Datumkiezer wordt gebruikt voor eenvoudige datumselectie (geen handmatige foutgevoelige invoer)                                |
| F20 | Bedrag mag geen negatief getal zijn (validatie)                                                                                |
| F21 | Beschrijving heeft een maximumlengte (bijv. 200 karakters)                                                                     |

---

## 4. Dashboard & Overzichten

| ID  | Eis                                                                                  |
| --- | ------------------------------------------------------------------------------------ |
| F22 | Dashboard toont huidig totaalsaldo (som alle inkomsten minus som alle uitgaven)      |
| F23 | Dashboard toont saldo van huidige maand (inkomsten en uitgaven apart)                |
| F24 | Dashboard toont laatste 10 transacties (datum, beschrijving, categorie, bedrag)      |
| F25 | Dashboard toont taartdiagram van uitgaven per categorie (huidige maand)              |
| F26 | Dashboard toont staafdiagram van inkomsten vs uitgaven per maand (laatste 6 maanden) |
| F27 | Grafieken zijn interactief (hover voor waarden)                                      |
| F28 | Dashboard heeft een "refresh" of werkt real-time na toevoegen/bewerken               |

---

## 5. Filteren & Zoeken

| ID  | Eis                                                                             |
| --- | ------------------------------------------------------------------------------- |
| F29 | Gebruiker kan transacties filteren op datumrange (van - tot)                    |
| F30 | Gebruiker kan transacties filteren op categorie (één of meerdere)               |
| F31 | Gebruiker kan transacties filteren op type (alleen inkomsten / alleen uitgaven) |
| F32 | Gebruiker kan zoeken op trefwoord in beschrijving                               |
| F33 | Filters combineren (bijv. "uitgaven in maand mei, categorie Boodschappen")      |
| F34 | Huidige filters zijn zichtbaar en kunnen één voor één worden verwijderd         |
| F35 | Resultaten kunnen worden gesorteerd op datum (aflopend/oplopend) of bedrag      |

---

## 6. Export Functionaliteit

| ID  | Eis                                                                                |
| --- | ---------------------------------------------------------------------------------- |
| F36 | Gebruiker kan huidige gefilterde transactielijst exporteren naar CSV               |
| F37 | Gebruiker kan alle transacties van een geselecteerde maand exporteren naar CSV     |
| F38 | CSV bevat kolommen: datum, beschrijving, categorie, type (inkomst/uitgave), bedrag |
| F39 | (Optioneel) Gebruiker kan dashboard als PDF exporteren (grafieken + saldo)         |

---

## 7. Data Validatie & Foutafhandeling

| ID  | Eis                                                                                             |
| --- | ----------------------------------------------------------------------------------------------- |
| F40 | Geen dubbele gebruikersnamen of e-mailadressen bij registratie                                  |
| F41 | Bij lege verplichte velden toont systeem duidelijke foutmelding (geen crash)                    |
| F42 | Bij verwijderen van categorie met transacties: blokkeer + toon "Verwijder eerst de transacties" |
| F43 | Bedrag mag maximaal 2 decimalen hebben (€-notatie)                                              |
| F44 | Datum mag niet in de toekomst liggen (waarschuwing, maar toegestaan als gebruiker wil)          |
| F45 | Sessie verloopt na X minuten inactiviteit (bijv. 30 minuten)                                    |

---

## 8. Front-end & Gebruikerservaring

| ID  | Eis                                                                                                  |
| --- | ---------------------------------------------------------------------------------------------------- |
| F46 | Responsive design (werkt op mobiel, tablet en desktop)                                               |
| F47 | Duidelijke navigatie (navbar met links naar Dashboard, Transacties, Categorieën, Profiel, Uitloggen) |
| F48 | Successmeldingen bij toevoegen/bewerken/verwijderen (toast of banner)                                |
| F49 | Foutmeldingen in rood, successmeldingen in groen                                                     |
| F50 | Bevestigingsdialoog bij verwijderen van transactie of categorie                                      |
| F51 | Datumkiezer heeft formaat DD-MM-YYYY (lokaal)                                                        |
| F52 | Bedrag wordt getoond met euroteken (€) en puntjes voor duizendtallen (bijv. € 1.234,56)              |
| F53 | Laadtijden onder 2 seconden voor dashboard (bij <1000 transacties)                                   |

---

## 9. Database & Prestaties (Niet-functioneel)

| ID  | Eis                                                                                              |
| --- | ------------------------------------------------------------------------------------------------ |
| NF1 | Database gebruikt indices op user_id, date, category_id voor snelle queries                      |
| NF2 | Bij meer dan 10.000 transacties blijft dashboard responsief (paginering op transactielijst)      |
| NF3 | Databaseback-up kan handmatig worden gemaakt via een adminpagina (of CLI-script)                 |
| NF4 | SQLite is standaard, maar migratie naar PostgreSQL moet mogelijk zijn (via environment variable) |

---

## 10. Beveiliging (Niet-functioneel)

| ID  | Eis                                                                                               |
| --- | ------------------------------------------------------------------------------------------------- |
| NF5 | Alle gebruikersinvoer wordt gesanitiseerd tegen XSS (bijv. via Flask escape of template escaping) |
| NF6 | CSRF-bescherming op alle POST-formulieren (bijv. Flask-WTF)                                       |
| NF7 | Wachtwoord heeft minimum eisen: min. 8 karakters, 1 cijfer, 1 hoofdletter (optioneel)             |
| NF8 | Geen SQL-injectie (gebruik ORM of parameterized queries)                                          |
| NF9 | Debug-modus uit in productie (geen stack traces naar gebruiker)                                   |

---

## Prioritering (MoSCoW)

| Prioriteit                                      | Eisen                                                                     |
| ----------------------------------------------- | ------------------------------------------------------------------------- |
| **Must have** (essentieel voor MVP)             | F1–F5, F9–F10, F14–F17, F22–F24, F29, F40–F41, F46–F47                    |
| **Should have** (belangrijk, maar niet kritiek) | F6–F7, F11–F13, F25–F26, F30–F31, F36, F42–F43, NF1, NF5–NF6              |
| **Could have** (nice to have)                   | F8, F18, F27–F28, F32–F35, F37–F39, F44–F45, F48–F53, NF2–NF4             |
| **Won't have** (niet in v1)                     | Mobiele app, budgetten, terugkerende transacties, notificaties per e-mail |
