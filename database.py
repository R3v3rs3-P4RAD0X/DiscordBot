from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# Define the database engine (you should replace 'sqlite:///mydb.db' with your actual database URL)
engine = create_engine("sqlite:///test.db")

# Create a base class for declarative models
Base = declarative_base()


# Define the model classes
class Guild(Base):
    __tablename__ = "guilds"

    # Model fields
    id = Column(Integer, primary_key=True, autoincrement=True)
    guild_id = Column(Integer, unique=True, nullable=False)

    # Relationships
    config = relationship("GuildConfig", uselist=False, back_populates="guild")

    def __repr__(self):
        return f"<Guild id={self.id} guild_id={self.guild_id}>"


class GuildConfig(Base):
    __tablename__ = "guild_configs"

    # Model fields
    id = Column(Integer, primary_key=True, autoincrement=True)
    guild_id = Column(Integer, ForeignKey("guilds.guild_id"), nullable=False)
    prefix = Column(String(10), nullable=False, default="!")

    # Relationships
    guild = relationship("Guild", back_populates="config")

    def __repr__(self):
        return (
            f"<GuildConfig id={self.id} guild_id={self.guild_id} prefix={self.prefix}>"
        )


class User(Base):
    __tablename__ = "users"

    # Model fields
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, unique=True, nullable=False)

    # Relationships
    economy = relationship("UserEconomy", uselist=False, back_populates="user")

    def __repr__(self):
        return f"<User id={self.id} user_id={self.user_id}>"


class UserEconomy(Base):
    __tablename__ = "user_economy"

    # Model fields
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    balance = Column(Integer, nullable=False, default=0)
    bank = Column(Integer, nullable=False, default=0)
    last_daily = Column(Integer, nullable=False, default=0)

    # Relationships
    user = relationship("User", back_populates="economy")

    def __repr__(self):
        return (
            f"<UserEconomy id={self.id} user_id={self.user_id} balance={self.balance}>"
        )


# Create the database tables
Base.metadata.create_all(engine)


# Database class
class Database:
    def __init__(self):
        # Create a session factory bound to the engine
        self.session_factory = sessionmaker(bind=engine)

        # Create a session
        self.session = self.session_factory()

    # Guilds
    def CreateGuild(self, guildID: int) -> Guild:
        # Create a new guild object
        guild = Guild(guild_id=guildID)
        guild.config = GuildConfig()

        # Add the guild to the session
        self.session.add(guild)

        # Commit the session
        self.session.commit()

        # Return the guild object
        return guild

    def GetGuild(self, guildID: int) -> Guild:
        # Get the guild from the database
        guild = self.session.query(Guild).filter_by(guild_id=guildID).first()

        # If the guild doesn't exist, create it
        if not guild:
            guild = self.CreateGuild(guildID)

        # Return the guild object
        return guild

    # Users
    def CreateUser(self, userID: int) -> User:
        # Create a new user object
        user = User(user_id=userID)
        user.economy = UserEconomy()

        # Add the user to the session
        self.session.add(user)

        # Commit the session
        self.session.commit()

        # Return the user object
        return user

    def GetUser(self, userID: int) -> User:
        # Get the user from the database
        user = self.session.query(User).filter_by(user_id=userID).first()

        # If the user doesn't exist, create it
        if not user:
            user = self.CreateUser(userID)

        # Return the user object
        return user

    def UpdateUser(self, user: User):
        # Update the user in the database
        self.session.merge(user)

        # Commit the session
        self.session.commit()
