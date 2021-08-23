# Crunchyroll Subtitles Downloader

This tool helps you download all of a season's subtitles list, in your choosen language.

## Installation

Install it from Pypi or clone the repo and install the requirements.

```bash
pip install crunchyrollsubdownloader
```

### FlareSolverr

[FlareSolverr](https://github.com/FlareSolverr/FlareSolverr) is a tool to bypass Cloudflare protection. Crunchyroll uses it and this tool requires FlareSolverr to work.

You can set it up with a simple Docker command for instance:

```bash
docker run --rm -p 8191:8191 -e LOG_LEVEL=info ghcr.io/flaresolverr/flaresolverr:latest
```

This will run the Docker container and clean it when you CTRL-C. FlareSolverr is exposed on the `8191` port.

By default, this tool will try to reach it at `http://localhost:8191`. But if you need to specify a custom URL, use the `--flaresolverr` argument right before the commands calls (`dl`, `lang`...)

## Usage

```
usage: crunchyrollsubdownloader [-h] [-f FLARESOLVERR] [-v] {dl,lang,seasons,interactive} ...

positional arguments:
  {dl,lang,seasons,interactive}
                        Subcommands
    dl                  Directly download subtitles with a given season name and language
    lang                Shows list of available subtitles for a given show and season name
    seasons             Shows list of seasons for a given show
    interactive         Interactive selection of season

optional arguments:
  -h, --help            show this help message and exit
  -f FLARESOLVERR, --flaresolverr FLARESOLVERR
                        Flaresolverr API URL. Default: http://localhost:8191
  -v, --verbose         Verbose mode
```

### Interactive

```
usage: crunchyrollsubdownloader interactive [-h] show_url

positional arguments:
  show_url    Crunchyroll show URL

optional arguments:
  -h, --help  show this help message and exit
```

Takes the show URL as parameter and guides you though a season's subs download.

```bash
crunchyrollsubdownloader interactive https://www.crunchyroll.com/tokyo-revengers
```

### Download a season subtitles

```
usage: crunchyrollsubdownloader dl [-h] [-s SEASON_NAME] show_url lang

positional arguments:
  show_url              Crunchyroll show URL
  lang                  Crunchyroll language

optional arguments:
  -h, --help            show this help message and exit
  -s SEASON_NAME, --season_name SEASON_NAME
                        Crunchyroll season name on the webpage
```

- `show_url` is the simple show URL, where the full list of episodes is displayed
- `lang` is a language code found with the language command explained below (such as `enUS`, `frFR`...)
- `season_name` is the name in the season dropdown (optional, will download all the page's episodes if not provided). Useful when the show is single season and there are no dropdown
  ![Red rectangle to show how to choose the season name](assets/season_name.png)

```bash
crunchyrollsubdownloader dl -s "Tokyo Revengers" https://www.crunchyroll.com/tokyo-revengers enUS # Will download the season "Tokyo Revengers"
crunchyrollsubdownloader dl https://www.crunchyroll.com/fena-pirate-princess enUS # Will download the whole page
```

### Display list of languages for a given season

```
usage: crunchyrollsubdownloader lang [-h] [-s SEASON_NAME] show_url

positional arguments:
  show_url              Crunchyroll show URL

optional arguments:
  -h, --help            show this help message and exit
  -s SEASON_NAME, --season_name SEASON_NAME
                        Crunchyroll season name on the webpage
```

Arguments are the same as above.

```bash
crunchyrollsubdownloader lang -s "Tokyo Revengers" https://www.crunchyroll.com/tokyo-revengers # Will show languages for the season "Tokyo Revengers"
crunchyrollsubdownloader lang https://www.crunchyroll.com/fena-pirate-princess # Will show languages for the whole page
```

### Display list of seasons for a given show

```
usage: crunchyrollsubdownloader seasons [-h] show_url

positional arguments:
  show_url    Crunchyroll show URL

optional arguments:
  -h, --help  show this help message and exit
```

```bash
crunchyrollsubdownloader seasons https://www.crunchyroll.com/tokyo-revengers # Will show seasons of this show
```
