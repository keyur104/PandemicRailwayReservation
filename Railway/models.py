from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
# Create your models here.
class Railwayroute(models.Model):
    trainNo=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=50)
    source=models.CharField(max_length=50)
    destination=models.CharField(max_length=50)
    intermediate_station=ArrayField(models.CharField(max_length=40 , blank=False))
    src_time=models.TimeField()




class UserMob(models.Model):    
    username=models.CharField(max_length=20)
    mobileno=models.CharField(max_length=10)



class RegisterSignup(models.Model):    
    name=models.CharField(max_length=50)
    username=models.CharField(max_length=20)
    mobileno=models.CharField(max_length=11)
    email=models.CharField(max_length=50)
    password=models.CharField(max_length=50)




class Mahanagari_Express_Schedule(models.Model):
     trainNo=models.IntegerField()
     Day=models.CharField(max_length=50)
     date=models.DateField(timezone.now)
     RunningStatus=models.CharField(max_length=50)
     


class Nagpur_Pune_Express_Schedule(models.Model):
     trainNo=models.IntegerField()
     Day=models.CharField(max_length=50)
     date=models.DateField(timezone.now)
     RunningStatus=models.CharField(max_length=50)
    

class Pune_Bsl_Express_Schedule(models.Model):
     trainNo=models.IntegerField()
     Day=models.CharField(max_length=50)
     date=models.DateField(timezone.now)
     RunningStatus=models.CharField(max_length=50)


class Pune_Bsl_Express(models.Model):
    trainNo=models.IntegerField()
    No=models.IntegerField()
    StationName= models.CharField(max_length=50)
    Arrives= models.TimeField()
    Departs= models.TimeField()
    StopTime= models.CharField(max_length=20)
    DistanceTravelled= models.CharField(max_length=20)
    Day= models.CharField(max_length=10)

class Nagpur_Pune_Express(models.Model):
    trainNo=models.IntegerField()
    No=models.IntegerField()
    StationName= models.CharField(max_length=50)
    Arrives= models.TimeField()
    Departs= models.TimeField()
    StopTime= models.CharField(max_length=20)
    DistanceTravelled= models.CharField(max_length=20)
    Day= models.CharField(max_length=10)

class Mahanagari_Express(models.Model):
    trainNo=models.IntegerField()
    No=models.IntegerField()
    StationName= models.CharField(max_length=50)
    Arrives= models.TimeField()
    Departs= models.TimeField()
    StopTime= models.CharField(max_length=20)
    DistanceTravelled= models.CharField(max_length=20)
    Day= models.CharField(max_length=10)     


class Mahanagari_Express_Seat_Alloc(models.Model):
    date = models.DateField()
    Mumbai_Cst = ArrayField(models.CharField(max_length = 10))
    Dadar = ArrayField(models.CharField(max_length = 10))
    Thane = ArrayField(models.CharField(max_length = 10))
    Kalyan_Junction = ArrayField(models.CharField(max_length = 10))
    Igatpuri = ArrayField(models.CharField(max_length = 10))
    Nashik_Road = ArrayField(models.CharField(max_length = 10))
    Manmad_Junction = ArrayField(models.CharField(max_length = 10))
    Jalgaon_Junction = ArrayField(models.CharField(max_length = 10))
    Bhusaval_Junction = ArrayField(models.CharField(max_length = 10))
    Burhanpur = ArrayField(models.CharField(max_length = 10))
    Nepanagar = ArrayField(models.CharField(max_length = 10))
    Khandwa = ArrayField(models.CharField(max_length = 10))
    Itarsi_Junction = ArrayField(models.CharField(max_length = 10))
    Pipariya = ArrayField(models.CharField(max_length = 10))
    Narsinghpur = ArrayField(models.CharField(max_length = 10))
    Madan_Mahal = ArrayField(models.CharField(max_length = 10))
    Jabalpur = ArrayField(models.CharField(max_length = 10))
    Katni = ArrayField(models.CharField(max_length = 10))
    Maihar = ArrayField(models.CharField(max_length = 10))
    Satna = ArrayField(models.CharField(max_length = 10))
    Manikpur_Junction = ArrayField(models.CharField(max_length = 10))
    Cheoki = ArrayField(models.CharField(max_length = 10))
    Vindhyachal = ArrayField(models.CharField(max_length = 10))
    Mirzapur = ArrayField(models.CharField(max_length = 10))
    Chunar = ArrayField(models.CharField(max_length = 10))
    Kashi = ArrayField(models.CharField(max_length = 10))
    Varansi_Junction = ArrayField(models.CharField(max_length = 10))

class Nagpur_Pune_Express_Seat_Alloc(models.Model):
    date=models.DateField()
    Nagpur=ArrayField(models.CharField(max_length=30))
    Ajni=ArrayField(models.CharField(max_length=30))
    Wardha_Junction=ArrayField(models.CharField(max_length=30))
    Pulgaon_Junction=ArrayField(models.CharField(max_length=30))
    Dhamangaon=ArrayField(models.CharField(max_length=30)) 
    Badnera_Junction=ArrayField(models.CharField(max_length=30))
    Akola_Junction=ArrayField(models.CharField(max_length=30))
    Shegaon=ArrayField(models.CharField(max_length=30))
    Malkapur=ArrayField(models.CharField(max_length=30))
    Bhusaval_Junction=ArrayField(models.CharField(max_length=30))
    Jalgaon_Junction=ArrayField(models.CharField(max_length=30))
    Chalisgaon_Junction =ArrayField(models.CharField(max_length=30))
    Manmad_Junction=ArrayField(models.CharField(max_length=30))
    Kopargaon=ArrayField(models.CharField(max_length=30))
    Belapur=ArrayField(models.CharField(max_length=30))
    Ahmadnagar=ArrayField(models.CharField(max_length=30))
    Daund_Junction=ArrayField(models.CharField(max_length=30))
    Pune_Junction=ArrayField(models.CharField(max_length=30))

class Pune_Bsl_Express_Seat_Alloc(models.Model):
    date=models.DateField()
    Pune_Junction=ArrayField(models.CharField(max_length=30))
    Chinchvad=ArrayField(models.CharField(max_length=30))
    Lonavala=ArrayField(models.CharField(max_length=30)) 
    Karjat=ArrayField(models.CharField(max_length=30))
    Chauk=ArrayField(models.CharField(max_length=30))
    Mohope=ArrayField(models.CharField(max_length=30))
    Chikhli=ArrayField(models.CharField(max_length=30)) 
    Panvel=ArrayField(models.CharField(max_length=30))
    Kalyan_Junction=ArrayField(models.CharField(max_length=30))
    Igatpuri=ArrayField(models.CharField(max_length=30))
    Devlali=ArrayField(models.CharField(max_length=30))
    Nashik_Road=ArrayField(models.CharField(max_length=30))
    Lasalgaon =ArrayField(models.CharField(max_length=30))
    Manmad_Junction=ArrayField(models.CharField(max_length=30))
    Chalisgaon_Junction=ArrayField(models.CharField(max_length=30))
    Kajgaon=ArrayField(models.CharField(max_length=30))
    Pachora_Junction=ArrayField(models.CharField(max_length=30))    
    Jalgaon_Junction=ArrayField(models.CharField(max_length=30))
    Bhusaval_Junction=ArrayField(models.CharField(max_length=30))


class Pune_Bsl_Express_Booked(models.Model):
    group_id = models.IntegerField()
    seat = models.CharField(max_length=10)
    source = models.CharField(max_length=30)
    destination = models.CharField(max_length=30)
    date_of_journey = models.DateField()
    name = models.CharField(max_length=40)
    birth_type = models.CharField(max_length=10)
    PNR=models.IntegerField()

class Nagpur_Pune_Express_Booked(models.Model):
    group_id = models.IntegerField()
    seat = models.CharField(max_length=10)
    source = models.CharField(max_length=30)
    destination = models.CharField(max_length=30)
    date_of_journey = models.DateField()
    name = models.CharField(max_length=40)
    birth_type = models.CharField(max_length=10)
    PNR=models.IntegerField()

class Mahanagari_Express_Booked(models.Model):
    group_id = models.IntegerField()
    seat = models.CharField(max_length=10)
    source = models.CharField(max_length=30)
    destination = models.CharField(max_length=30)
    date_of_journey = models.DateField()
    name = models.CharField(max_length=40)
    birth_type = models.CharField(max_length=10)
    PNR=models.IntegerField()


class Seat_Alloc(models.Model):
    seat_no = models.CharField(max_length=10)
    class_type = models.CharField(max_length=10)
    birth_type = models.CharField(max_length=10)

class registration(models.Model):
    group_id = models.IntegerField()
    source = models.CharField(max_length=20)
    destination = models.CharField(max_length=20)
    date_of_journey = models.DateField()
    no_of_Seats = models.IntegerField()
    name = models.CharField(max_length=40)
    age = models.IntegerField()
    id_proof = models.CharField(max_length=20)
    id_number = models.CharField(max_length=20)
    class_type = models.CharField(max_length=10)
    birth_preferance = models.CharField(max_length=5)
    email=models.CharField(max_length=50)
    train_name=models.CharField(max_length=50)
    src_date=models.CharField(max_length=50)
    medical_status=models.CharField(max_length=50)
    PNR= models.IntegerField()
    medical=models.ImageField()
