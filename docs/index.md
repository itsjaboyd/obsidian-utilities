# Welcome to Obsidian Utilities!

Visit the repository on Github for more information ([obsidian-utilities](https://github.com/itsjaboyd/obsidian-utilities)).

## Commands

`copy_template` - Copy a template file location to a given directory.

* Option `--uf`: Attempt to match the destination formatting for the copied template.
* Option `--n`: The number of copies to make of the template file.

**Examples**

`copy_template /Users/username/notes/templates/template-one.md /Users/username/notes/files --uf`

This example will copy the template-one.md template file to the files/ directory once with an 
attempt to match the destination formatting of notes that already exist in files/.

`copy_template template-two.md /Users/username/notes/dailys --n 10`

This example will copy the template-two.md template file using any possibly configured template 
location to the dailys/ directory ten times without attempting to match any destination formatting.
