# CommandTimeline

CommandTimeline is designed for pentesters to log all commands run on your Linux testing platform. While you can use any version of Linux with CommandTimeline, the preferred platform is Kali Linux. All development and testing is done against Kali Linux.

### Use Case

Two use cases exist for the tool. First, a single tester can log all their commands for archiving and/or providing to the customer. Second, teams of pentesters can merge their command histories together, then run the tool against the combined history file to see all commands in sorted, timeline order. The multi-team member environment was the original design of the tool.

## Commands to setup logging

* File to edit: .bashrc

  * Edit in place:

    * `HISTSIZE=3000`

    * `HISTFILESIZE=5000`

  * Append to file:

    * `export HISTTIMEFORMAT="%F %T "`

    * `export HISTIGNORE="histor*:clear:exit"`

    * `export PROMPT_COMMAND='history -a'`

* File to edit: .bash_logout

  * Append to file:

    * `history -w`

* Run from Terminal

  * `export HISTTIMEFORMAT="%F %T "`

  * `history -w`

  * `reboot`

  * `cat /dev/null > ~/.bash_history && history -c && exit`

## How to run CommandTimeline

The basic gist of the tool is simple. 

1. Ensure commands to setup logging have occurred

1. Update command-timeline.py file with the path to the combined history file (line #18)

1. Run: `python3 command-timeline.py`

## Storing CommandTimeline archive in database

(TBD)

## Obfuscating passwords in CommandTimeline archive

(TBD)

