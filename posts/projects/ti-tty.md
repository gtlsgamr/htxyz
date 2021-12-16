title="Time In TTY, a CLI timetracking script"
description="A command line time tracking shell script."
date="2021-12-08"
+++
This is a time tracking shell script, used to track time for ongoing projects or some other task that needs time tracking. It uses unix timestamp and the `date` utility that comes with most unix-like operating systems. It is lightweight, and does one thing well, track time. It is similar to [Timewarrior](https://timewarrior.net/) but the difference is in the implementation, as in timewarrior is too complex for my use case. This is just so very usable. Its data is stored in plaintext, it is easily modifiable and it is modular. Here are instructions on how to use [titty](https://github.com/gtlsgamr/ti-tty).


#### Installation:
Just copy the titty file to your path

#### Usage:

```titty start [taskname]```

Start tracking time for a task.

```titty start taskname [time]```

Start tracking time for a task from some time ago.    
example:    
    titty start Task23 1hour    
    titty start Task42 1min    
    titty start Task43 54sec    

```titty status```
	
  Display the time tracked so far for the current task.

```titty stop```

  Display the raw masterlist (for piping into other programs)

```titty raw```

Stop tracking the current task.

```titty display [day|week|month|year|all]```

Display tracked time (default is month).

```titty delete [all]```

Delete the previous task or all tasks.

```titty help```

Display this help text.

Configuration:
The default configuration files are located in ~/.config/titty/
This directory can be changed using the \$TITTY_CONFIG_DIR environment variable.

