# Imports
import schema

# Define Schemas
SchemaUser = schema.Schema("User")\
    .add("UserID", int, True)\
    .add("Economy", schema.Schema("Economy")\
        .add("Balance", int, True, 0)\
        .add("Bank", int, True, 0)\
        .add("LastDaily", int, True, 0)\
        .compose(), True, {})\
    .add("Levelling", schema.Schema("Levelling")\
         .add("XP", int, True, 0)\
         .add("Level", int, True, 0)\
         .compose(), True, {})\
    .compose()

SchemaGuild = schema.Schema("Guild")\
    .add("GuildID", int, True)\
    .add("Prefix", str, True, "s!")\
    .add("Welcome", schema.Schema("Welcome")\
        .add("Enabled", bool, True, False)\
        .add("ChannelID", int, True)\
        .add("Message", str, True, "Welcome {user} to {guild}!")\
        .compose(), True, {})\
    .add("Leave", schema.Schema("Leave")\
        .add("Enabled", bool, True, False)\
        .add("ChannelID", int, True)\
        .add("Message", str, True, "Goodbye {user}!")\
        .compose(), True, {})\
    .add("Log", schema.Schema("Log")\
        .add("Enabled", bool, True, False)\
        .add("ChannelID", int, True)\
        .compose(), True, {})\
    .compose()


# If ran directly
if __name__ == "__main__":
    # Print the schemas
    print(SchemaUser.new())
    print(SchemaGuild.new())