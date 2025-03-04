from django.db import models

class Album(models.Model):
    """
    Represents a collection of music files.
    One album can have multiple music files.
    """
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class MusicFile(models.Model):
    """
    Represents a single music track.
    Each track belongs to exactly one album.
    """
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='music_files')
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='music/')
    duration = models.PositiveIntegerField(help_text="Duration in seconds")
    order = models.PositiveIntegerField(default=0, help_text="Order of the music file in the album")

    def __str__(self):
        return f"{self.title} ({self.album.name})"
