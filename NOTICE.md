# Third-party material

purrimer-build ships and generates files that include work by others.

| Material | Where | Licence |
| --- | --- | --- |
| Octicons 19.15.0, GitHub Inc. | `src/purrimer_build/data/octicons.json`, every generated icon file | MIT, see `src/purrimer_build/data/OCTICONS_LICENSE` |
| Mona Sans and Mona Sans Mono, GitHub Inc. | `tokens/fonts`, generated `fonts/` folders | SIL Open Font License 1.1 |
| Quicksand, Andrew Paglinawan | `tokens/fonts`, generated `fonts/` folders | SIL Open Font License 1.1 |
| Playwrite GB S, TypeTogether | `tokens/fonts`, generated `fonts/` folders | SIL Open Font License 1.1 |
| JetBrains Mono, JetBrains | `tokens/fonts`, generated `fonts/` folders | SIL Open Font License 1.1 |

The native targets use static TTF instances that `purrimer build` cuts from the variable fonts. Mona Sans reserves
the font name "Mona" and Quicksand reserves "Quicksand", and the OFL does not let a modified font keep a reserved name.
Before you ship an app with those two families, swap the generated instances for the static files the authors publish
(github.com/github/mona-sans releases, github.com/andrew-paglinawan/QuicksandFamily). Ship each family's `OFL.txt`
with the fonts in every case.
