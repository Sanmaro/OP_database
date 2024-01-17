# CZECH LITERARY TRANSLATORS' GUILD DATABASE
### Video Demo: https://youtu.be/X_bcVuKZG1c
### Changelog:

**Released:** November 24, 2023 \
**Version:** 1.5 \
**Changes:**

* New users' avatars
* Improved translator's profile page
* New reset-password feature
* User-friendlier table for updating book info, now with the option to add books
* Several minor changes to links and templates
* Re-arranged app architecture 

### Description:
#### Summary

**Released:** November 14, 2023  
**Version:** 1.0  
**Written on Python ver.:** 3.12.0  
**Made by:** Vojtěch Ettler

**DISCLAIMER:** THIS IS A TEST PROJECT IMITATING A REAL-WORLD SOLUTION

Let me present to you a web application based on the **Flask** framework and **SQLite** database contatining several tables: `users`, `translators`, and `books`. As for the front-end, the site uses mostly **Bootstrap** styles and scripts. The database follows the paradigm
of other book servers such as Goodreads.com but focuses on literary translators, their bios and work (more on this in *Background info* section). Visitors can browse the database, find inspiration in five translated books randomly generated at each reload, and check what the translators have to say about themselves in their respective profiles. The translators can in turn log into their accounts and manage data related to their person.

The whole site is localised into the Czech language due to its specific purpose. However, the code "under the hood" is written in English.

#### Technical details

The meat of the app is found in the `app.py` file coded in the Python programming language. Thanks to **Flask**, it is turned into a server code rendering webpages to the client. Apart from Flask and its Session complement, the database relies on CS50 SQL module, Werkzeug security, as well as custom helper functions from `helpers.py`.

The functions in `app.py` serves different routes following users' actions. On entering the site, `login()` renders the `index.html` with the corresponding `layout.html` which are linked together through **Jinja** formatting. There visitors can search for a translator or book by typing their name or title in the search box. Also, via the same function using `POST` method, authorized users can log in and manage their account, bio, or translated books. Every user is entitled to alter only items consisting of their own work. Solely administrators (rights set to 1) see the whole database.

Other functions help user navigate across the web.

The templates are coded in `HTML` using the **Bootstrap 5.3** styles and JavaScripts, giving the site modern but sober look suitable for a webpage of a professional guild. Thanks to Jinja, only `layout.html` is a "whole" template with `<html>`, `<head>`, and `<body>` tags, while other templates are inserted into it by extending its "blocks".

The interactive tables are made with **DataTables** module compatible with Bootstrap.

Front-end modules are called by CDN links. All the necessary Python libraries are summarized in *requirements.txt*.


#### Possible improvements, design choices, and drawbacks

Since creating and fine-tuning a web application of such proportions is a long-term task going beyond the scope of a practice final project, there are several areas waiting to be improved.

* Changing layout of the search table so as translators' names appear only once with a list of their books shown next to them.
* Adding more user-friendly options to the login section, including "Remember me" check, "Forgotten password" feature, and more.
* Using real databases! For the time being, the app is powered by a mock database downloaded from **Goodreads.com**. In real-case scenario, it is intended to acquire the list with all the members of the Translators' guild, creating accounts for each of them, and populating `translators` table in the database (this might in fact attract more translators to become members!). Regarding the book database, it might be mutually beneficial to get together with the **Databazeknih.cz** or **CBDB.cz** servers that already own and administer extensive amount of related data. Both parties could become interlinked, the database showing ratings or guiding visitors to associated websites, while the book servers redirecting to translators' profiles. In any case, the co-operation with the Czech Literary Translators' Guild would be essential.

For the purposes of testing, it is possible to access the user section via `username`: **Sanmaro** and `password`: **Op01**.


#### Background info

The idea for this project came from my being a literary translator and a member of the Guild myself. The Guild depends on the efforts of the few most active players in the field, which is why it is in a dire need of a modern, interactive database for quite a long time.

This is an attempt to fulfill that need and show a prototype of how the database might look like. Literary translators are chronically underpaid despite doing a highly specialized and educated job, working under unstable conditions, and losing their footing oqing to progressing MT technologies. Putting their names and work on the Internet for everyone to see in one place might make their contributions a little bit more visible.

### <p style="text-align: center;"> Happy browsing. </p>


