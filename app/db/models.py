from sqlmodel import Field, Relationship, SQLModel


class UserSettings(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    theme: str = Field(default="system")
    voice_preference: str = Field(default="voice1")
    emotion_choices: str = Field(default="")
    user: "User" = Relationship(back_populates="settings")


class User(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    privy_wallet_id: str = Field(default=None)
    wallet_id: str = Field(default=None)
    wallet_provider: str = Field(default=None)
    settings: UserSettings = Relationship(back_populates="user")
