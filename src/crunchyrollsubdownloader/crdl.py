import requests
import json
from bs4 import BeautifulSoup
import youtube_dl
import argparse
from urllib.parse import urlparse


def calc_root_url(show_url):
    parsed_uri = urlparse(show_url)
    result = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
    return result


def fetch_url(flaresolverr, show_url):
    flaresolverr = flaresolverr + "/v1"
    r = requests.post(flaresolverr, json={
        "cmd": "request.get",
        "url": show_url,
        "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleW...",
        "maxTimeout": 60000
    }, headers={
        "Content-Type": "application/json"
    })
    html = r.json()["solution"]["response"]
    soup = BeautifulSoup(html, features="lxml")
    return soup


def soup_get_list_of_seasons(soup):
    return soup.find("ul", {"class": "list-of-seasons"})


def get_season_episodes_url(soup, show_url, season_name):
    seasons = soup_get_list_of_seasons(soup)
    season_a = seasons.find("a", {"title": season_name})
    season_ul = season_a.find_next()
    episodes = season_ul.find_all("a", {"class": "episode"})
    crunchyroll_url = calc_root_url(show_url)
    episodes_url = ["{}{}".format(crunchyroll_url, ep["href"])
                    for ep in episodes]
    return episodes_url


def get_all_episodes_url(soup, show_url):
    seasons = soup_get_list_of_seasons(soup)
    episodes = seasons.find_all("a", {"class": "episode"})
    crunchyroll_url = calc_root_url(show_url)
    episodes_url = ["{}{}".format(crunchyroll_url, ep["href"])
                    for ep in episodes]
    return episodes_url


def get_list_of_seasons(soup):
    seasons = soup_get_list_of_seasons(soup)
    seasons_list = seasons.find_all("a", {"class": "season-dropdown"})
    return [el["title"] for el in seasons_list]


def main():

    parser = argparse.ArgumentParser(
        add_help="Downloads a full season subtitles pack from Crunchyroll, with youtube-dl")
    parser.add_argument("-f", "--flaresolverr", help="Flaresolverr API URL. Default: http://localhost:8191",
                        type=str, default="http://localhost:8191")
    parser.add_argument('-v', "--verbose", help="Verbose mode",
                        action='store_const', default=False, const=True)

    subparsers = parser.add_subparsers(help="Subcommands", dest="command")

    # DL
    parser_dl = subparsers.add_parser(
        'dl', help="Directly download subtitles with a given season name and language")
    parser_dl.add_argument('show_url', help="Crunchyroll show URL", type=str)
    parser_dl.add_argument(
        "-s", '--season_name', help="Crunchyroll season name on the webpage", type=str)
    parser_dl.add_argument('lang', help="Crunchyroll language", type=str)

    # LANG
    parser_dl = subparsers.add_parser(
        'lang', help="Shows list of available subtitles for a given show and season name")
    parser_dl.add_argument('show_url', help="Crunchyroll show URL", type=str)
    parser_dl.add_argument(
        "-s", '--season_name', help="Crunchyroll season name on the webpage", type=str)

    # SEASONS
    parser_dl = subparsers.add_parser(
        'seasons', help="Shows list of seasons for a given show")
    parser_dl.add_argument('show_url', help="Crunchyroll show URL", type=str)

    args = parser.parse_args()

    if(args.command is None):
        print("No command supplied, aborting")
        print(parser.format_help())
        exit()

    soup = fetch_url(args.flaresolverr, args.show_url)

    if(args.command == "dl"):
        if(args.season_name is None):
            episodes = get_all_episodes_url(soup, args.show_url)
        else:
            episodes = get_season_episodes_url(
                soup, args.show_url, args.season_name)

        ytdl = youtube_dl.YoutubeDL(
            {"writesubtitles": True, "subtitleslangs": [args.lang], "skip_download": True, "quiet": not(args.verbose), "no_warnings": not(args.verbose)})
        for el in episodes:
            try:
                ytdl.download([el])
            except:
                print("Can't download episode subtitles from {}, skipping".format(el))

    elif(args.command == "seasons"):
        seasons = get_list_of_seasons(soup)
        print("List of available seasons to download:")
        print("---------------------------------------")
        for el in seasons:
            print(el)

    elif(args.command == "lang"):
        if(args.season_name is None):
            episodes = get_all_episodes_url(soup, args.show_url)
        else:
            episodes = get_season_episodes_url(
                soup, args.show_url, args.season_name)

        ytdl = youtube_dl.YoutubeDL(
            {"writesubtitles": True, "quiet": not(args.verbose), "no_warnings": not(args.verbose)})
        if(len(episodes) == 0):
            print("No episode found for this show/season")
            exit()
        # Checking last item in the list, cause the first item is the most recent one and can be paywalled
        meta = ytdl.extract_info(episodes[-1], False)
        languages = meta["subtitles"]
        print("List of available languages to download:")
        print("---------------------------------------")
        for el in languages.keys():
            print(el)


if __name__ == "__main__":
    main()
