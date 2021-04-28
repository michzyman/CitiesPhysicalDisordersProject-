import os
import matplotlib.pyplot as plt

occ_struc = len(os.listdir(r'output\OCCUPIED_STRUCTURE')) 
vac_struc = len(os.listdir(r'output\VACANT_STRUCTURE')) 
vac_lot = len(os.listdir(r'output\VACANT_LOT')) 

print('Occupied Structure:', occ_struc)
print()
print('Vacant Structure: ', vac_struc)
print()
print('Vacant Lot: ', vac_lot)

x = [vac_lot,vac_struc,occ_struc]
y = ['Vacant Lot', 'Vacant Structure', 'Occupied Structure']
plt.pie(x=x, labels=y,colors=['purple','blue','orange'],autopct='%1.1f%%' )
plt.show()

x1 = [vac_struc+occ_struc, vac_lot]
y1 = ['Structure','Vacant Lot']
plt.pie(x=x1, labels=y1, colors=['orange','purple'],autopct='%1.1f%%')
plt.show()
