from django.db import models

class Contact(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    description=models.TextField()
    def __str__(self): 
        return f' Message from {self.name}'
    
class Blogs(models.Model):
    title=models.CharField(max_length=50)
    description=models.TextField()
    authorname=models.CharField(max_length=60)
    img=models.ImageField(upload_to='images/',blank=True,null=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'uploaded by  {self.authorname} on {self.timestamp}'
