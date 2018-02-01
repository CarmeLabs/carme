"""The save command."""


from json import dumps

from .base import Base


class Save(Base):
    """Save the file"""
    def run(self):
        print("running")
        #print(self.bash_command(self.options['<command>'],self.cluster_commands[self.options['<command>']]))
        #self.bash_command(self, "save","git add -A & git commit -m 'saving' & git push "))
        print(self.bash_command("saving work", "git add -A "))
        print(self.bash_command("saving work", "git commit -m 'saving'"))
        print(self.bash_command("saving work", "git push "))
