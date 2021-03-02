import re
from PrismParser.Prism import *

# $ set | grep '^[A-Z][^[:space:]]*=' | cut -d= -f1 | tr '\n' '|'
# + LC_ALL, RANDOM, REPLY, SECONDS.
# + make sure PS1..4 are here as they are not always set,
# - some useless things.
envVars = r"\b(?:BASH|BASHOPTS|BASH_ALIASES|BASH_ARGC|BASH_ARGV|BASH_CMDS|BASH_COMPLETION_COMPAT_DIR|BASH_LINENO|BASH_REMATCH|BASH_SOURCE|BASH_VERSINFO|BASH_VERSION|COLORTERM|COLUMNS|COMP_WORDBREAKS|DBUS_SESSION_BUS_ADDRESS|DEFAULTS_PATH|DESKTOP_SESSION|DIRSTACK|DISPLAY|EUID|GDMSESSION|GDM_LANG|GNOME_KEYRING_CONTROL|GNOME_KEYRING_PID|GPG_AGENT_INFO|GROUPS|HISTCONTROL|HISTFILE|HISTFILESIZE|HISTSIZE|HOME|HOSTNAME|HOSTTYPE|IFS|INSTANCE|JOB|LANG|LANGUAGE|LC_ADDRESS|LC_ALL|LC_IDENTIFICATION|LC_MEASUREMENT|LC_MONETARY|LC_NAME|LC_NUMERIC|LC_PAPER|LC_TELEPHONE|LC_TIME|LESSCLOSE|LESSOPEN|LINES|LOGNAME|LS_COLORS|MACHTYPE|MAILCHECK|MANDATORY_PATH|NO_AT_BRIDGE|OLDPWD|OPTERR|OPTIND|ORBIT_SOCKETDIR|OSTYPE|PAPERSIZE|PATH|PIPESTATUS|PPID|PS1|PS2|PS3|PS4|PWD|RANDOM|REPLY|SECONDS|SELINUX_INIT|SESSION|SESSIONTYPE|SESSION_MANAGER|SHELL|SHELLOPTS|SHLVL|SSH_AUTH_SOCK|TERM|UID|UPSTART_EVENTS|UPSTART_INSTANCE|UPSTART_JOB|UPSTART_SESSION|USER|WINDOWID|XAUTHORITY|XDG_CONFIG_DIRS|XDG_CURRENT_DESKTOP|XDG_DATA_DIRS|XDG_GREETER_DATA_DIR|XDG_MENU_PREFIX|XDG_RUNTIME_DIR|XDG_SEAT|XDG_SEAT_PATH|XDG_SESSION_DESKTOP|XDG_SESSION_ID|XDG_SESSION_PATH|XDG_SESSION_TYPE|XDG_VTNR|XMODIFIERS)\b"

commandAfterHeredoc = {
    "pattern": r"(^([\"']?)\w+\2)[ \t]+\S.*",
    "lookbehind": True,
    "alias": 'punctuation',  # this looks reasonably well in all themes
    "inside": None  # see below
}

insideString = {
    'bash': commandAfterHeredoc,
    'environment': {
        "pattern": r"\$" + envVars,
        "alias": 'constant'
    },
    'variable': [
        # [0]: Arithmetic Environment
        {
            "pattern": r"\$?\(\([\s\S]+?\)\)",
            "greedy": True,
            "inside": {
                # If there is a $ sign at the beginning highlight $(( and )) as variable
                'variable': [
                    {
                        "pattern": r"(^\$\(\([\s\S]+)\)\)",
                        "lookbehind": True
                    },
                    r"^\$\(\("
                ],
                'number': r"\b0x[\dA-Fa-f]+\b|(?:\b\d+(?:\.\d*)?|\B\.\d+)(?:[Ee]-?\d+)?",
                # Operators according to https://www.gnu.org/software/bash/manual/bashref.html#Shell-Arithmetic
                'operator': r"--?|-=|\+\+?|\+=|!=?|~|\*\*?|\*=|\/=?|%=?|<<=?|>>=?|<=?|>=?|==?|&&?|&=|\^=?|\|\|?|\|=|\?|:",
                # If there is no $ sign at the beginning highlight (( and )) as punctuation
                'punctuation': r"\(\(?|\)\)?|,|;"
            }
        },
        # [1]: Command Substitution
        {
            "pattern": r"\$\((?:\([^)]+\)|[^()])+\)|`[^`]+`",
            "greedy": True,
            "inside": {
                'variable': r"^\$\(|^`|\)$|`$"
            }
        },
        # [2]: Brace expansion
        {
            "pattern": r"\$\{[^}]+\}",
            "greedy": True,
            "inside": {
                'operator': r":[-=?+]?|[!\/]|##?|%%?|\^\^?|,,?",
                'punctuation': r"[\[\]]",
                'environment': {
                    "pattern": r"({)" + envVars,
                    "lookbehind": True,
                    "alias": 'constant'
                }
            }
        },
        r"\$(?:\w+|[#?*!@$])"
    ],
    # Escape sequences from echo and printf's manuals, and escaped quotes.
    'entity': r"(?:[abceEfnrtv\"]|O?[0-7]{1,3}|x[0-9a-fA-F]{1,2}|u[0-9a-fA-F]{4}|U[0-9a-fA-F]{8})"
}

Prism.LanguagesPatterns["bash"] = {
    'shebang': {
        "pattern": r"^#!\s*\/.*",
        "alias": 'important'
    },
    'comment': {
        "pattern": r"(^|[^\"{\$])#.*",
        "lookbehind": True
    },
    'function-name': [
        # a) function foo {
        # b) foo() {
        # c) function foo() {
        # but not “foo {”
        {
            # a) and c)
            "pattern": r"(\bfunction\s+)\w+(?=(?:\s*\(?:\s*\))?\s*\{)",
            "lookbehind": True,
            "alias": 'function'
        },
        {
            # // b)
            "pattern": r"\b\w+(?=\s*\(\s*\)\s*\{)",
            "alias": 'function'
        }
    ],
    # Highlight variable names as variables in for and select beginnings.
    'for-or-select': {
        "pattern": r"(\b(?:for|select)\s+)\w+(?=\s+in\s)",
        "alias": 'variable',
        "lookbehind": True
    },
    # Highlight variable names as variables in the left-hand part
    # of assignments (“=” and “+=”).
    'assign-left': {
        "pattern": r"(^|(\s)|[;|&]|[<>]\()\w+(?=\+?=)",
        "inside": {
            'environment': {
                "pattern": r"(^|(\s)|[;|&]|[<>]\()" + envVars,
                "lookbehind": True,
                "alias": 'constant'
            }
        },
        "alias": 'variable',
        "lookbehind": True
    },
    'string': [
        # Support for Here-documents https://en.wikipedia.org/wiki/Here_document
        {
            "pattern": r"((?:^|[^<])<<-?\s*)(\w+?)\s[\s\S]*?(?:\r?\n|\r)\2",
            "lookbehind": True,
            "greedy": True,
            # for better performance
            # "inside": insideString
        },
        # Here-document with quotes around the tag
        # → No expansion (so no “inside”).
        {
            "pattern": r"((?:^|[^<])<<-?\s*)([\"'])(\w+)\2\s[\s\S]*?(?:\r?\n|\r)\3",
            "lookbehind": True,
            "greedy": True,
            # for better performance
            # "inside": {
            #    '"bash"': commandAfterHeredoc
            #}
        },
        # “Normal” string
        {
            "pattern": r"(^|[^\\](?:\\\\)*)([\"'])(?:\\[\s\S]|\$\([^)]+\)|\$(?!\()|`[^`]+`|(?!\2)[^\\`$])*\2",
            "lookbehind": True,
            "greedy": True,
            # for better performance
            # "inside": insideString
        }
    ],
    'environment': {
        "pattern": r"\$?" + envVars,
        "alias": 'constant'
    },
    'variable': insideString["variable"],
    'function': {
        "pattern": r"(^|[\s;|&]|[<>]\()(?:add|apropos|apt|aptitude|apt-cache|apt-get|aspell|automysqlbackup|awk|basename|bash|bc|bconsole|bg|bzip2|cal|cat|cfdisk|chgrp|chkconfig|chmod|chown|chroot|cksum|clear|cmp|column|comm|composer|cp|cron|crontab|csplit|curl|cut|date|dc|dd|ddrescue|debootstrap|df|diff|diff3|dig|dir|dircolors|dirname|dirs|dmesg|du|egrep|eject|env|ethtool|expand|expect|expr|fdformat|fdisk|fg|fgrep|file|find|fmt|fold|format|free|fsck|ftp|fuser|gawk|git|gparted|grep|groupadd|groupdel|groupmod|groups|grub-mkconfig|gzip|halt|head|hg|history|host|hostname|htop|iconv|id|ifconfig|ifdown|ifup|import|install|ip|jobs|join|kill|killall|less|link|ln|locate|logname|logrotate|look|lpc|lpr|lprint|lprintd|lprintq|lprm|ls|lsof|lynx|make|man|mc|mdadm|mkconfig|mkdir|mke2fs|mkfifo|mkfs|mkisofs|mknod|mkswap|mmv|more|most|mount|mtools|mtr|mutt|mv|nano|nc|netstat|nice|nl|nohup|notify-send|npm|nslookup|op|open|parted|passwd|paste|pathchk|ping|pkill|pnpm|popd|pr|printcap|printenv|ps|pushd|pv|quota|quotacheck|quotactl|ram|rar|rcp|reboot|remsync|rename|renice|rev|rm|rmdir|rpm|rsync|scp|screen|sdiff|sed|sendmail|seq|service|sftp|sh|shellcheck|shuf|shutdown|sleep|slocate|sort|split|ssh|stat|strace|su|sudo|sum|suspend|swapon|sync|tac|tail|tar|tee|time|timeout|top|touch|tr|traceroute|tsort|tty|umount|uname|unexpand|uniq|units|unrar|unshar|unzip|update-grub|uptime|useradd|userdel|usermod|users|uudecode|uuencode|v|vdir|vi|vim|virsh|vmstat|wait|watch|wc|wget|whereis|which|who|whoami|write|xargs|xdg-open|yarn|yes|zenity|zip|zsh|zypper)(?=$|[)\s;|&])",
        "lookbehind": True
    },
    'keyword': {
        "pattern": r"(^|[\s;|&]|[<>]\()(?:if|then|else|elif|fi|for|while|in|case|esac|function|select|do|done|until)(?=$|[)\s;|&])",
        "lookbehind": True
    },
    # https://www.gnu.org/software/bash/manual/html_node/Shell-Builtin-Commands.html
    'builtin': {
        "pattern": r"(^|[\s;|&]|[<>]\()(?:\.|:|break|cd|continue|eval|exec|exit|export|getopts|hash|pwd|readonly|return|shift|test|times|trap|umask|unset|alias|bind|builtin|caller|command|declare|echo|enable|help|let|local|logout|mapfile|printf|read|readarray|source|type|typeset|ulimit|unalias|set|shopt)(?=$|[)\s;|&])",
        "lookbehind": True,
        # Alias added to make those easier to distinguish from strings.
        "alias": 'class-name'
    },
    'boolean': {
        "pattern": r"(^|[\s;|&]|[<>]\()(?:true|false)(?=$|[)\s;|&])",
        "lookbehind": True
    },
    'file-descriptor': {
        "pattern": r"\B&\d\b",
        "alias": 'important'
    },
    'operator': {
        # Lots of redirections here, but not just that.
        "pattern": r"\d?<>|>\||\+=|==?|!=?|=~|<<[<-]?|[&\d]?>>|\d?[<>]&?|&[>&]?|\|[&|]?|<=?|>=?",
        "inside": {
            'file-descriptor': {
                "pattern": r"^\d",
                "alias": 'important'
            }
        }
    },
    'punctuation': r"\$?\(\(?|\)\)?|\.\.|[{}[\];\\]",
    'number': {
        "pattern": r"(^|\s)(?:[1-9]\d*|0)(?:[.,]\d+)?\b",
        "lookbehind": True
    },
    'enter': r"[\r\n]+",
    'blank': r"[ \f\t\v]+"
}

commandAfterHeredoc["inside"] = Prism.LanguagesPatterns["bash"]

# Patterns in command substitution.
toBeCopied = [
    'comment',
    'function-name',
    'for-or-select',
    'assign-left',
    'string',
    'environment',
    'function',
    'keyword',
    'builtin',
    'boolean',
    'file-descriptor',
    'operator',
    'punctuation',
    'number'
]
inside = insideString["variable"][1]["inside"]
for i in range(0, len(toBeCopied)):
    inside[toBeCopied[i]] = Prism.LanguagesPatterns["bash"][toBeCopied[i]]

Prism.LanguagesPatterns["shell"] = Prism.LanguagesPatterns["bash"]

__all__ = []

