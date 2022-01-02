title="tidytilde, A script to make your HOME clean and tidy."
description="A script to make your HOME clean and tidy. ✨"
date="2021-12-08"
+++
Sometimes your $HOME directory gets too cluttered with .dotfiles and it just
looks very unclean. Fortunately the archwiki has a nice
[article](https://wiki.archlinux.org/title/XDG_Base_Directory) on how to make
it tidy. [tidytilde](https://github.com/gtlsgamr/tidytilde) automates many of
the dotfiles listed there, and since it
is a long list, it might be a while before all the files are implemented. You
just need to run the script and it will move the files to the necessary
location and create a file called `tidytilde_commands` in your $HOME directory
which will contain all the environment variables and aliases that need to be
set at startup. You can just source that file in your .profile to make sure it
works.

