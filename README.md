# TT — the Three Tree Tenets

This folder is the TT site: plain HTML and CSS pages, with no build step and nothing to install.

## See it on this computer

    py serve.py

Then open http://127.0.0.1:8080. An open page reloads by itself about a second after any file here is saved, so an edit shows at once. `serve.py` adds that reload while it serves and never writes it into the files. It listens on this computer only.

## Where it will live

The plan: the same files served from two places, this computer and an external host that stays up while this computer is off, each one the other's fallback. Small edits go live as they are made; a whole set of changes goes out as one push. The external host is not chosen yet, so the repository has no remote and nothing here is pushed anywhere.

## History

Every change is a git commit, so the site's history is its own record.

## Licence

The code (the page structure, stylesheets, scripts and `serve.py`) is licensed under the GNU Affero General Public License v3.0; see `LICENSE`. The writing (the words on the pages and in the posts) is licensed under Creative Commons Attribution-ShareAlike 4.0 International; see `LICENSES/CC-BY-SA-4.0.txt`.

In short: take anything, give credit, give back the same way.
