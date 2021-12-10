# adventofcode-2021

My attempt at 2021's Advent of Code.

## Development

Puzzle inputs differ by user. For this reason, you can't get your data with an unauthenticated request. To authenicate
your requests, you must export your session token as an environment variable, or add it to `~/.config/aocd/token`.

```shell
// EITHER
export AOC_SESSION=<AOC_SESSION_TOKEN>
// OR
echo <AOC_SESSION_TOKEN> > ~/.config/aocd/token
```

Setup your environment and dependencies with pipenv.

```shell
make install
make test
```
