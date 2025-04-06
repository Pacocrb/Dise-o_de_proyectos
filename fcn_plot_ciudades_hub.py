import matplotlib.pyplot as plt
def plot_ciudades_hub(a, b, x_hub, y_hub, optimal_x,optimal_y):
    plt.figure(2)
    plt.scatter(a,b, marker='o', s=30,edgecolors='blue',facecolor='none')
    plt.scatter(x_hub,y_hub, marker='o', s=30,edgecolors='red',facecolor='none')
    plt.scatter(optimal_x,optimal_y, marker='o', s=30,edgecolors='purple',facecolor='none')
    plt.title('Tiendas de electrodomésticos en la provincia de Málaga', loc = 'center',fontsize = 30, fontname= 'Times New Roman')
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.xlabel('Longitud', loc = 'center',fontsize = 30, fontname= 'Times New Roman')
    plt.ylabel('Latitud', loc = 'center',fontsize = 30, fontname= 'Times New Roman')
    plt.minorticks_on()
    plt.grid(True, which='major', linewidth=0.5, color='gray', linestyle='-', alpha=0.7)  # Rejilla principal
    plt.grid(True, which='minor', linewidth=0.2, color='black', linestyle=':', alpha=0.5)  # Rejilla menor
    plt.show()