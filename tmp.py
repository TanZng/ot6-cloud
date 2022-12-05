import matplotlib.pyplot as plt
    
denmark_2011 = df_per_city[df_per_city.Country == "Denmark"][df_per_city["dt"] > "2011-1-1"][df_per_city["dt"] < "2012-1-1"]
denmark_2012 = df_per_city[df_per_city.Country == "Denmark"][df_per_city["dt"] > "2012-1-1"][df_per_city["dt"] < "2013-1-1"]
    
print("2011: ", denmark_2011["AverageTemperature"].mean())
print("2012: ", denmark_2012["AverageTemperature"].mean())
    
plt.scatter(x=denmark_2011['dt'],y=denmark_2011['AverageTemperature'],color='red', label="Denmark 2011")
plt.scatter(x=denmark_2012['dt'],y=denmark_2012['AverageTemperature'],color='blue', label="Denmark 2012")
    
plt.title('Denmark AverageTemperature 2011 vs 2012')
plt.show()