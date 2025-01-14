
# Crear gráfico de comparación de volúmenes para Standard, Sokolowsky, Petrenko y Brun
plt.figure(figsize=(12, 6))
plt.plot(weeks_common, new_volumes_standard[:3], marker='o', 

linestyle='-',
label='Standard (Esferoide)', linewidth=2, color='blue')
plt.plot(weeks_common, volumes_sokolowsky, marker='s', linestyle='--', 

label='Sokolowsky (Lit.)', linewidth=2, color='orange')
plt.plot(weeks_common, volumes_petrenko, marker='^', linestyle='-.', 

label='Petrenko (Lit.)', linewidth=2, color='green')
plt.plot(weeks_common, new_volumes_brun[:3], marker='d', linestyle=':', 

label='Brun (Esferoide)', linewidth=2, color='red')

# Etiquetas y formato
plt.xlabel('Semana gestacional', fontsize=12)
plt.ylabel('Volumen (litros)', fontsize=12)
plt.title('Comparación de volúmenes uterinos: Standard, Sokolowsky, Petrenko y Brun', 
fontsize=14)
plt.legend(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(weeks_common)
plt.show()