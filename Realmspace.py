
import OrbitBasics as ob

names = ['Anadia',  # spherical earth body
         'Coliar',  # spherical air body
         'Toril',   # spherical earth body orbited by one moon (Selune) and an asteroid cluster (Tears of Selune)
         'Karpri',  # spherical water body
         'Chandos', # spherical water body
         'Glyth',   # spherical, ringed earth body orbited by three moons
         'Garden',  # cluster of seven earth bodies held together by a colossal plant, orbited by eleven moons
         'H\'catha' # Disk-shaped water body orbited by two moons
         ]

r_sphere = 3200 # million miles
r_edge = [3150,
          3100,
          3000,
          2900,
          2800,
          2200,
          2000,
          1600
          ]

a_vec = []

RealmspaceSystem = {'names':names,
                    'r'    :a_vec,    
                    'title':'Realmspace',
                    'CB'   :ob.Sun}