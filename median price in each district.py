import pandas as pd
import matplotlib.pyplot as plt
import folium
df = pd.read_csv('clean_otodom.csv')
pd.set_option("display.max_columns", None)
n_rooms = 2
# find mean and median prices for n-rooms apartments grouped by Warsaw's districts
median_prices = df[df['Rooms'] == n_rooms].groupby('District')['Full_price'].median().sort_values()
mean_prices = df[df['Rooms'] == n_rooms].groupby('District')['Full_price'].mean().sort_values()
# plot them
prices = pd.concat([median_prices, mean_prices], axis=1, keys=['Median', 'Mean'])
ax = prices.plot(kind='bar', color=['blue', 'green'])
ax.set_xlabel('District')
ax.set_ylabel('Price (PLN)')
ax.set_title('Median and Mean Prices by District')
plt.show()
# plot median prices on the map of Warsaw
m = folium.Map(location=[52.2297, 21.0122], zoom_start=11)
# define a dictionary with district names and their corresponding latitude and longitude
districts_lat_long = {
    'Bemowo': (52.2389, 20.9131),
    'Białołęka': (52.3118, 20.9474),
    'Bielany': (52.2908, 20.9474),
    'Mokotów': (52.1939, 21.0459),
    'Ochota': (52.2122, 20.9725),
    'Praga-Południe': (52.2369, 21.0493),
    'Praga-Północ': (52.2643, 21.0285),
    'Rembertów': (52.2592, 21.1375),
    'Śródmieście': (52.2297, 21.0118),
    'Targówek': (52.2761, 21.0588),
    'Ursus': (52.1919, 20.8823),
    'Ursynów': (52.1418, 21.0302),
    'Wawer': (52.1950, 21.1371),
    'Wesoła': (52.2500, 21.2500),
    'Wilanów': (52.1650, 21.0900),
    'Włochy': (52.1864, 20.9472),
    'Wola': (52.2367, 20.9544),
    'Żoliborz': (52.2675, 20.9797)
}
# loop through the districts and get the corresponding latitude and longitude values
for district in median_prices.index:
    lat_long = districts_lat_long[district]
    lat, long = lat_long[0], lat_long[1]
    # plot the marker on the map with the median price
    folium.Marker([lat, long], popup=district + ':' + str(median_prices[district]) + ' PLN').add_to(m)
m.save("Median price of 2-rooms apartments of each Warsaw district.html")
print(df.describe())