from sqlalchemy import DateTime, String, BigInteger, func, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(DeclarativeBase, AsyncAttrs):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String(100))
    one_time_mail: Mapped[str] = mapped_column(String(200), default=None, nullable=True)


class Birthday(Base):
    __tablename__ = "birthday"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    b_day: Mapped[int] = mapped_column(BigInteger)
    b_mon: Mapped[int] = mapped_column(BigInteger)


class Investment(Base):
    __tablename__ = "investment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    amount: Mapped[int] = mapped_column(BigInteger)
    all_money: Mapped[int] = mapped_column(BigInteger)


class Expenses(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    amount: Mapped[int] = mapped_column(BigInteger)
    expenses_name: Mapped[str] = mapped_column(String())


class Product_list(Base):
    __tablename__ = "product_list"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_name: Mapped[str] = mapped_column(String())


class LikeImage(Base):
    __tablename__ = "like_image"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    caption: Mapped[str] = mapped_column(String(100))
    image: Mapped[str] = mapped_column(String())
