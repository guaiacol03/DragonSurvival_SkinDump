usage: python ddump.py [-h] {list} {dump <name> <type>} {info <name>} [--key KEY]

A tool for minecraft mod DragonSurvival (https://github.com/DragonSurvivalTeam/DragonSurvival) to dump skins from developers repo.
Can automatically compose texture packs, which can be installed as described in DragonSurvival wiki under "Skin testing"

commands:
    list    List available skins
    dump    Dump skin to texture pack
        <name>  Name of a player
        <type>  Dragon type to assign skin to (in texture pack): forest, cave, sea
    info    Show info about player's skin
        <name>  Name of a player

options:
    -h, --help    show this help message and exit
    -key <KEY>    GitHub personal access key. Optional, but recommended not to run out of request limits

How to dump and install a skin locally:
    * Install python version 3.12+
    * Run "python ddump.py dump <player_name> <dragon_type>"
        * You can see player skins via ingame menu
        * Set dragon_type to whichever dragon type you're creating
    * Copy archive "dump-PlayerName.zip" to "resourcepacks" folder of a game instance (or install via a launcher)
    * Enable a pack in "Resource packs" menu ingame (make sure to disable/overwrite other dragon skin dumps)
    * Create/modify a dragon character, picking an "Old texture" option and a specie specified in dragon_type
        * You can re-create existing character with "/dragon-altar" and set its age via "/dragon ..."
        * Or just change appearance via "/dragon-editor"
