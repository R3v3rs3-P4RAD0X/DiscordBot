from command import Command
import random


class Gamble(Command):
    usage = "gamble <bet>"

    async def run(self):
        # Check if args length is >= 1
        if len(self.args) >= 1:
            # Find the first integer in the args
            amount = self.client.config.FilterFirstType(self.args, int, lambda x: x > 0)

            # Check if the amount is None or False
            if amount is None or amount is False:
                await self.SendMessage(f"Invalid amount. Usage: `{self.usage}`")
                return
            
            # Get the user's balance
            user = self.client.database.GetUser(self.message.author.id)

            # Check if the amount is greater than the user's balance
            if amount > user.economy.balance:
                await self.SendMessage("You don't have enough money to gamble that much!")
                return
            
            # Check if the amount is greater than the max gamble
            if amount > self.client.CONSTANTS['commands']['economy']['max_gamble']:
                await self.SendMessage(f"You can't gamble more than £{self.client.CONSTANTS['commands']['economy']['max_gamble']}!")
                return
            
            # Get the user's gamble chance
            chance = random.choices([True, False], weights=[0.3, 0.7])[0]

            # Check if the user won
            if chance:
                # Calculate how much the user has won
                winMultiplier = self.client.config.RandomNumber(1, 100) / 100

                # Calculate the amount the user has won
                won = round(amount * winMultiplier)

                # Add the won amount to the user's balance
                user.economy.balance += (amount + won)

                # Save the user's economy
                self.client.database.UpdateUser(user)

                # Convert winMultiplier to a percentage
                winMultiplier = round(winMultiplier * 100)

                # Check if the user can embed links
                if self.perms['bot'].embed_links:
                    # Create the embed
                    embed = self.embed(
                        title="You won!",
                        fields = [
                            {
                                "name": "Amount",
                                "value": f"£{won + amount} (£{amount} + £{won})"
                            },
                            {
                                "name": "Random Win Multiplier",
                                "value": f"{winMultiplier}%"
                            }
                        ],
                        colour = (0, 255, 0),
                        footer="Amount won is your bet + the amount you won"
                    )

                    # Send the embed
                    await self.SendEmbed(embed=embed)
                    return
                
                # Send a message
                await self.SendMessage("\n".join([
                    "You won!",
                    f"Amount: £{won + amount} (£{amount} + £{won})",
                    f"Random Win Multiplier: {winMultiplier}%",
                    "Amount won is your bet + the amount you won"
                ]))
                return
            
            # Update the user's balance
            user.economy.balance -= amount

            # Save the user's economy
            self.client.database.UpdateUser(user)

            # Check if the user can embed links
            if self.perms['bot'].embed_links:
                # Create the embed
                embed = self.embed(
                    title="You lost!",
                    fields = [
                        {
                            "name": "Amount",
                            "value": f"£{amount}"
                        },
                        {
                            "name": "Random Win Multiplier",
                            "value": "0%"
                        }
                    ],
                    colour = (255, 0, 0)
                )

                # Send the embed
                await self.SendEmbed(embed=embed)
                return
            
            # Send a message
            await self.SendMessage("\n".join([
                "You lost!",
                f"Amount: £{amount}",
                "Random Win Multiplier: 0%"
            ]))

        else:
            # Tell the user how to use the command
            await self.SendMessage(f"You haven't specified an amount to gamble. Usage: `{self.usage}`")