#Generate lab command.
carme lab --help > lab.tmp && sed -e '/## Usage/r lab.tmp' -e '$G' ./templates/lab.template > lab.rst && rm lab.tmp
#Generate notebook command.
carme notebook --help > notebook.tmp && sed -e '/## Usage/r notebook.tmp' -e '$G' ./templates/notebook.template > notebook.rst && rm notebook.tmp
#Generate Carme package command.
carme package --help > package.tmp && sed -e '/## Usage/r package.tmp' -e '$G' ./templates/package.template > package.rst && rm package.tmp
#Generate Carme help command.
carme lab --help > help.tmp && sed -e '/## Usage/r help.tmp' -e '$G' ./templates/help.template > help.rst && rm help.tmp
#Generate Carme build command.
carme build --help > build.tmp && sed -e '/## Usage/r build.tmp' -e '$G' ./templates/build.template > build.rst && rm build.tmp
#Generate Carme cleanup command.
carme cleanup --help > cleanup.tmp && sed -e '/## Usage/r cleanup.tmp' -e '$G' ./templates/cleanup.template > cleanup.rst && rm cleanup.tmp
#Generate Carme cmd command.
carme cmd --help > cmd.tmp && sed -e '/## Usage/r cmd.tmp' -e '$G' ./templates/cmd.template > cmd.rst && rm cmd.tmp
#Generate Carme git command.
carme git --help > git.tmp && sed -e '/## Usage/r git.tmp' -e '$G' ./templates/git.template > git.rst && rm git.tmp
#Generate Carme git command.
carme new --help > new.tmp && sed -e '/## Usage/r new.tmp' -e '$G' ./templates/new.template > new.rst && rm new.tmp
#Generate Carme save command.
carme save --help > save.tmp && sed -e '/## Usage/r save.tmp' -e '$G' ./templates/save.template > save.rst && rm save.tmp
#Generate Carme start command.
carme start --help > start.tmp && sed -e '/## Usage/r start.tmp' -e '$G' ./templates/start.template > start.rst && rm start.tmp
#Generate Carme stop command.
carme stop --help > stop.tmp && sed -e '/## Usage/r stop.tmp' -e '$G' ./templates/stop.template > stop.rst && rm stop.tmp
