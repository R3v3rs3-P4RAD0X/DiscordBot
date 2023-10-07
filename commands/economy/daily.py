from command import Command
import datetime
import pendulum


class Daily(Command):
    usage = "daily"

    async def run(self):
        # Get the user's data from the database
        userData = self.client.database.GetUser(self.message.author.id)

        # Get the user's economy profile
        profile = userData.economy

        # Get the user's last daily
        lastDaily = profile.last_daily

        # Check if lastDaily is 0
        if lastDaily == 0:
            # Set lastDaily to now
            profile.last_daily = datetime.datetime.now().timestamp()

            # Calculate the daily income, min of £1000 or max of £10000 (5% of balance)
            amount = round(max(1000, min(10000, int(profile.balance * 0.05))))

            # Add the amount to the user's balance
            profile.balance = round(profile.balance + amount, 0)

            # Save the user's data
            self.client.database.UpdateUser(userData)

            # Send a message
            await self.SendMessage(f"You have claimed your daily reward of £{amount}!")

        # Otherwise, check if the user can claim their daily
        elif datetime.datetime.now().timestamp() - lastDaily >= 86400:
            # Set lastDaily to now
            profile.last_daily = datetime.datetime.now().timestamp()

            # Calculate the daily income, min of £1000 or max of £10000 (5% of balance)
            amount = round(max(1000, min(10000, int(profile.balance * 0.05))))

            # Add the amount to the user's balance
            profile.balance = round(profile.balance + amount, 0)

            # Save the user's data
            self.client.database.UpdateUser(userData)

            # Send a message
            await self.SendMessage(f"You have claimed your daily reward of £{amount}!")

        # Otherwise, send a message
        else:
            # Get the time left
            timeLeft = pendulum.from_timestamp(lastDaily + 86400)

            # Send a message
            await self.SendMessage(
                f"You can claim your daily reward in {timeLeft.diff().in_words()}!"
            )
