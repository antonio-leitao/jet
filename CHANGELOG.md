# Changelog

## Changes since 887cdbcbb91cbb23ad7c84b2e4da8ac825d4171f

* 3ab7da2: Typos
* c4c17f5: Added changelog recipe to makefile.
* 0c1a37b: Changes to readme
* af1da97: Final tweaks to readme
* c537c0a: fixed links
* b07170e: added links and corrected minor mistakes in Readme
* bde7815: Centered some divs in readme
* ed81a8a: added banner to readme
* 275205d: Changes to Readme
* 3bb570e: Typos
* c14612e: Changes to readme
* 8db9168: Updated readme and started the vhs gifs.
* 5c5758b: Fixed issue with progress bar.
* ab037f6: Pre-release tests
* 30f0bb4: Corrected import statements
* 448f18b: Finished new colors and removed hanging prints. release is ready. Starting work on example tests
* e7fe77b: Finalized changes to Jet. Stable version. Minor patches probably will be required.
* 5fa8449: Refactored code completely Needs clean up specially on gum colors
* 7244a97: Refactored entire runner, added custom types. Probably in future change from Namedtuple to dataclass but will see. starting on seer and doctor which might take a bit
* 5e06fc6: Started refactoring, major changes. Lost oportunity to do this in a new branch though
* 63042b8: added flex behaviour to report block
* 7d9178a: release delayed, in order to enable parallelization runner refactoring is necessary. Maybe reconsider the use of classes. (since they are unpickleable). Do this before release otherwise its just spaghetti code. Its a thing of 2 days work.
* 3ff0c98: Fixed bugs in argparser
* 70a9251: Debug on argparser for file support
* 12efe4d: Changed progress bar color and verbose. Added option for either percentage or counts
* 9c83bb1: Small issues debugging and prettyfying scripts
* 1a0593d: Finished, ready for VHS and initial release. Don't forget to remove time.sleep!!!
* 751f89e: Made test selection screen. Added cool margin feature. Goddam gum is great and powerfull. Fnishing touches, first release only a few hours of work away.
* 0ea86e9: added new diagnosis, added support for custom errors and custom set checks. Missing just the diagnosis selection
* 910a2af: Added new error catching function and overhauled diagnostics seer. Testing now. Missing only the diagnostics chooser.
* d49aff0: removed console from doctor, starting pager diagnostics
* fc8d505: Fixed gitignore file
* 2b90075: Created gitignore
* 06414af: Added --all, --quiet and --version to jet. Stable release. Starting new diagnosis report, lots of ideas
* d053625: Passed everything to pytproject.toml and testes. added pip-chill but not sure if worth it. Added --all flag to cli.
* c2626e9: built wheels and added entry point for cli
* 945890a: Migrated from Nau to Jet, initial commit on new remote repo
* 5901382: Added main file and argparser. Library is now finished. Missing only deploy to Pypy and CLI support.
* a04f9bc: Finished base functionality, everything works. Starting cleanup.
* dcf7a2a: finished runner. Starting long diagnostics script. Color permanently changed as it looks better. Considering changing name to JET instead.
* 6eccc39: Finally fixes escape sequence that clears terminal goddam was hard. Now its in a state that is very usable and is a good thing to have in back pocket.
* 3228210: Changed main color to purple. much better actually like it. Relized I need quitting checks here and there.
* 18a4ca2: Introduced module choosing into base clase. Removed old one. Started (almost finished) diagnosis script. Starting to rething colors though. a bit bleah. Specially in module selec its jsut a bit weird still.Going to desaturate them
* 51c6138: integrated new progress bar to runner, and updated colors. Todo clean choice script and maybe allow for further costumization since it will be needed for diagnostics.
* b2d6706: Finished module choosing script, movint to progress bar. Module choice should stay as script but progress should be integrated. TODO add printf cleaner to remove progress bar. (maybe there is a native option actually)
* 92aad3e: Removed color (at least made it optional) added possibility of removing header cleaning it up now
* f1704da: Gumtest contains the main method for iterating clearing input and adding commands etc
* 35c6044: Finished gum choose option to include fainted descriptions. Should be in separate module for organization and simplicity. Not surea about color but prefix is looking better. Work on way of showing keybinds.
* 9a9a41c: Customized gum. Changed color (31 remember it), changed maximum width and height. Gum's costumization is deeper than readily available. Might make bubble tea superfluous. This is great
* c64dc95: added commit make file
* a613cb8: experienced with different TUI libraries, reverted to just gum. Found rich whcih is good but thaths about it
* f51664c: finished first part, some issues with color codes but seems to be just zsh scpecific. Consider switching to alacrity?
* fcc6e62: configured gum minimally but still problems with decodeing the output. maybe regex will be necessary?
* 5b5ebc9: fixed standard output capture system
* c79a343: added progressbar and verbose options. Fixing standardoutup catcher. Tqdm still displays artifacts in progress bar
* 107cc2d: commit before the addition of progress bar
* 8a71590: first runner version, working very nice
* 7fb5ef9: dropped scene idea, probably redudante prone to errors and frankly unncecesary
