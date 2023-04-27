from django.contrib import admin
from .models import Railwayroute
from .models import Mahanagari_Express
from .models import Pune_Bsl_Express
from .models import Nagpur_Pune_Express
from .models import Mahanagari_Express_Schedule
from .models import Nagpur_Pune_Express_Schedule
from .models import Pune_Bsl_Express_Schedule
from .models import Mahanagari_Express_Seat_Alloc
from .models import Nagpur_Pune_Express_Seat_Alloc
from .models import Pune_Bsl_Express_Seat_Alloc
from .models import Mahanagari_Express_Booked
from .models import Nagpur_Pune_Express_Booked
from .models import Pune_Bsl_Express_Booked
from .models import Seat_Alloc
from .models import registration

# Register your models here.
admin.site.register(Mahanagari_Express_Schedule)
admin.site.register(Nagpur_Pune_Express_Schedule)
admin.site.register(Pune_Bsl_Express_Schedule)
admin.site.register(Railwayroute)
admin.site.register(Mahanagari_Express)
admin.site.register(Pune_Bsl_Express)
admin.site.register(Nagpur_Pune_Express)
admin.site.register(Mahanagari_Express_Seat_Alloc)
admin.site.register(Nagpur_Pune_Express_Seat_Alloc) 
admin.site.register(Pune_Bsl_Express_Seat_Alloc)
admin.site.register(Mahanagari_Express_Booked)
admin.site.register(Nagpur_Pune_Express_Booked) 
admin.site.register(Pune_Bsl_Express_Booked) 
admin.site.register(Seat_Alloc)
admin.site.register(registration)



# class Maharashtra_Express(models.Model):
#     No=models.IntegerField()
#     StationName= models.CharField()
#     Arrives= models.timezone()
#     Departs= models.timezone()
#     StopTime= models.CharField(max_length=20)
#     DistanceTravelled= models.CharField(max_length=20)
#     Day= models.CharField(max_length=10)
# 
#                     #print(data2)

                    
#                         # train_no.append(cursor.fetchone())
#                         # print(train_no)
                    
#                         # print(train_with_priority)                 
#                         #print(sql2)