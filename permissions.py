import discord
import math

class Permissions:
    value: int
    all_perms = {1 << i for i in range(1, 46)}

    def __init__(self, value: int):
        self.value = value


    def add(self, value: int):
        self.value |= value

        return self

    def isset(self):
        # Convert self.value to a set of permissions
        perms = {(i, 1 << i) for i in range(1, 46) if self.value & (1 << i)}

        # Return the set of permissions
        return perms

# If ran as a script, run this
if __name__ == '__main__':
    perms = Permissions(1 << 10)
    perms.add(1 << 11).add(1 << 12).add(1 << 13)

    bot = Permissions(1 << 10)
    bot.add(1<<11)

    pset = perms.isset()
    bset = bot.isset()

    print(pset)
    print(bset)
    missing = pset - bset

    permissions = {v:k for k,v in discord.Permissions.VALID_FLAGS.items()}

    for m in missing:
        print(m[0], permissions[m[1]])