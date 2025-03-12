from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, DateTime
from datetime import datetime

Base = declarative_base()
engine = create_engine("sqlite:///spotify.db")

Session = sessionmaker(bind = engine)
session = Session()

class Playlist(Base):
    __tablename__ = "playlists"

    id = Column(Integer(), primary_key = True)
    name = Column(String())
    date_created = Column(DateTime(), default = datetime.now())

    songs = relationship("Song", back_populates = "playlist", cascade = "all, delete-orphan")

    def __repr__(self):
        return f"Playlist : {self.id} : {self.name}"

    @property
    def song_count(self):
        return len(self.songs)

    @classmethod
    def create_playlist(cls, name):
        playlist = cls(name=name)
        session.add(playlist)
        session.commit()
        return playlist  

    @classmethod
    def get_all_playlists(cls) :
        return session.query(cls).all()

    @classmethod
    def find_by_name(cls, name) :
        return session.query(cls).filter(cls.name.ilike(f"%{name}%")).all()

    def delete_playlist(self):
        session.delete(self)
        session.commit()

    def get_songs(self) :
        return self.songs        

class Song(Base):
    __tablename__    = "songs"

    id = Column(Integer(), primary_key = True)
    title = Column(String())
    artist = Column(String())
    album = Column(String())
    genre = Column(String())
    runtime = Column(Integer())
    date_released = Column(DateTime())
    playlist_id = Column(Integer(), ForeignKey("playlists.id"))

    playlist = relationship("Playlist", back_populates = "songs")

    def __repr__(self):
        minutes, seconds = divmod(self.runtime, 60) 
        return f"Song : {self.id} : {self.title} | Artist : {self.artist} | Album : {self.album} | Runtime : {minutes}:{seconds:02d}"

    @property
    def formatted_runtime(self) :
        minutes, seconds = divmod(self.runtime, 60)
        return f"{minutes}:{seconds:02d}"

    @classmethod 
    def create_song(cls, title, artist, album, genre, runtime, date_released, playlist_id):
        song = cls(
            title = title,
            artist = artist,
            album = album,
            genre = genre,
            runtime = runtime,
            date_released = date_released,
            playlist_id = playlist_id,
        )  
        session.add(song)
        session.commit()
        return song

    @classmethod
    def get_all_songs(cls):
        return session.query(cls).all()         

    @classmethod
    def find_by_id(cls, song_id):
        return session.query(cls).filter(cls.id == song_id).first()

    @classmethod
    def search_song(cls, query) :
        return session.query(cls).filter(
            (cls.title.ilike(f"%{query}%")) |
            (cls.artist.ilike(f"%{query}%")) |
            (cls.album.ilike(f"%{query}%")) |
            (cls.genre.ilike(f"%{query}%"))
        ).all()

    def delete_song(self) :
        session.delete(self)
        session.commit()           

if __name__ == "__main__":
     Base.metadata.create_all(engine)     

